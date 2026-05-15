from .ast_nodes import FunctionDef
from .exceptions import NameError_


class Environment:
    def __init__(self):
        self._variables = {}
        self._functions = {}

    def _normalize(self, name):
        return name.lower()

    def set_variable(self, name, value):
        key = self._normalize(name)
        self._variables[key] = value

    def get_variable(self, name):
        key = self._normalize(name)
        if key not in self._variables:
            raise NameError_(f'Undefined variable: {name}')
        return self._variables[key]

    def has_variable(self, name):
        return self._normalize(name) in self._variables

    def set_function(self, name, func_def):
        key = self._normalize(name)
        self._functions[key] = func_def

    def get_function(self, name):
        key = self._normalize(name)
        if key not in self._functions:
            raise NameError_(f'Undefined function: {name}')
        return self._functions[key]

    def has_function(self, name):
        return self._normalize(name) in self._functions

    def is_defined(self, name):
        key = self._normalize(name)
        return key in self._variables or key in self._functions

    def __repr__(self):
        return f'Environment(vars={self._variables}, funcs={self._functions})'
