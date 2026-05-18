import math
from fractions import Fraction
from .rational import Rational
from .complex_num import Complex, ZeroDivisionError as ComplexZeroDiv


class Matrix:
    def __init__(self, data):
        if isinstance(data, Matrix):
            self.data = [row[:] for row in data.data]
            self.rows = data.rows
            self.cols = data.cols
            return
        if not data or not data[0]:
            raise ValueError('Matrix must be non-empty')
        self.rows = len(data)
        self.cols = len(data[0])
        for row in data:
            if len(row) != self.cols:
                raise ValueError('All rows must have the same length')
        self.data = []
        for row in data:
            new_row = []
            for elem in row:
                if isinstance(elem, Complex):
                    new_row.append(elem)
                elif isinstance(elem, Rational):
                    new_row.append(Complex(elem, Rational(0)))
                elif isinstance(elem, int):
                    new_row.append(Complex(Rational(elem), Rational(0)))
                elif isinstance(elem, float):
                    new_row.append(Complex(Rational(elem), Rational(0)))
                else:
                    new_row.append(elem)
            self.data.append(new_row)

    def _check_dimensions(self, other, op_name):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f'Matrix dimensions mismatch for {op_name}: ({self.rows}x{self.cols}) vs ({other.rows}x{other.cols})')

    def __add__(self, other):
        if isinstance(other, Matrix):
            self._check_dimensions(other, 'addition')
            result = []
            for i in range(self.rows):
                row = [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                result.append(row)
            return Matrix(result)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Matrix):
            self._check_dimensions(other, 'subtraction')
            result = []
            for i in range(self.rows):
                row = [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
                result.append(row)
            return Matrix(result)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Matrix):
            self._check_dimensions(other, 'term-by-term multiplication')
            result = []
            for i in range(self.rows):
                row = [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
                result.append(row)
            return Matrix(result)
        if isinstance(other, (Rational, int, Complex)):
            result = []
            for i in range(self.rows):
                row = [self.data[i][j] * other for j in range(self.cols)]
                result.append(row)
            return Matrix(result)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (Rational, int, Complex)):
            result = []
            for i in range(self.rows):
                row = [other * self.data[i][j] for j in range(self.cols)]
                result.append(row)
            return Matrix(result)
        return NotImplemented

    def __matmul__(self, other):
        return self.matrix_mul(other)

    def matrix_mul(self, other):
        if not isinstance(other, Matrix):
            raise ValueError('Matrix multiplication requires Matrix operand')
        if self.cols != other.rows:
            raise ValueError(f'Matrix multiplication dimension mismatch: ({self.rows}x{self.cols}) x ({other.rows}x{other.cols})')
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                total = Complex(Rational(0), Rational(0))
                for k in range(self.cols):
                    total = total + self.data[i][k] * other.data[k][j]
                row.append(total)
            result.append(row)
        return Matrix(result)

    def __pow__(self, other):
        if isinstance(other, int):
            if not self.is_square():
                raise ValueError('Only square matrices can be raised to a power')
            if other == -1:
                return self.inverse()
            if other < 0:
                raise ValueError('Only -1 (inverse) is supported for negative powers')
            if other == 0:
                return self._identity()
            result = self
            for _ in range(1, other):
                result = result.matrix_mul(self)
            return result
        if isinstance(other, Rational):
            if other.denominator == 1:
                return self ** other.numerator
        raise ValueError('Only integer powers supported for matrices')

    def __neg__(self):
        result = [[-elem for elem in row] for row in self.data]
        return Matrix(result)

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    def __repr__(self):
        lines = []
        for row in self.data:
            elems = ', '.join(str(e) for e in row)
            lines.append(f'[ {elems} ]')
        return '\n'.join(lines)

    def is_square(self):
        return self.rows == self.cols

    def _identity(self):
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(Complex(Rational(1 if i == j else 0), Rational(0)))
            result.append(row)
        return Matrix(result)

    def norm(self):
        total = Rational(0)
        for row in self.data:
            for elem in row:
                total = total + elem.real * elem.real + elem.imag * elem.imag
        f = math.sqrt(float(total))
        return Rational(Fraction(f).limit_denominator(1000000))

    def _minor(self, row, col):
        data = []
        for i in range(self.rows):
            if i == row:
                continue
            new_row = []
            for j in range(self.cols):
                if j == col:
                    continue
                new_row.append(self.data[i][j])
            data.append(new_row)
        return Matrix(data)

    def determinant(self):
        if not self.is_square():
            raise ValueError('Determinant is only defined for square matrices')
        n = self.rows
        if n == 1:
            return self.data[0][0]
        if n == 2:
            return (self.data[0][0] * self.data[1][1]
                    - self.data[0][1] * self.data[1][0])
        if n == 3:
            a, b, c = self.data[0]
            d, e, f = self.data[1]
            g, h, i = self.data[2]
            return (a * (e * i - f * h)
                    - b * (d * i - f * g)
                    + c * (d * h - e * g))
        return self._laplace_det()

    def _laplace_det(self):
        total = Complex(Rational(0), Rational(0))
        for j in range(self.cols):
            sign = Complex(Rational(1), Rational(0)) if j % 2 == 0 else Complex(Rational(-1), Rational(0))
            total = total + sign * self.data[0][j] * self._minor(0, j).determinant()
        return total

    def _cofactor(self, i, j):
        det = self._minor(i, j).determinant()
        if (i + j) % 2 == 1:
            return -det
        return det

    def adjugate(self):
        n = self.rows
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(self._cofactor(j, i))
            result.append(row)
        return Matrix(result)

    def inverse(self):
        if not self.is_square():
            raise ValueError('Inverse is only defined for square matrices')
        det = self.determinant()
        if det.is_zero():
            raise ValueError('Matrix is singular (determinant is zero) — no inverse exists')
        if self.rows == 1:
            inv = Complex(Rational(1), Rational(0)) / self.data[0][0]
            return Matrix([[inv]])
        return self.adjugate() * (Complex(Rational(1), Rational(0)) / det)

    def transpose(self):
        result = []
        for j in range(self.cols):
            row = [self.data[i][j] for i in range(self.rows)]
            result.append(row)
        return Matrix(result)
