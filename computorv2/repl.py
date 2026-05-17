import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .exceptions import ComputorError, RuntimeError_, NameError_, TypeError_, ZeroDivisionError_
from .printer import print_value, print_solutions
from .types.rational import Rational
from .types.complex_num import Complex
from .types.matrix import Matrix
from .ast_nodes import FunctionDef


class REPL:
    def __init__(self):
        self.env = Environment()
        self.interp = Interpreter(self.env)

    def _handle_vars(self):
        vars = self.env.get_all_variables()
        funcs = self.env.get_all_functions()
        if not vars and not funcs:
            print('No variables or functions defined.')
            return
        for name, value in vars.items():
            if isinstance(value, Rational):
                t = 'rational'
            elif isinstance(value, Complex):
                t = 'complex'
            elif isinstance(value, Matrix):
                t = 'matrix'
            elif isinstance(value, FunctionDef):
                t = 'function'
            else:
                t = type(value).__name__
            val_str = print_value(value)
            print(f'{name} ({t}) = {val_str}')
        for name in funcs:
            if name not in vars:
                val_str = print_value(funcs[name])
                print(f'{name} (function) = {val_str}')

    def run(self):
        print('Computor v2 - Type "exit" to quit')
        while True:
            try:
                text = input('> ').strip()
                if not text:
                    continue
                if text.lower() in ('exit', 'quit'):
                    break
                if text.lower() in ('vars', 'showvars'):
                    self._handle_vars()
                    continue

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
            if text.lower() in ('vars', 'showvars'):
                vars = self.env.get_all_variables()
                funcs = self.env.get_all_functions()
                for name, value in vars.items():
                    if isinstance(value, Rational):
                        t = 'rational'
                    elif isinstance(value, Complex):
                        t = 'complex'
                    elif isinstance(value, Matrix):
                        t = 'matrix'
                    elif isinstance(value, FunctionDef):
                        t = 'function'
                    else:
                        t = type(value).__name__
                    val_str = print_value(value)
                    outputs.append(f'{name} ({t}) = {val_str}')
                for name in funcs:
                    if name not in vars:
                        val_str = print_value(funcs[name])
                        outputs.append(f'{name} (function) = {val_str}')
                continue
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
