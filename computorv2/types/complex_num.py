from .rational import Rational


class Complex:
    def __init__(self, real, imag=None):
        if isinstance(real, Complex):
            self.real = real.real
            self.imag = real.imag
            return
        self.real = Rational(real) if not isinstance(real, Rational) else real
        if imag is None:
            self.imag = Rational(0)
        else:
            self.imag = Rational(imag) if not isinstance(imag, Rational) else imag

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        if isinstance(other, (Rational, int)):
            return Complex(self.real + other, self.imag)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (Rational, int)):
            return Complex(self.real + other, self.imag)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        if isinstance(other, (Rational, int)):
            return Complex(self.real - other, self.imag)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (Rational, int)):
            return Complex(other - self.real, -self.imag)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Complex):
            r = self.real * other.real - self.imag * other.imag
            i = self.real * other.imag + self.imag * other.real
            return Complex(r, i)
        if isinstance(other, (Rational, int)):
            return Complex(self.real * other, self.imag * other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (Rational, int)):
            return Complex(self.real * other, self.imag * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Complex):
            denom = other.real * other.real + other.imag * other.imag
            if denom.is_zero():
                raise ZeroDivisionError('complex division by zero')
            r = (self.real * other.real + self.imag * other.imag) / denom
            i = (self.imag * other.real - self.real * other.imag) / denom
            return Complex(r, i)
        if isinstance(other, (Rational, int)):
            if Rational(other).is_zero():
                raise ZeroDivisionError('complex division by zero')
            return Complex(self.real / other, self.imag / other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (Rational, int)):
            return Complex(other, 0) / self
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Complex):
            raise ValueError('Modulo not supported for complex numbers')
        if isinstance(other, (Rational, int)):
            raise ValueError('Modulo not supported for complex numbers')
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int):
            if other == 0:
                return Complex(1, 0)
            if other < 0:
                return Complex(1, 0) / (self ** (-other))
            result = Complex(1, 0)
            base = self
            exp = other
            while exp > 0:
                if exp & 1:
                    result = result * base
                base = base * base
                exp >>= 1
            return result
        if isinstance(other, Rational):
            if other.denominator == 1:
                return self ** other.numerator
        raise ValueError('Only integer powers supported for Complex')

    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __pos__(self):
        return Complex(self.real, self.imag)

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, (Rational, int)):
            return self.imag.is_zero() and self.real == other
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def norm(self):
        return (self.real * self.real + self.imag * self.imag).sqrt()

    def __abs__(self):
        return self.norm()

    def __repr__(self):
        if self.imag.is_zero():
            return str(self.real)
        if self.real.is_zero():
            if self.imag == Rational(1):
                return 'i'
            if self.imag == Rational(-1):
                return '-i'
            return f'{self.imag}i'
        imag_str = ''
        if self.imag == Rational(1):
            imag_str = '+ i'
        elif self.imag == Rational(-1):
            imag_str = '- i'
        elif self.imag > Rational(0):
            imag_str = f'+ {self.imag}i'
        else:
            imag_str = f'- {abs(self.imag)}i'
        return f'{self.real} {imag_str}'

    def __str__(self):
        return self.__repr__()

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def is_zero(self):
        return self.real.is_zero() and self.imag.is_zero()

    def is_real(self):
        return self.imag.is_zero()


class ZeroDivisionError(Exception):
    pass
