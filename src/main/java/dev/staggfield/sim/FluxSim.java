package dev.staggfield.sim;

import java.util.Arrays;

/**
 * Neutron flux and heat model for a rod lattice. No Minecraft imports, so it runs in plain unit tests.
 * Rays travel along the six axes through solid lattice cells only; an air gap stops them.
 * A ray that reaches a fuel cell d cells away delivers strength * eff(d); eff peaks at `optimum`
 * (too close: neutrons still fast, too far: leaked). Fission follows flux with a first-order lag
 * (`response`), which stands in for delayed neutrons.
 */
public final class FluxSim {
    public enum Cell { AIR, GRAPHITE, FUEL, SOURCE, ABSORBER }

    public record Params(int range, double optimum, double width, double nu, double sigma, double response,
                         double heatPerFission, double doppler, double passiveCool, double ambient,
                         double meltdown, double burnPerFission, double sourceFlux,
                         double decayShare, double decayRate) {
        /** sigma chosen so a natural-uranium rod (richness 1) gives k_inf = nu * sigma = 1.6 in a full lattice. */
        public static Params defaults() {
            return new Params(4, 2.0, 1.0, 2.4, 1.6 / 2.4, 0.02, 1.0, 0.5, 0.003, 20.0, 1200.0, 2e-6, 1.0, 0.07, 0.0005);
        }
    }

    private static final int[][] DIRS = {{1, 0, 0}, {-1, 0, 0}, {0, 1, 0}, {0, -1, 0}, {0, 0, 1}, {0, 0, -1}};

    private final int nx, ny, nz;
    private final Params p;
    private final Cell[] type;
    private final double[] richness, fission, fluxIn, heat, depletion, insertion, cooling, decay;
    private double heatRemoved;
    private int melted;

    public FluxSim(int nx, int ny, int nz, Params p) {
        this.nx = nx; this.ny = ny; this.nz = nz; this.p = p;
        int n = nx * ny * nz;
        type = new Cell[n]; Arrays.fill(type, Cell.AIR);
        richness = new double[n]; fission = new double[n]; fluxIn = new double[n];
        heat = new double[n]; Arrays.fill(heat, p.ambient());
        depletion = new double[n]; insertion = new double[n]; decay = new double[n];
        cooling = new double[n]; Arrays.fill(cooling, p.passiveCool());
    }

    private int idx(int x, int y, int z) { return x + nx * (y + ny * z); }

    public void set(int x, int y, int z, Cell c) { type[idx(x, y, z)] = c; }
    public void setFuel(int x, int y, int z, double richness) { int i = idx(x, y, z); type[i] = Cell.FUEL; this.richness[i] = richness; }
    public void setInsertion(int x, int y, int z, double v) { insertion[idx(x, y, z)] = Math.max(0, Math.min(1, v)); }
    public void setCooling(int x, int y, int z, double c) { cooling[idx(x, y, z)] = c; }

    public double fission(int x, int y, int z) { return fission[idx(x, y, z)]; }
    public double heat(int x, int y, int z) { return heat[idx(x, y, z)]; }
    public double depletion(int x, int y, int z) { return depletion[idx(x, y, z)]; }
    public double totalFission() { double s = 0; for (double f : fission) s += f; return s; }
    public double maxHeat() { double m = p.ambient(); for (double h : heat) m = Math.max(m, h); return m; }
    /** Heat carried away by coolant this tick: this is what a boiler or heat exchanger receives. */
    public double heatRemoved() { return heatRemoved; }
    public int meltedCells() { return melted; }

    public double eff(int d) { double z = (d - p.optimum()) / p.width(); return Math.exp(-0.5 * z * z); }

    public void tick() {
        Arrays.fill(fluxIn, 0);
        for (int z = 0; z < nz; z++) for (int y = 0; y < ny; y++) for (int x = 0; x < nx; x++) {
            int i = idx(x, y, z);
            double emission = switch (type[i]) {
                case SOURCE -> p.sourceFlux();
                case FUEL -> fission[i] * p.nu();
                default -> 0;
            };
            if (emission > 0) trace(x, y, z, emission / 6.0);
        }
        heatRemoved = 0;
        double span = p.meltdown() - p.ambient();
        for (int i = 0; i < type.length; i++) {
            if (type[i] != Cell.FUEL) continue;
            double react = richness[i] * (1 - depletion[i]) * Math.max(0, 1 - p.doppler() * (heat[i] - p.ambient()) / span);
            double target = p.sigma() * react * fluxIn[i];
            fission[i] += (target - fission[i]) * p.response();
            // Fission products keep releasing heat after the chain reaction stops: why a scram is not the end of cooling.
            double released = decay[i] * p.decayRate();
            decay[i] += fission[i] * p.heatPerFission() * p.decayShare() - released;
            heat[i] += fission[i] * p.heatPerFission() * (1 - p.decayShare()) + released;
            depletion[i] = Math.min(1, depletion[i] + fission[i] * p.burnPerFission());
            double q = cooling[i] * (heat[i] - p.ambient());
            heat[i] -= q; heatRemoved += q;
            if (heat[i] >= p.meltdown()) { type[i] = Cell.AIR; fission[i] = 0; melted++; }
        }
    }

    private void trace(int x, int y, int z, double strength) {
        for (int[] dir : DIRS) {
            double s = strength;
            for (int d = 1; d <= p.range(); d++) {
                int cx = x + dir[0] * d, cy = y + dir[1] * d, cz = z + dir[2] * d;
                if (cx < 0 || cy < 0 || cz < 0 || cx >= nx || cy >= ny || cz >= nz) break;
                int c = idx(cx, cy, cz);
                if (type[c] == Cell.AIR || type[c] == Cell.SOURCE) break;
                if (type[c] == Cell.ABSORBER) s *= 1 - insertion[c];
                else if (type[c] == Cell.FUEL) { fluxIn[c] += s * eff(d); break; }
            }
        }
    }
}
