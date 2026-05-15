import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .exceptions import ComputorError, RuntimeError_, NameError_, TypeError_, ZeroDivisionError_
from .printer import print_value, print_solutions


class REPL:
    def __init__(self):
        self.env = Environment()
        self.interp = Interpreter(self.env)

    def run(self):
        print('Computor v2 - Type "exit" to quit')
        while True:
            try:
                text = input('> ').strip()
                if not text:
                    continue
                if text.lower() in ('exit', 'quit'):
                    break

                lexer = Lexer(text)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                result = self.interp.eval(ast)

                if result is None:
                    continue

                if isinstance(result, tuple) and len(result) == 4:
                    eq_left, eq_right, domain, solutions = result
                    print(f'{eq_left} = {eq_right}')
                    print(print_solutions(solutions, domain))
                else:
                    print(print_value(result))

            except KeyboardInterrupt:
                print()
                continue
            except EOFError:
                print()
                break
            except ComputorError as e:
                print(f'Error: {e}')

    def run_batch(self, lines):
        outputs = []
        for text in lines:
            text = text.strip()
            if not text:
                continue
            if text.lower() in ('exit', 'quit'):
                break
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            result = self.interp.eval(ast)
            if result is None:
                outputs.append('')
                continue
            if isinstance(result, tuple) and len(result) == 4:
                eq_left, eq_right, domain, solutions = result
                outputs.append(f'{eq_left} = {eq_right}')
                outputs.append(print_solutions(solutions, domain))
            else:
                outputs.append(print_value(result))
        return outputs


def main():
    repl = REPL()
    repl.run()
