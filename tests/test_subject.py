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

# V.2 Assignments
r = run(repl, 'varA = 2')
assert '2' in r, f'Expected 2, got {r}'
print(f'varA = 2 -> {r}')

r = run(repl, 'varB = 4.242')
assert '4.242' in r, f'Expected 4.242, got {r}'
print(f'varB = 4.242 -> {r}')

r = run(repl, 'varC = -4.3')
assert '-4.3' in r, f'Expected -4.3, got {r}'
print(f'varC = -4.3 -> {r}')

r = run(repl, 'varA = 2*i + 3')
assert '3' in r and '2i' in r, f'Expected 3 + 2i, got {r}'
print(f'varA = 2*i + 3 -> {r}')

r = run(repl, 'varB = -4i - 4')
assert '-4' in r and '- 4i' in r, f'Expected -4 - 4i, got {r}'
print(f'varB = -4i - 4 -> {r}')

r = run(repl, 'varA = [[2,3];[4,3]]')
assert '2' in r and '3' in r, f'Expected matrix, got {r}'
print(f'varA = [[2,3];[4,3]] ->\n{r}')

r = run(repl, 'varB = [[3,4]]')
assert '3' in r and '4' in r, f'Expected [3,4], got {r}'
print(f'varB = [[3,4]] -> {r}')

r = run(repl, 'funA(x) = 2*x^5 + 4*x^2 - 5*x + 4')
assert 'x' in r, f'Expected expression with x, got {r}'
print(f'funA(x) = 2*x^5 + 4*x^2 - 5*x + 4 -> {r}')

# V.2 Reassignment
print('\n=== Reassignment ===')
r = run(repl, 'x = 2')
assert '2' in r, f'Expected 2, got {r}'
print(f'x = 2 -> {r}')

r = run(repl, 'y = x')
assert '2' in r, f'Expected 2, got {r}'
print(f'y = x -> {r}')

r = run(repl, 'y = 7')
assert '7' in r, f'Expected 7, got {r}'
print(f'y = 7 -> {r}')

r = run(repl, 'y = 2 * i - 4')
assert '-4' in r and '2i' in r, f'Expected -4 + 2i, got {r}'
print(f'y = 2 * i - 4 -> {r}')

# V.2 Computation chain
print('\n=== Computation chain ===')
r = run(repl, 'varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)')
assert '27' in r, f'Expected 27, got {r}'
print(f'-> {r}')

r = run(repl, 'varB = 2 * varA - 5 %4')
assert '53' in r, f'Expected 53, got {r}'
print(f'-> {r}')

r = run(repl, 'funA(x) = varA + varB * 4 - 1 / 2 + x')
assert 'x' in r, f'Expected expression with x, got {r}'
print(f'-> {r}')

r = run(repl, 'varC = 2 * varA - varB')
assert '1' in r, f'Expected 1, got {r}'
print(f'-> {r}')

r = run(repl, 'varD = funA(varC)')
print(f'-> {r}')

# V.3 Query
print('\n=== Query ===')
r = run(repl, 'a = 2 * 4 + 4')
assert '12' in r, f'Expected 12, got {r}'
print(f'-> {r}')

r = run(repl, 'a + 2 = ?')
assert '14' in r, f'Expected 14, got {r}'
print(f'a + 2 = ? -> {r}')

# V.3 Solver
print('\n=== Solver ===')
repl2 = REPL()
r = run(repl2, 'funA(x) = x^2 + 2*x + 1')
print(f'funA(x) = x^2 + 2*x + 1 -> {r}')

r = run(repl2, 'y = 0')
print(f'y = 0 -> {r}')

r = run(repl2, 'funA(x) = y ?')
assert '-1' in r, f'Expected -1, got {r}'
print(f'funA(x) = y ? ->\n{r}')

# V.4 Syntax
print('\n=== Syntax ===')
repl3 = REPL()
r = run(repl3, 'varA = 2')
assert '2' in r
r = run(repl3, 'varB= 2 * (4 + varA + 3)')
assert '18' in r, f'Expected 18, got {r}'
print(f'varB= 2 * (4 + varA + 3) -> {r}')

r = run(repl3, 'varC =2 * varB')
assert '36' in r, f'Expected 36, got {r}'
print(f'varC =2 * varB -> {r}')

r = run(repl3, 'varD = 2 *(2 + 4 *varC -4 /3)')
assert '289' in r, f'Expected ~289.33, got {r}'
print(f'varD = 2 *(2 + 4 *varC -4 /3) -> {r}')

# V.4.2 Matrices
print('\n=== Matrices ===')
repl4 = REPL()
r = run(repl4, 'matA = [[1,2];[3,2];[3,4]]')
assert '1' in r and '2' in r and '3' in r
print(f'matA = [[1,2];[3,2];[3,4]] ->\n{r}')
r = run(repl4, 'matB= [[1,2]]')
print(f'matB= [[1,2]] -> {r}')

print('\nAll tests passed!')
