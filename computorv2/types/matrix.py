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
            if other < 0:
                raise ValueError('Negative powers not supported for matrices')
            if other == 0:
                return self._identity()
            result = self
            for _ in range(1, other):
                result = result.matrix_mul(self)
            return result
        if isinstance(other, Rational):
            if other.denominator == 1:
                return self ** other.numerator
        raise ValueError('Only non-negative integer powers supported for matrices')

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

    def transpose(self):
        result = []
        for j in range(self.cols):
            row = [self.data[i][j] for i in range(self.rows)]
            result.append(row)
        return Matrix(result)
