from computorv2.lexer import Lexer
from parser import Parser
from computorv2.ast_nodes import *


def parse(text):
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def test(desc, text, expected_type):
    try:
        ast = parse(text)
        ok = isinstance(ast, expected_type)
        status = 'PASS' if ok else 'FAIL'
        print(f'{status}: {desc} -> {type(ast).__name__}')
        if not ok:
            print(f'  Expected {expected_type.__name__}, got {type(ast).__name__}: {ast}')
    except Exception as e:
        print(f'FAIL: {desc} -> {type(e).__name__}: {e}')


test('number', '42', Number)
test('variable assignment', 'x = 2', Assignment)
test('variable assignment (string)', 'varA = 2', Assignment)
test('re-assignment', 'y = x', Assignment)
test('re-assignment numeric', 'y = 7', Assignment)
test('complex assignment', 'y = 2 * i - 4', Assignment)
test('complex expr', '2 * i + 3', BinaryOp)
test('imaginary alone', 'i', ImaginaryUnit)
test('negative imaginary', '-4i', UnaryOp)
test('matrix literal', '[[2,3];[4,3]]', MatrixLiteral)
test('single row matrix', '[[3,4]]', MatrixLiteral)
test('function def', 'funA(x) = 2*x^5 + 4*x^2 - 5*x + 4', FunctionDef)
test('function def simple', 'funA(b) = 2*b+b', FunctionDef)
test('function call', 'funA(2)', FunctionCall)
test('query', 'a + 2 = ?', Query)
test('var query', 'varA = ?', Query)
test('expression with parens', '2 + 4 * 2 - 5 % 4 + 2 * (4 + 5)', BinaryOp)
test('complex expression', '2 * varA - 5 % 4', BinaryOp)
test('function call query', 'funA(2) + funB(4) = ?', Query)
test('solve query', 'funA(x) = y ?', SolveQuery)
test('matrix assignment', 'matA = [[1,2];[3,2];[3,4]]', Assignment)
test('double star', '2 ** 3', BinaryOp)

print('\nDone!')
