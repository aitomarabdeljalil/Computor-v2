from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .exceptions import ComputorError
from .printer import print_value, print_solutions
from .types.rational import Rational
from .types.complex_num import Complex
from .types.matrix import Matrix
from .ast_nodes import FunctionDef


class REPL:
    MAX_HISTORY = 100

    def __init__(self):
        self.env = Environment()
        self.interp = Interpreter(self.env)
        self.history = []

    def _format_output(self, result):
        if result is None:
            return None
        if isinstance(result, tuple) and len(result) == 4:
            eq_left, eq_right, domain, solutions = result
            return f'{eq_left} = {eq_right}\n{print_solutions(solutions, domain)}'
        return print_value(result)

    def _exec(self, text):
        lexer = Lexer(text)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.interp.eval(ast)
        return ast, result

    def _add_history(self, input_text, output_text, ast):
        self.history.append({
            'input': input_text,
            'output': output_text,
            'ast': ast,
        })
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

    def _get_vars_output(self):
        vars = self.env.get_all_variables()
        funcs = self.env.get_all_functions()
        if not vars and not funcs:
            return 'No variables or functions defined.'
        lines = []
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
            lines.append(f'{name} ({t}) = {val_str}')
        for name in funcs:
            if name not in vars:
                val_str = print_value(funcs[name])
                lines.append(f'{name} (function) = {val_str}')
        return '\n'.join(lines)

    def _get_history_output(self):
        if not self.history:
            return 'No history.'
        lines = []
        for i, entry in enumerate(self.history, 1):
            lines.append(f'{i:3}: {entry["input"]}')
        return '\n'.join(lines)

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
                    output = self._get_vars_output()
                    print(output)
                    self._add_history(text, output, None)
                    continue
                if text.lower() == 'history':
                    output = self._get_history_output()
                    print(output)
                    self._add_history(text, output, None)
                    continue

                if text.startswith('!'):
                    try:
                        idx = int(text[1:])
                    except ValueError:
                        print(f'Error: Invalid history index: {text[1:]}')
                        continue
                    if idx < 1 or idx > len(self.history):
                        print(f'Error: No such history entry: {idx}')
                        continue
                    entry = self.history[idx - 1]
                    replay_text = entry['input']
                    print(f'Re-running: {replay_text}')
                    if entry['ast'] is not None:
                        result = self.interp.eval(entry['ast'])
                        output_str = self._format_output(result)
                        if output_str:
                            print(output_str)
                        self._add_history(replay_text, output_str, entry['ast'])
                    else:
                        if replay_text.lower() in ('vars', 'showvars'):
                            output = self._get_vars_output()
                            print(output)
                            self._add_history(replay_text, output, None)
                        elif replay_text.lower() == 'history':
                            output = self._get_history_output()
                            print(output)
                            self._add_history(replay_text, output, None)
                    continue

                ast, result = self._exec(text)
                output_str = self._format_output(result)
                if output_str:
                    print(output_str)
                self._add_history(text, output_str, ast)

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
                lines_out = []
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
                    lines_out.append(f'{name} ({t}) = {val_str}')
                for name in funcs:
                    if name not in vars:
                        val_str = print_value(funcs[name])
                        lines_out.append(f'{name} (function) = {val_str}')
                output = '\n'.join(lines_out)
                outputs.append(output)
                self._add_history(text, output, None)
                continue
            ast, result = self._exec(text)
            if result is None:
                outputs.append('')
                self._add_history(text, '', ast)
                continue
            if isinstance(result, tuple) and len(result) == 4:
                eq_left, eq_right, domain, solutions = result
                output = f'{eq_left} = {eq_right}'
                sol_str = print_solutions(solutions, domain)
                outputs.append(output)
                outputs.append(sol_str)
                self._add_history(text, output + '\n' + sol_str, ast)
            else:
                output = print_value(result)
                outputs.append(output)
                self._add_history(text, output, ast)
        return outputs


def main():
    repl = REPL()
    repl.run()
