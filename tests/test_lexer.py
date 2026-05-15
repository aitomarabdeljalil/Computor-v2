from computorv2.lexer import Lexer, TokenType


def test(input_str, expected):
    lexer = Lexer(input_str)
    tokens = lexer.tokenize()
    types = [t.type for t in tokens[:-1]]
    if types != expected:
        print(f'FAIL: {input_str!r}')
        print(f'  Expected: {expected}')
        print(f'  Got:      {types}')
        return False
    print(f'PASS: {input_str!r} -> {types}')
    return True


tests = [
    ('2', [TokenType.NUMBER]),
    ('4.242', [TokenType.NUMBER]),
    ('-4.3', [TokenType.MINUS, TokenType.NUMBER]),
    ('2*i + 3', [TokenType.NUMBER, TokenType.STAR, TokenType.IMAGINARY, TokenType.PLUS, TokenType.NUMBER]),
    ('-4i - 4', [TokenType.MINUS, TokenType.NUMBER, TokenType.IMAGINARY, TokenType.MINUS, TokenType.NUMBER]),
    ('[[2,3];[4,3]]', [TokenType.LBRACKET, TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA,
                       TokenType.NUMBER, TokenType.RBRACKET, TokenType.SEMICOLON,
                       TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA,
                       TokenType.NUMBER, TokenType.RBRACKET, TokenType.RBRACKET]),
    ('[[3,4]]', [TokenType.LBRACKET, TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA,
                 TokenType.NUMBER, TokenType.RBRACKET, TokenType.RBRACKET]),
    ('varA = 2', [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.NUMBER]),
    ('y = x', [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.IDENTIFIER]),
    ('y = 7', [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.NUMBER]),
    ('y = 2 * i - 4', [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.NUMBER,
                       TokenType.STAR, TokenType.IMAGINARY, TokenType.MINUS, TokenType.NUMBER]),
    ('2 + 4 * 2 - 5 % 4 + 2 * (4 + 5)', [
        TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.STAR, TokenType.NUMBER,
        TokenType.MINUS, TokenType.NUMBER, TokenType.PERCENT, TokenType.NUMBER,
        TokenType.PLUS, TokenType.NUMBER, TokenType.STAR, TokenType.LPAREN,
        TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.RPAREN
    ]),
    ('funA(x) = 2*x^5 + 4*x^2 - 5*x + 4', [
        TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.IDENTIFIER, TokenType.RPAREN,
        TokenType.EQUALS, TokenType.NUMBER, TokenType.STAR, TokenType.IDENTIFIER,
        TokenType.POWER, TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER,
        TokenType.STAR, TokenType.IDENTIFIER, TokenType.POWER, TokenType.NUMBER,
        TokenType.MINUS, TokenType.NUMBER, TokenType.STAR, TokenType.IDENTIFIER,
        TokenType.PLUS, TokenType.NUMBER
    ]),
    ('a + 2 = ?', [TokenType.IDENTIFIER, TokenType.PLUS, TokenType.NUMBER,
                   TokenType.EQUALS, TokenType.QUESTION]),
    ('varA = ?', [TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.QUESTION]),
    ('varB = 2 * varA - 5 % 4', [TokenType.IDENTIFIER, TokenType.EQUALS,
                                 TokenType.NUMBER, TokenType.STAR, TokenType.IDENTIFIER,
                                 TokenType.MINUS, TokenType.NUMBER, TokenType.PERCENT, TokenType.NUMBER]),
    ('funA(2) + funB(4) = ?', [
        TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.NUMBER, TokenType.RPAREN,
        TokenType.PLUS, TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.NUMBER,
        TokenType.RPAREN, TokenType.EQUALS, TokenType.QUESTION
    ]),
    ('funA(x) = y ?', [TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.IDENTIFIER,
                       TokenType.RPAREN, TokenType.EQUALS, TokenType.IDENTIFIER,
                       TokenType.QUESTION]),
    ('funA(b) = 2*b+b', [TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.IDENTIFIER,
                         TokenType.RPAREN, TokenType.EQUALS, TokenType.NUMBER,
                         TokenType.STAR, TokenType.IDENTIFIER, TokenType.PLUS,
                         TokenType.IDENTIFIER]),
    ('varB= 2 * (4 + varA + 3)', [TokenType.IDENTIFIER, TokenType.EQUALS,
                                  TokenType.NUMBER, TokenType.STAR, TokenType.LPAREN,
                                  TokenType.NUMBER, TokenType.PLUS, TokenType.IDENTIFIER,
                                  TokenType.PLUS, TokenType.NUMBER, TokenType.RPAREN]),
    ('varC =2 * varB', [TokenType.IDENTIFIER, TokenType.EQUALS,
                        TokenType.NUMBER, TokenType.STAR, TokenType.IDENTIFIER]),
    ('varD = 2 *(2 + 4 *varC -4 /3)', [
        TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.NUMBER, TokenType.STAR,
        TokenType.LPAREN, TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER,
        TokenType.STAR, TokenType.IDENTIFIER, TokenType.MINUS, TokenType.NUMBER,
        TokenType.SLASH, TokenType.NUMBER, TokenType.RPAREN
    ]),
    ('funD(x) = 2 *x', [TokenType.IDENTIFIER, TokenType.LPAREN, TokenType.IDENTIFIER,
                        TokenType.RPAREN, TokenType.EQUALS, TokenType.NUMBER,
                        TokenType.STAR, TokenType.IDENTIFIER]),
    ('matB= [[1,2]]', [TokenType.IDENTIFIER, TokenType.EQUALS,
                       TokenType.LBRACKET, TokenType.LBRACKET,
                       TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER,
                       TokenType.RBRACKET, TokenType.RBRACKET]),
    ('2**3', [TokenType.NUMBER, TokenType.DOUBLESTAR, TokenType.NUMBER]),
]


if __name__ == '__main__':
    failures = 0
    for input_str, expected in tests:
        if not test(input_str, expected):
            failures += 1
    print(f'\n{len(tests) - failures}/{len(tests)} tests passed')
    if failures:
        print(f'{failures} tests FAILED')
    else:
        print('All tests passed!')
