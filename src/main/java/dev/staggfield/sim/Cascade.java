package dev.staggfield.sim;

/**
 * Gas centrifuge cascade. Real law: per-stage separation factor alpha = exp(dm * v^2 / (2 R T)),
 * so ln(alpha) scales with the square of rim speed, and rim speed scales with rpm.
 * Each stage multiplies the abundance ratio R = x / (1 - x) by alpha.
 */
public final class Cascade {
    public static final double NATURAL_U235 = 0.00711;

    private Cascade() {}

    public static double alpha(double rpm, double ratedRpm, double alphaRated) {
        double f = Math.min(rpm / ratedRpm, 1.0);
        return Math.exp(Math.log(alphaRated) * f * f);
    }

    public static double stage(double x, double alpha) {
        double r = x / (1 - x) * alpha;
        return r / (1 + r);
    }

    public static double run(double x, int stages, double alpha) {
        for (int i = 0; i < stages; i++) x = stage(x, alpha);
        return x;
    }
}
