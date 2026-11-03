package dev.staggfield.sim;

/**
 * Control rod actuator driven by shaft speed. The rod is held up only while the shaft turns:
 * stop the shaft (or overstress the network) and gravity drops the rod, which is a fail-safe scram.
 * Bands: |rpm| < HOLD_RPM falls, HOLD_RPM..MOVE_RPM holds position, >= MOVE_RPM moves (sign sets direction).
 */
public final class ControlRodMotion {
    public static final double HOLD_RPM = 16, MOVE_RPM = 32, DROP_PER_TICK = 0.02, TRAVEL_PER_RPM = 0.0002;

    private ControlRodMotion() {}

    /** @return new insertion, 0 = fully withdrawn, 1 = fully inserted. Positive rpm withdraws. */
    public static double step(double insertion, double rpm) {
        double a = Math.abs(rpm);
        if (a < HOLD_RPM) return Math.min(1, insertion + DROP_PER_TICK);
        if (a < MOVE_RPM) return insertion;
        double next = insertion - Math.signum(rpm) * a * TRAVEL_PER_RPM;
        return Math.max(0, Math.min(1, next));
    }
}
