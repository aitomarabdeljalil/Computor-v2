import math
from fractions import Fraction


class Rational:
    def __init__(self, value, denominator=None):
        if denominator is not None:
            if isinstance(value, Rational):
                value = value.numerator
            if isinstance(denominator, Rational):
                denominator = denominator.numerator
            self._frac = Fraction(int(value), int(denominator))
            return
        if isinstance(value, Rational):
            self._frac = value._frac
        elif isinstance(value, Fraction):
            self._frac = value
        elif isinstance(value, str):
            self._frac = Fraction(value)
        else:
            self._frac = Fraction(value)

    @property
    def numerator(self):
        return self._frac.numerator

    @property
    def denominator(self):
        return self._frac.denominator

    def __add__(self, other):
        if isinstance(other, Rational):
            return Rational(self._frac + other._frac)
        if isinstance(other, Fraction):
            return Rational(self._frac + other)
        if isinstance(other, int):
            return Rational(self._frac + other)
        if isinstance(other, float):
            return Rational(self._frac + Fraction.from_float(other))
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Rational):
            return Rational(self._frac - other._frac)
        if isinstance(other, Fraction):
            return Rational(self._frac - other)
        if isinstance(other, int):
            return Rational(self._frac - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return Rational(other - self._frac)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Rational):
            return Rational(self._frac * other._frac)
        if isinstance(other, Fraction):
            return Rational(self._frac * other)
        if isinstance(other, int):
            return Rational(self._frac * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Rational):
            if other._frac == 0:
                raise ZeroDivisionError('division by zero')
            return Rational(self._frac / other._frac)
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError('division by zero')
            return Rational(self._frac / other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, int):
            if self._frac == 0:
                raise ZeroDivisionError('division by zero')
            return Rational(other / self._frac)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Rational):
            if other._frac == 0:
                raise ZeroDivisionError('modulo by zero')
            return Rational(self._frac % other._frac)
        if isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError('modulo by zero')
            return Rational(self._frac % other)
        return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, int):
            if self._frac == 0:
                raise ZeroDivisionError('modulo by zero')
            return Rational(other % self._frac)
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, Rational):
            if other.denominator == 1:
                exp = other.numerator
                if exp >= 0:
                    return Rational(self._frac ** exp)
                else:
                    return Rational(self._frac ** exp)
            raise ValueError('Only integer powers supported for Rational')
        if isinstance(other, int):
            if other >= 0:
                return Rational(self._frac ** other)
            else:
                return Rational(self._frac ** other)
        return NotImplemented

    def __neg__(self):
        return Rational(-self._frac)

    def __pos__(self):
        return Rational(self._frac)

    def __abs__(self):
        return Rational(abs(self._frac))

    def __eq__(self, other):
        if isinstance(other, Rational):
            return self._frac == other._frac
        if isinstance(other, int):
            return self._frac == other
        if isinstance(other, float):
            return float(self._frac) == other
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        if isinstance(other, Rational):
            return self._frac < other._frac
        if isinstance(other, int):
            return self._frac < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Rational):
            return self._frac <= other._frac
        if isinstance(other, int):
            return self._frac <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Rational):
            return self._frac > other._frac
        if isinstance(other, int):
            return self._frac > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Rational):
            return self._frac >= other._frac
        if isinstance(other, int):
            return self._frac >= other
        return NotImplemented

    def __float__(self):
        return float(self._frac)

    def __int__(self):
        return int(self._frac)

    def __hash__(self):
        return hash(self._frac)

    def __repr__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f'{self.numerator}/{self.denominator}'

    def __str__(self):
        if self.denominator == 1:
            if self.numerator == 0:
                return '0'
            return str(self.numerator)
        if self.denominator < 0:
            return f'{-self.numerator}/{-self.denominator}'
        return f'{self.numerator}/{self.denominator}'

    def is_zero(self):
        return self._frac == 0

    def is_one(self):
        return self._frac == 1

    def sqrt(self):
        if self._frac < 0:
            raise ValueError('Cannot take sqrt of negative rational without complex')
        num = self.numerator
        den = self.denominator
        num_sqrt = math.isqrt(num)
        den_sqrt = math.isqrt(den)
        if num_sqrt * num_sqrt == num and den_sqrt * den_sqrt == den:
            return Rational(Fraction(num_sqrt, den_sqrt))
        return Rational(Fraction(int(math.isqrt(num * den)), den))

    def to_decimal_str(self, precision=10):
        return format(float(self._frac), f'.{precision}f').rstrip('0').rstrip('.')


class ZeroDivisionError(Exception):
    pass
