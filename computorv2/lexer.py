from enum import Enum, auto


class TokenType(Enum):
    NUMBER = 'NUMBER'
    IMAGINARY = 'IMAGINARY'
    IDENTIFIER = 'IDENTIFIER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    DOUBLESTAR = 'DOUBLESTAR'
    SLASH = 'SLASH'
    PERCENT = 'PERCENT'
    POWER = 'POWER'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    SEMICOLON = 'SEMICOLON'
    COMMA = 'COMMA'
    EQUALS = 'EQUALS'
    QUESTION = 'QUESTION'
    PIPE = 'PIPE'
    AT = 'AT'
    EOF = 'EOF'


class Token:
    __slots__ = ('type', 'value', 'pos')

    def __init__(self, type_, value, pos):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, {self.pos})'


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def error(self, msg):
        raise LexerError(f'{msg} at line {self.line}, col {self.col}')

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.text):
            return self.text[idx]
        return '\0'

    def advance(self):
        ch = self.text[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.text) and self.peek() in ' \t\r\n':
            self.advance()

    def read_number(self):
        start = self.pos
        has_dot = False
        while self.pos < len(self.text) and (self.peek().isdigit() or (self.peek() == '.' and not has_dot)):
            if self.peek() == '.':
                has_dot = True
            self.advance()
        return self.text[start:self.pos]

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (self.peek().isalnum()):
            self.advance()
        return self.text[start:self.pos]

    def get_next_token(self):
        self.skip_whitespace()

        if self.pos >= len(self.text):
            return Token(TokenType.EOF, None, (self.line, self.col))

        ch = self.peek()

        if ch.isdigit() or ch == '.':
            num = self.read_number()
            if ch == '.' and num == '.':
                self.error('Unexpected decimal point')
            return Token(TokenType.NUMBER, num, (self.line, self.col))

        if ch.isalpha():
            ident = self.read_identifier()
            if ident == 'i':
                return Token(TokenType.IMAGINARY, ident, (self.line, self.col))
            return Token(TokenType.IDENTIFIER, ident, (self.line, self.col))

        if ch == '+':
            self.advance()
            return Token(TokenType.PLUS, '+', (self.line, self.col - 1))

        if ch == '-':
            self.advance()
            return Token(TokenType.MINUS, '-', (self.line, self.col - 1))

        if ch == '*':
            self.advance()
            if self.peek() == '*':
                self.advance()
                return Token(TokenType.DOUBLESTAR, '**', (self.line, self.col - 2))
            return Token(TokenType.STAR, '*', (self.line, self.col - 1))

        if ch == '/':
            self.advance()
            return Token(TokenType.SLASH, '/', (self.line, self.col - 1))

        if ch == '%':
            self.advance()
            return Token(TokenType.PERCENT, '%', (self.line, self.col - 1))

        if ch == '^':
            self.advance()
            return Token(TokenType.POWER, '^', (self.line, self.col - 1))

        if ch == '(':
            self.advance()
            return Token(TokenType.LPAREN, '(', (self.line, self.col - 1))

        if ch == ')':
            self.advance()
            return Token(TokenType.RPAREN, ')', (self.line, self.col - 1))

        if ch == '[':
            self.advance()
            return Token(TokenType.LBRACKET, '[', (self.line, self.col - 1))

        if ch == ']':
            self.advance()
            return Token(TokenType.RBRACKET, ']', (self.line, self.col - 1))

        if ch == ';':
            self.advance()
            return Token(TokenType.SEMICOLON, ';', (self.line, self.col - 1))

        if ch == ',':
            self.advance()
            return Token(TokenType.COMMA, ',', (self.line, self.col - 1))

        if ch == '=':
            self.advance()
            return Token(TokenType.EQUALS, '=', (self.line, self.col - 1))

        if ch == '?':
            self.advance()
            return Token(TokenType.QUESTION, '?', (self.line, self.col - 1))

        if ch == '|':
            self.advance()
            return Token(TokenType.PIPE, '|', (self.line, self.col - 1))

        if ch == '@':
            self.advance()
            return Token(TokenType.AT, '@', (self.line, self.col - 1))

        self.error(f'Unexpected character {ch!r}')

    def tokenize(self):
        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens
