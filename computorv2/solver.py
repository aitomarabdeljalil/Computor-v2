from fractions import Fraction
from .types.rational import Rational
from .types.complex_num import Complex
import math


def solve_equation(expr_eval_fn):
    coeffs = _interpolate_coeffs(expr_eval_fn)
    a = coeffs[2]
    b = coeffs[1]
    c = coeffs[0]

    if abs(a) < 1e-12:
        if abs(b) < 1e-12:
            if abs(c) < 1e-12:
                return 'R', ['All real numbers']
            return 'R', []
        x = -c / b
        return 'R', [Rational(Fraction(x).limit_denominator(1000000))]

    disc = b * b - 4.0 * a * c

    if disc >= 0:
        sqrt_disc = math.sqrt(disc)
        x1 = (-b - sqrt_disc) / (2.0 * a)
        x2 = (-b + sqrt_disc) / (2.0 * a)
        sol1 = Rational(Fraction(x1).limit_denominator(1000000))
        sol2 = Rational(Fraction(x2).limit_denominator(1000000))
        if abs(x1 - x2) < 1e-12:
            return 'R', [sol1]
        return 'R', [sol1, sol2]
    else:
        sqrt_neg = math.sqrt(-disc)
        real_part = -b / (2.0 * a)
        imag_part = sqrt_neg / (2.0 * a)
        r = Rational(Fraction(real_part).limit_denominator(1000000))
        i = Rational(Fraction(imag_part).limit_denominator(1000000))
        c1 = Complex(r, i)
        c2 = Complex(r, -i)
        if abs(imag_part) < 1e-12:
            return 'R', [Rational(Fraction(real_part).limit_denominator(1000000))]
        return 'C', [c1, c2]


def _interpolate_coeffs(fn):
    ys = [float(fn(Rational(i))) for i in range(5)]
    a = (ys[2] - 2.0 * ys[1] + ys[0]) / 2.0
    b = ys[1] - ys[0] - a
    c = ys[0]
    return [c, b, a]
