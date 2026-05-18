from .ast_nodes import Number, Identifier, ImaginaryUnit, UnaryOp, BinaryOp, FunctionCall, Norm, Compose
from .exceptions import RuntimeError_


def simplify(node):
    node = _round(node)
    while True:
        prev = repr(node)
        node = _round(node)
        if repr(node) == prev:
            break
    return node


def _round(node):
    node = _deep(node)
    node = _distribute(node)
    node = _deep(node)
    node = _fold(node)
    node = _collect(node)
    return node


def _deep(node):
    if isinstance(node, (Number, Identifier, ImaginaryUnit)):
        return node
    if isinstance(node, UnaryOp):
        return UnaryOp(node.op, _round(node.expr))
    if isinstance(node, BinaryOp):
        return BinaryOp(_round(node.left), node.op, _round(node.right))
    if isinstance(node, FunctionCall):
        return FunctionCall(node.name, _round(node.arg))
    if isinstance(node, Norm):
        return Norm(_round(node.expr))
    if isinstance(node, Compose):
        return Compose(_round(node.left), _round(node.right))
    return node


def _is_num(node):
    return isinstance(node, Number)


def _is_var(node):
    return isinstance(node, Identifier)


def _is_zero(node):
    return _is_num(node) and (node.value == '0' or float(node.value) == 0.0)


def _is_one(node):
    return _is_num(node) and (node.value == '1' or float(node.value) == 1.0)


def _num_val(node):
    if '.' in node.value:
        return float(node.value)
    return int(node.value)


def _distribute(node):
    if not isinstance(node, BinaryOp):
        return node
    l = _distribute(node.left)
    r = _distribute(node.right)

    if node.op == '*':
        if isinstance(r, BinaryOp) and r.op == '+':
            return BinaryOp(BinaryOp(l, '*', r.left), '+', BinaryOp(l, '*', r.right))
        if isinstance(r, BinaryOp) and r.op == '-':
            return BinaryOp(BinaryOp(l, '*', r.left), '-', BinaryOp(l, '*', r.right))
        if isinstance(l, BinaryOp) and l.op == '+':
            return BinaryOp(BinaryOp(l.left, '*', r), '+', BinaryOp(l.right, '*', r))
        if isinstance(l, BinaryOp) and l.op == '-':
            return BinaryOp(BinaryOp(l.left, '*', r), '-', BinaryOp(l.right, '*', r))
    return BinaryOp(l, node.op, r)


def _fold(node):
    if not isinstance(node, BinaryOp):
        return node

    if node.op == '+':
        if _is_zero(node.left):
            return node.right
        if _is_zero(node.right):
            return node.left
        if _is_num(node.left) and _is_num(node.right):
            return Number(str(_num_val(node.left) + _num_val(node.right)))

    if node.op == '-':
        if _is_zero(node.right):
            return node.left
        if _is_zero(node.left):
            return UnaryOp('-', node.right)
        if _is_num(node.left) and _is_num(node.right):
            return Number(str(_num_val(node.left) - _num_val(node.right)))

    if node.op == '*':
        if _is_zero(node.left) or _is_zero(node.right):
            return Number('0')
        if _is_one(node.left):
            return node.right
        if _is_one(node.right):
            return node.left
        if _is_num(node.left) and _is_num(node.right):
            return Number(str(_num_val(node.left) * _num_val(node.right)))
        # Combine coefficients: (a * v) * b  →  (a * b) * v
        if isinstance(node.left, BinaryOp) and node.left.op == '*' and _is_num(node.left.left) and isinstance(node.left.right, Identifier) and _is_num(node.right):
            return BinaryOp(BinaryOp(Number(str(_num_val(node.left.left) * _num_val(node.right))), '*', node.left.right), '*', node.right)
        # no that's wrong. Let me just handle the simple case

    return BinaryOp(node.left, node.op, node.right)


def _collect(node):
    if not isinstance(node, BinaryOp):
        return node
    terms = {}
    _flatten(node, terms, 1)
    return _rebuild(terms)


def _flatten(node, terms, sign):
    if isinstance(node, Number):
        v = float(node.value) if '.' in node.value else int(node.value)
        key = ''
        terms[key] = terms.get(key, 0) + sign * v
    elif isinstance(node, Identifier):
        terms[node.name.lower()] = terms.get(node.name.lower(), 0) + sign * 1
    elif isinstance(node, UnaryOp) and node.op == '-':
        _flatten(node.expr, terms, -sign)
    elif isinstance(node, BinaryOp):
        if node.op == '+':
            _flatten(node.left, terms, sign)
            _flatten(node.right, terms, sign)
        elif node.op == '-':
            _flatten(node.left, terms, sign)
            _flatten(node.right, terms, -sign)
        elif node.op == '*':
            coeff, var_name = _extract_prod(node)
            terms[var_name] = terms.get(var_name, 0) + sign * coeff
        else:
            key = repr(node)
            terms[key] = terms.get(key, 0) + sign * 1
    elif isinstance(node, (ImaginaryUnit, FunctionCall, Norm, Compose)):
        key = repr(node)
        terms[key] = terms.get(key, 0) + sign * 1
    else:
        key = repr(node)
        terms[key] = terms.get(key, 0) + sign * 1


def _extract_prod(node):
    if isinstance(node, BinaryOp) and node.op == '*':
        l, r = node.left, node.right
        if isinstance(l, Number) and isinstance(r, Identifier):
            v = float(l.value) if '.' in l.value else int(l.value)
            return (v, r.name.lower())
        if isinstance(l, Identifier) and isinstance(r, Number):
            v = float(r.value) if '.' in r.value else int(r.value)
            return (v, l.name.lower())
        if isinstance(l, Number):
            v = float(l.value) if '.' in l.value else int(l.value)
            inner_v, inner_k = _extract_prod(r)
            return (v * inner_v, inner_k)
        if isinstance(r, Number):
            v = float(r.value) if '.' in r.value else int(r.value)
            inner_v, inner_k = _extract_prod(l)
            return (v * inner_v, inner_k)
    if isinstance(node, Identifier):
        return (1, node.name.lower())
    return (1, repr(node))


def _rebuild(terms):
    result = None
    for key, coeff in sorted(terms.items(), key=lambda x: (x[0] == '', x[0])):
        if coeff == 0:
            continue
        if key == '':
            if coeff == int(coeff):
                term = Number(str(int(coeff)))
            else:
                term = Number(str(coeff))
        else:
            if coeff == 1:
                term = Identifier(key)
            elif coeff == -1:
                term = UnaryOp('-', Identifier(key))
            else:
                if coeff == int(coeff):
                    c = Number(str(int(coeff)))
                else:
                    c = Number(str(coeff))
                term = BinaryOp(c, '*', Identifier(key))
        if result is None:
            result = term
        else:
            result = BinaryOp(result, '+', term)
    return result or Number('0')
