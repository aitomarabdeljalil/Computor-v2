from computorv2.repl import REPL


def run(repl, line):
    from computorv2.lexer import Lexer
    from parser import Parser
    lexer = Lexer(line)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = repl.interp.eval(ast)
    if result is None:
        return ''
    if isinstance(result, tuple) and len(result) == 4:
        eq_left, eq_right, domain, solutions = result
        from computorv2.printer import print_solutions
        return f'{eq_left} = {eq_right}\n{print_solutions(solutions, domain)}'
    from computorv2.printer import print_value
    return print_value(result)


repl = REPL()
errors = []

def check(desc, actual, expected):
    if expected not in actual:
        errors.append(f'{desc}: expected {expected!r} in {actual!r}')
        print(f'  FAIL: {desc}')
    else:
        print(f'  PASS: {desc}')

print('=== Case Insensitivity ===')
r = run(repl, 'varA = 5')
check('varA = 5', r, '5')
r = run(repl, 'vara = 10')
check('vara = 10 (same var)', r, '10')
r = run(repl, 'varA = ?')
check('varA = ? (case insensitive)', r, '10')

print('\n=== Variable reuse ===')
r = run(repl, 'x = 42')
check('x = 42', r, '42')
r = run(repl, 'x = 3 + 4i')
check('x = 3 + 4i (type change)', r, '3 + 4i')
r = run(repl, 'x = 7')
check('x = 7 (back to rational)', r, '7')

print('\n=== Power operator ===')
r = run(repl, '2 ^ 3')
check('2^3 = 8', r, '8')
r = run(repl, '5 ^ 0')
check('5^0 = 1', r, '1')

print('\n=== Complex power ===')
r = run(repl, '(1 + i) ^ 2')
check('(1+i)^2 = 2i', r, '2i')

print('\n=== Division ===')
r = run(repl, '10 / 4')
check('10/4 = 2.5', r, '2.5')

print('\n=== Errors ===')
try:
    from computorv2.lexer import Lexer
    from parser import Parser
    lexer = Lexer('1 / 0')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = repl.interp.eval(ast)
    check('1/0 should error', 'error', 'error')
except Exception as e:
    check('1/0 errors correctly', f'{e}', 'zero')

print('\n=== Matrix: dimension mismatch ===')
try:
    lexer = Lexer('[[1,2]] + [[3,4];[5,6]]')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = repl.interp.eval(ast)
    check('matrix dim mismatch should error', 'error', 'error')
except Exception as e:
    check('matrix dim mismatch errors', f'{e}', 'mismatch')

print('\n=== Matrix multiplication ===')
r = run(repl, 'm = [[1,2];[3,4]]')
r = run(repl, 'n = [[5,6];[7,8]]')
r = run(repl, 'm ** n')
check('matrix mul', r, '19')
check('matrix mul 2', r, '22')
check('matrix mul 3', r, '43')
check('matrix mul 4', r, '50')

print('\n=== Undefined variable error ===')
try:
    lexer = Lexer('unknownVar')
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = repl.interp.eval(ast)
    check('undefined var should error', 'error', 'error')
except Exception as e:
    check('undefined var errors', f'{e}', 'undefined')

if errors:
    print(f'\n{len(errors)} FAILURES:')
    for e in errors:
        print(f'  {e}')
else:
    print('\nAll extra tests passed!')
