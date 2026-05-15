class Node:
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Number({self.value})'

class Identifier(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Identifier({self.name})'

class ImaginaryUnit(Node):
    def __repr__(self):
        return 'ImaginaryUnit()'

class UnaryOp(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f'UnaryOp({self.op}, {self.expr})'

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinaryOp({self.left}, {self.op}, {self.right})'

class MatrixLiteral(Node):
    def __init__(self, rows):
        self.rows = rows

    def __repr__(self):
        return f'MatrixLiteral({self.rows})'

class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f'Assignment({self.name}, {self.expr})'

class FunctionDef(Node):
    def __init__(self, name, param, body):
        self.name = name
        self.param = param
        self.body = body

    def __repr__(self):
        return f'FunctionDef({self.name}, {self.param}, {self.body})'

class FunctionCall(Node):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def __repr__(self):
        return f'FunctionCall({self.name}, {self.arg})'

class Query(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f'Query({self.expr})'

class SolveQuery(Node):
    def __init__(self, expr, value):
        self.expr = expr
        self.value = value

    def __repr__(self):
        return f'SolveQuery({self.expr}, {self.value})'
