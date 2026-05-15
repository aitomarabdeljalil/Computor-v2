from .types.rational import Rational
from .types.complex_num import Complex
from .types.matrix import Matrix
from .ast_nodes import FunctionDef


def print_value(value):
    if isinstance(value, FunctionDef):
        from .interpreter import Interpreter
        return print_expression(value.body)
    if isinstance(value, Rational):
        return format_rational(value)
    if isinstance(value, Complex):
        return str(value)
    if isinstance(value, Matrix):
        return str(value)
    return str(value)


def format_rational(r):
    if r.denominator == 1:
        return str(r.numerator)
    return f'{float(r):.10f}'.rstrip('0').rstrip('.')


def print_expression(node):
    if node is None:
        return ''
    from .ast_nodes import Number, Identifier, ImaginaryUnit, UnaryOp, BinaryOp, FunctionCall
    if isinstance(node, Number):
        return node.value
    if isinstance(node, Identifier):
        return node.name
    if isinstance(node, ImaginaryUnit):
        return 'i'
    if isinstance(node, UnaryOp):
        return f'{node.op}{print_expression(node.expr)}'
    if isinstance(node, BinaryOp):
        left = print_expression(node.left)
        right = print_expression(node.right)
        return f'{left} {node.op} {right}'
    if isinstance(node, FunctionCall):
        return f'{node.name}({print_expression(node.arg)})'
    return str(node)


def print_solutions(solutions, domain='R'):
    lines = []
    if len(solutions) == 0:
        lines.append('No solution in ' + domain)
    elif isinstance(solutions[0], str):
        lines.append(str(solutions[0]))
    elif len(solutions) == 1:
        lines.append('One solution in ' + domain + ':')
        lines.append(str(solutions[0]))
    else:
        lines.append('Two solutions in ' + domain + ':')
        for s in solutions:
            lines.append(str(s))
    return '\n'.join(lines)
