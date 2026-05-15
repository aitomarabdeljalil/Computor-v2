class ComputorError(Exception):
    pass

class LexerError(ComputorError):
    pass

class ParserError(ComputorError):
    pass

class RuntimeError_(ComputorError):
    pass

class TypeError_(RuntimeError_):
    pass

class NameError_(RuntimeError_):
    pass

class ZeroDivisionError_(RuntimeError_):
    pass
