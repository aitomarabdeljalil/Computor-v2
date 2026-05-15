from .lexer import TokenType
from .ast_nodes import (
    Number, Identifier, ImaginaryUnit, UnaryOp, BinaryOp,
    MatrixLiteral, Assignment, FunctionDef, FunctionCall,
    Query, SolveQuery
)
from .exceptions import ParserError


PRECEDENCE = {
    '?': 0,
    '=': 1,
    '+': 2, '-': 2,
    '*': 3, '/': 3, '%': 3,
    '**': 4, '^': 4,
}

RIGHT_ASSOC = {'^', '**'}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, *types):
        tok = self.peek()
        if tok is None:
            expected = '/'.join(t.value if hasattr(t, 'value') else str(t) for t in types)
            raise ParserError(f'Expected {expected}, got EOF')
        if tok.type not in types:
            raise ParserError(f'Expected {tok.type.value}, got {tok.type.value} ({tok.value}) at {tok.pos}')
        return self.advance()

    def parse(self):
        if self.peek() is None or self.peek().type == TokenType.EOF:
            raise ParserError('Empty input')

        if self.peek().type == TokenType.QUESTION:
            self.advance()
            raise ParserError('Unexpected ?')

        if self._is_function_def():
            return self._parse_function_def()

        if self.peek().type == TokenType.IDENTIFIER:
            saved = self.pos
            try:
                if self._check_lookahead(1, TokenType.EQUALS):
                    name = self.advance().value
                    self.advance()
                    if self.peek() and self.peek().type == TokenType.QUESTION:
                        self.advance()
                        return Query(Identifier(name))
                    expr = self._parse_expr(0)
                    if self.peek() and self.peek().type == TokenType.QUESTION:
                        self.advance()
                        return SolveQuery(Identifier(name), expr)
                    return Assignment(name, expr)
            except ParserError:
                self.pos = saved

        left = self._parse_expr(0)

        if self.peek() and self.peek().type == TokenType.QUESTION:
            self.advance()
            return Query(left)

        if self.peek() and self.peek().type == TokenType.EQUALS:
            self.advance()
            tok = self.peek()
            if tok and tok.type == TokenType.QUESTION:
                self.advance()
                return Query(left)
            right = self._parse_expr(0)
            if self.peek() and self.peek().type == TokenType.QUESTION:
                self.advance()
                return SolveQuery(left, right)
            return BinaryOp(left, '=', right)

        return left

    def _is_function_def(self):
        if self.peek().type != TokenType.IDENTIFIER:
            return False
        if not self._check_lookahead(1, TokenType.LPAREN):
            return False
        scan = self.pos
        self.pos += 2
        result = False
        if (self.peek() and self.peek().type == TokenType.IDENTIFIER
                and self._check_lookahead(1, TokenType.RPAREN)
                and self._check_lookahead(2, TokenType.EQUALS)):
            result = True
        self.pos = scan
        return result

    def _check_lookahead(self, offset, expected_type):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx].type == expected_type
        return False

    def _parse_function_def(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        param = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.EQUALS)
        body = self._parse_expr(0)
        if self.peek() and self.peek().type == TokenType.QUESTION:
            self.advance()
            return SolveQuery(FunctionCall(name, Identifier(param)), body)
        return FunctionDef(name, param, body)

    def _parse_expr(self, min_prec):
        tok = self.peek()
        if tok is None:
            raise ParserError('Unexpected end of expression')

        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            operand = self._parse_expr(PRECEDENCE.get('*', 4))
            left = UnaryOp(op, operand)
        elif tok.type == TokenType.IMAGINARY:
            self.advance()
            left = ImaginaryUnit()
        elif tok.type == TokenType.NUMBER:
            val = self.advance().value
            left = Number(val)
            if self.peek() and self.peek().type == TokenType.IMAGINARY:
                self.advance()
                left = BinaryOp(left, '*', ImaginaryUnit())
        elif tok.type == TokenType.IDENTIFIER:
            name = self.advance().value
            if self.peek() and self.peek().type == TokenType.LPAREN:
                self.advance()
                arg = self._parse_expr(0)
                self.expect(TokenType.RPAREN)
                left = FunctionCall(name, arg)
            else:
                left = Identifier(name)
        elif tok.type == TokenType.LPAREN:
            self.advance()
            left = self._parse_expr(0)
            self.expect(TokenType.RPAREN)
        elif tok.type == TokenType.LBRACKET:
            left = self._parse_matrix()
        else:
            raise ParserError(f'Unexpected token {tok.type.value} ({tok.value})')

        while True:
            tok = self.peek()
            if tok is None or tok.type in (TokenType.EOF, TokenType.RPAREN,
                                           TokenType.RBRACKET, TokenType.COMMA,
                                           TokenType.SEMICOLON, TokenType.QUESTION,
                                           TokenType.EQUALS):
                break

            if tok.type in (TokenType.PLUS, TokenType.MINUS,
                            TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
                            TokenType.DOUBLESTAR, TokenType.POWER):
                op = self.advance().value
                prec = PRECEDENCE.get(op, 0)
                if prec < min_prec:
                    self.pos -= 1
                    break
                next_min = prec
                if op in RIGHT_ASSOC:
                    next_min = prec
                else:
                    next_min = prec + 1
                right = self._parse_expr(next_min)
                left = BinaryOp(left, op, right)
            else:
                break

        return left

    def _parse_matrix(self):
        self.expect(TokenType.LBRACKET)
        rows = []
        rows.append(self._parse_matrix_row())
        while self.peek() and self.peek().type == TokenType.SEMICOLON:
            self.advance()
            rows.append(self._parse_matrix_row())
        self.expect(TokenType.RBRACKET)
        return MatrixLiteral(rows)

    def _parse_matrix_row(self):
        self.expect(TokenType.LBRACKET)
        row = [self._parse_expr(0)]
        while self.peek() and self.peek().type == TokenType.COMMA:
            self.advance()
            row.append(self._parse_expr(0))
        self.expect(TokenType.RBRACKET)
        return row
