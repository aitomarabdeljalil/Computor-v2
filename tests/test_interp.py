from computorv2.repl import REPL
from computorv2.lexer import Lexer
from parser import Parser
from computorv2.types.rational import Rational
from computorv2.types.complex_num import Complex
from computorv2.types.matrix import Matrix
from computorv2.printer import print_value


def run(text):
    repl = REPL()
    lines = text.strip().split('\n')
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        lexer = Lexer(line)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = repl.interp.eval(ast)
        results.append((line, result))
    return results


results = run('''
x = 2
y = x
y = 7
y = 2 * i - 4
a = 2 * 4 + 4
varB = 2 * 5 - 5 % 4
matA = [[1,2];[3,4]]
matB = [[1,2]]
''')

for line, result in results:
    val_str = print_value(result) if result is not None else 'None'
    print(f'{line} -> {val_str}')
