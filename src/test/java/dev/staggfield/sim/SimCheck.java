package dev.staggfield.sim;

import dev.staggfield.sim.FluxSim.Cell;
import dev.staggfield.sim.FluxSim.Params;

/** Plain-main checks (no JUnit) so they run anywhere: java -cp out dev.staggfield.sim.SimCheck */
public final class SimCheck {
    static int fails;
    static void check(String name, boolean ok, String detail) {
        System.out.printf("%-4s %s  %s%n", ok ? "PASS" : "FAIL", name, detail);
        if (!ok) fails++;
    }
    static boolean near(double a, double b, double rel) { return Math.abs(a - b) <= rel * Math.abs(b); }

    /** n^3 graphite cube, fuel at even coordinates, optional source at the centre rod, optional absorbers in between. */
    static FluxSim pile(int n, double richness, boolean source, boolean absorbers) {
        FluxSim s = new FluxSim(n, n, n, Params.defaults());
        for (int z = 0; z < n; z++) for (int y = 0; y < n; y++) for (int x = 0; x < n; x++) {
            int odd = (x % 2) + (y % 2) + (z % 2);
            if (odd == 0) s.setFuel(x, y, z, richness);
            else if (absorbers && odd == 1) s.set(x, y, z, Cell.ABSORBER);
            else s.set(x, y, z, Cell.GRAPHITE);
        }
        if (source) s.set(n / 2 / 2 * 2, n / 2 / 2 * 2, n / 2 / 2 * 2, Cell.SOURCE);
        return s;
    }
    static void run(FluxSim s, int ticks) { for (int t = 0; t < ticks; t++) s.tick(); }
    static void insertAll(FluxSim s, int n, double v) {
        for (int z = 0; z < n; z++) for (int y = 0; y < n; y++) for (int x = 0; x < n; x++)
            if ((x % 2) + (y % 2) + (z % 2) == 1) s.setInsertion(x, y, z, v);
    }

