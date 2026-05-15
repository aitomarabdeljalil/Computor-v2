from fractions import Fraction
from .ast_nodes import (
    Number, Identifier, ImaginaryUnit, UnaryOp, BinaryOp,
    MatrixLiteral, Assignment, FunctionDef, FunctionCall,
    Query, SolveQuery
)
from .types.rational import Rational
from .types.complex_num import Complex
from .types.matrix import Matrix
from .environment import Environment
from .exceptions import RuntimeError_, TypeError_, NameError_, ZeroDivisionError_
from .printer import print_value
from .solver import solve_equation


class Interpreter:
    def __init__(self, env=None):
        self.env = env or Environment()

    def eval(self, node):
        if isinstance(node, Number):
            return Rational(node.value)
        if isinstance(node, Identifier):
            return self.env.get_variable(node.name)
        if isinstance(node, ImaginaryUnit):
            return Complex(Rational(0), Rational(1))
        if isinstance(node, UnaryOp):
            return self._eval_unary(node)
        if isinstance(node, BinaryOp):
            return self._eval_binary(node)
        if isinstance(node, MatrixLiteral):
            return self._eval_matrix(node)
        if isinstance(node, Assignment):
            return self._eval_assignment(node)
        if isinstance(node, FunctionDef):
            return self._eval_function_def(node)
        if isinstance(node, FunctionCall):
            return self._eval_function_call(node)
        if isinstance(node, Query):
            return self._eval_query(node)
        if isinstance(node, SolveQuery):
            return self._eval_solve_query(node)
        raise RuntimeError_(f'Unknown node type: {type(node).__name__}')

    def _eval_unary(self, node):
        val = self.eval(node.expr)
        if node.op == '+':
            return val
        if node.op == '-':
            return -val
        raise RuntimeError_(f'Unknown unary operator: {node.op}')

    def _eval_binary(self, node):
        left = self.eval(node.left)
        right = self.eval(node.right)

        if node.op == '+':
            return left + right
        if node.op == '-':
            return left - right
        if node.op == '*':
            return left * right
        if node.op == '/':
            try:
                return left / right
            except (ZeroDivisionError, ZeroDivisionError_) as e:
                raise ZeroDivisionError_(str(e))
        if node.op == '%':
            try:
                return left % right
            except (ZeroDivisionError, ZeroDivisionError_) as e:
                raise ZeroDivisionError_(str(e))
        if node.op == '**':
            if isinstance(left, Matrix) and isinstance(right, Matrix):
                return left.matrix_mul(right)
            if isinstance(left, Matrix):
                if isinstance(right, (Rational, int)):
                    return left ** int(right)
                return left.matrix_mul(right)
            return left ** right
        if node.op == '^':
            return left ** right
        if node.op == '=':
            if isinstance(node.left, Identifier) and not isinstance(right, FunctionDef):
                self.env.set_variable(node.left.name, right)
                return right
            raise RuntimeError_('Equation evaluation not supported for = operator')

        raise RuntimeError_(f'Unknown operator: {node.op}')

    def _eval_matrix(self, node):
        rows = []
        for row_nodes in node.rows:
            row = [self.eval(cell) for cell in row_nodes]
            rows.append(row)
        return Matrix(rows)

    def _eval_assignment(self, node):
        value = self.eval(node.expr)
        self.env.set_variable(node.name, value)
        return value

    def _eval_function_def(self, node):
        self.env.set_function(node.name, node)
        return node

    def _eval_function_call(self, node):
        func_def = self.env.get_function(node.name)
        arg_val = self.eval(node.arg)
        if isinstance(arg_val, (Rational, int)):
            substituted = self._substitute_var(func_def.body, Identifier(func_def.param), arg_val)
            return self.eval(substituted)
        raise TypeError_('Function argument must evaluate to a number')

    def _substitute_var(self, node, var_node, value):
        if isinstance(node, Number):
            return node
        if isinstance(node, Identifier):
            if node.name.lower() == var_node.name.lower():
                if isinstance(value, (Rational, int)):
                    if isinstance(value, int):
                        return Number(str(value))
                    if value.denominator == 1:
                        return Number(str(value.numerator))
                    return Number(str(float(value)))
                return value
            return node
        if isinstance(node, ImaginaryUnit):
            return node
        if isinstance(node, UnaryOp):
            return UnaryOp(node.op, self._substitute_var(node.expr, var_node, value))
        if isinstance(node, BinaryOp):
            return BinaryOp(
                self._substitute_var(node.left, var_node, value),
                node.op,
                self._substitute_var(node.right, var_node, value)
            )
        if isinstance(node, FunctionCall):
            return FunctionCall(node.name, self._substitute_var(node.arg, var_node, value))
        return node

    def _eval_query(self, node):
        if node.expr is None:
            return None
        val = self.eval(node.expr)
        return val

    def _eval_solve_query(self, node):
        func_body = self._get_function_body(node.expr)
        right_val = self._build_solve_term(node.value)

        eq_left_str = self._node_to_expr_str(func_body)
        eq_right_str = str(right_val) if isinstance(right_val, (Rational, int)) else self._node_to_expr_str(node.value)

        def combined_fn(x):
            substituted = self._substitute_var(func_body, self._get_param(node.expr), Rational(x))
            lv = self.eval(substituted)
            if callable(right_val):
                rv = right_val(x)
            elif isinstance(right_val, (Rational, int)):
                rv = Rational(right_val)
            else:
                rv = Rational(0)
            return lv - rv

        domain, solutions = solve_equation(combined_fn)
        return eq_left_str, eq_right_str, domain, solutions

    def _get_function_body(self, node):
        if isinstance(node, FunctionCall):
            func_def = self.env.get_function(node.name)
            return func_def.body
        raise RuntimeError_('Solve query requires a function call on the left side')

    def _get_param(self, node):
        if isinstance(node, FunctionCall):
            func_def = self.env.get_function(node.name)
            return Identifier(func_def.param)
        raise RuntimeError_('Solve query requires a function call on the left side')

    def _build_solve_term(self, node):
        if isinstance(node, (Number, Identifier, ImaginaryUnit, UnaryOp, BinaryOp, FunctionCall)):
            val = self.eval(node)
            if isinstance(val, (Rational, int)):
                return Rational(val)
        if isinstance(node, Number):
            return Rational(node.value)
        try:
            val = self.eval(node)
            if isinstance(val, (Rational, int, Complex)):
                return val
        except:
            pass
        return Rational(0)

    def _node_to_expr_str(self, node):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Identifier):
            return node.name
        if isinstance(node, ImaginaryUnit):
            return 'i'
        if isinstance(node, UnaryOp):
            return f'{node.op}{self._node_to_expr_str(node.expr)}'
        if isinstance(node, BinaryOp):
            return f'{self._node_to_expr_str(node.left)} {node.op} {self._node_to_expr_str(node.right)}'
        if isinstance(node, FunctionCall):
            return f'{node.name}({self._node_to_expr_str(node.arg)})'
        return str(node)
