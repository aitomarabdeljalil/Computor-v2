from computorv2.repl import REPL
from computorv2.lexer import Lexer
from parser import Parser
from computorv2.types.rational import Rational
from computorv2.types.complex_num import Complex
from computorv2.types.matrix import Matrix
from computorv2.printer import print_value, print_solutions


def test(desc, text, expected_str):
    repl = REPL()
    lines = text.strip().split('\n')
    outputs = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            result = repl.interp.eval(ast)
            if result is None:
                val_str = ''
            elif isinstance(result, tuple) and len(result) == 4:
                eq_left, eq_right, domain, solutions = result
                val_str = f'{eq_left} = {eq_right}\n{print_solutions(solutions, domain)}'
            else:
                val_str = print_value(result)
            outputs.append(val_str)
        except Exception as e:
            import traceback
            outputs.append(f'ERROR: {e}\n{traceback.format_exc()}')
    full_output = '\n'.join(outputs)
    if expected_str in full_output:
        print(f'PASS: {desc}')
    else:
        print(f'FAIL: {desc}')
        print(f'  Expected to contain: {expected_str!r}')
        print(f'  Got: {full_output!r}')


test('basic arithmetic', '2 + 3 * 4', '14')

test('modulo', '10 % 3', '1')

test('parens', '(2 + 3) * 4', '20')

test('variable lookup', 'x = 5\nx = ?', '5')

test('complex arithmetic', '(2 + 3*i) + (1 - i)', '3 + 2i')

test('complex multiply', '(1 + i) * (1 - i)', '2')

test('matrix add', 'm = [[1,2];[3,4]]\nn = [[5,6];[7,8]]\nm + n', '[ 6, 8 ]\n[ 10, 12 ]')

test('matrix scalar mult', 'm = [[1,2];[3,4]]\n2 * m', '[ 2, 4 ]\n[ 6, 8 ]')

test('matrix mul **', 'm = [[1,2];[3,4]]\nn = [[2,0];[1,2]]\nm ** n', '[ 4, 4 ]\n[ 10, 8 ]')

test('function def', 'funA(x) = x + 1', 'x + 1')

test('function call', 'funA(x) = x + 1\nfunA(5)', '6')

test('query', 'funA(x) = x^2 + 2*x + 1\nfunA(2) = ?', '9')

test('solve degree 1', 'funA(x) = 2*x + 1\nfunA(x) = 0 ?', 'One solution in R:\n-1/2')

test('solve degree 2 real', 'funA(x) = x^2 - 3*x + 2\nfunA(x) = 0 ?', 'Two solutions in R:')

print('\nDone!')