    public static void main(String[] a) {
        Params p = Params.defaults();
        FluxSim probe = new FluxSim(1, 1, 1, p);
        check("eff(2) is 1", near(probe.eff(2), 1.0, 1e-12), "" + probe.eff(2));
        check("eff(1)=eff(3)=exp(-0.5)", near(probe.eff(1), Math.exp(-0.5), 1e-12) && near(probe.eff(3), probe.eff(1), 1e-12), "" + probe.eff(1));
        check("eff(4)=exp(-2)", near(probe.eff(4), Math.exp(-2), 1e-12), "" + probe.eff(4));

        // Hand value: source at x=0, fuel at x=2 with graphite between. flux in = S/6 * eff(2); F = sigma * flux
        FluxSim line = new FluxSim(3, 1, 1, p);
        line.set(0, 0, 0, Cell.SOURCE); line.set(1, 0, 0, Cell.GRAPHITE); line.setFuel(2, 0, 0, 1.0);
        run(line, 2000);
        double expect = p.sigma() * p.sourceFlux() / 6.0;
        check("line: fission = sigma*S/6", near(line.fission(2, 0, 0), expect, 0.03), line.fission(2, 0, 0) + " vs " + expect);

        // An air gap must stop the ray
        FluxSim gap = new FluxSim(3, 1, 1, p);
        gap.set(0, 0, 0, Cell.SOURCE); gap.setFuel(2, 0, 0, 1.0);
        run(gap, 500);
        check("air gap blocks flux", gap.fission(2, 0, 0) == 0, "" + gap.fission(2, 0, 0));

        FluxSim cold = pile(5, 1.0, false, false); run(cold, 3000);
        check("no source, no fission", cold.totalFission() == 0, "" + cold.totalFission());

        FluxSim sub = pile(3, 1.0, true, false); run(sub, 5000);
        double f0 = sub.totalFission(); run(sub, 1000);
        check("3^3 natural pile is subcritical and steady", sub.totalFission() > 0 && near(sub.totalFission(), f0, 0.01) && sub.meltedCells() == 0,
              "F=" + sub.totalFission() + " maxT=" + sub.maxHeat());

        FluxSim crit = pile(5, 1.0, true, false); run(crit, 30000);
        double fc = crit.totalFission(); run(crit, 500);
        check("5^3 natural pile self-limits by temperature", crit.meltedCells() == 0 && crit.maxHeat() > 40 && crit.maxHeat() < 1000 && near(crit.totalFission(), fc, 0.03),
              "F=" + crit.totalFission() + " maxT=" + crit.maxHeat());

        FluxSim hot = pile(5, 3.0, true, false); run(hot, 6000);
        check("enriched fuel, no control: meltdown", hot.meltedCells() > 0, "melted=" + hot.meltedCells());

        FluxSim held = pile(5, 3.0, true, true); insertAll(held, 5, 0.60); run(held, 30000);
        check("enriched fuel, control at 0.60 holds", held.meltedCells() == 0 && held.totalFission() > 0, "F=" + held.totalFission() + " maxT=" + held.maxHeat());

        FluxSim loose = pile(5, 3.0, true, true); insertAll(loose, 5, 0.50); run(loose, 30000);
        check("enriched fuel, control at 0.50 melts", loose.meltedCells() > 0, "melted=" + loose.meltedCells());

        FluxSim scram = pile(5, 3.0, true, true); insertAll(scram, 5, 0.60); run(scram, 20000);
        double before = scram.totalFission(), t0 = scram.maxHeat(); insertAll(scram, 5, 1.0); run(scram, 300);
        check("scram cuts fission under 5% in 300 ticks", scram.totalFission() < 0.05 * before, before + " -> " + scram.totalFission());
        double coolingOnly = p.ambient() + (t0 - p.ambient()) * Math.exp(-p.passiveCool() * 300);
        check("after scram, decay heat keeps the hottest rod above pure Newton cooling", scram.maxHeat() > coolingOnly + 1.0, scram.maxHeat() + " vs " + coolingOnly);

        // Active cooling: energy balance, then loss of coolant
        FluxSim loop = pile(5, 3.0, true, true); insertAll(loop, 5, 0.50);
        for (int z = 0; z < 5; z += 2) for (int y = 0; y < 5; y += 2) for (int x = 0; x < 5; x += 2) loop.setCooling(x, y, z, 0.05);
        run(loop, 30000);
        double produced = 0; for (int z = 0; z < 5; z += 2) for (int y = 0; y < 5; y += 2) for (int x = 0; x < 5; x += 2) produced += loop.fission(x, y, z) * p.heatPerFission();
        check("cooled: heat removed = heat produced", near(loop.heatRemoved(), produced, 0.02) && loop.meltedCells() == 0, loop.heatRemoved() + " vs " + produced + " maxT=" + loop.maxHeat());

        // Control rod motion
        double ins = 0; for (int t = 0; t < 50; t++) ins = ControlRodMotion.step(ins, 0);
        check("shaft stopped: rod drops to 1.0 in 50 ticks", ins == 1.0, "" + ins);
        check("hold band keeps position", ControlRodMotion.step(0.4, 20) == 0.4, "");
        ins = 1.0; for (int t = 0; t < 80; t++) ins = ControlRodMotion.step(ins, 64);
        check("64 rpm withdraws fully in 80 ticks", ins == 0.0, "" + ins);

        // Cascade: hand value alpha=1.5, 4 stages. R0 = 0.00711/0.99289; R4 = R0*5.0625
        double r0 = 0.00711 / 0.99289, r4 = r0 * Math.pow(1.5, 4), x4 = r4 / (1 + r4);
        check("cascade 4 stages at rated: ~3.5% U-235", near(Cascade.run(Cascade.NATURAL_U235, 4, 1.5), x4, 1e-9) && x4 > 0.034 && x4 < 0.036, "" + x4);
        double half = Cascade.alpha(128, 256, 1.5);
        check("half speed: ln(alpha) is a quarter", near(Math.log(half), 0.25 * Math.log(1.5), 1e-12), "" + half);
        System.out.println(fails == 0 ? "ALL PASS" : fails + " FAILED");
        System.exit(fails == 0 ? 0 : 1);
    }
}
