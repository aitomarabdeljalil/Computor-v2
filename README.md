# Computor v2

> "Your homemade basic calculator"

An interpreter for advanced mathematical computations — rational numbers, complex numbers, matrices, functions, and polynomial equation solving (degree ≤ 2). Inspired by `bc` and Google calculator.

## Features

- **Rational numbers** — any `x ∈ Q`
- **Complex numbers** — `a + ib` with rational coefficients
- **Matrices** — `M_{n,p}(Q)` with term-by-term (`*`), matrix product (`**`), and inverse (`A^-1` / `inverse(A)`)
- **Norm / absolute value** — `\|expr\|` or `norm(expr)`: modulus for complex, Frobenius norm for matrices
- **Functions** — single-variable functions with symbolic evaluation
- **Function composition** — `f @ g` creates `h(x) = f(g(x))` via AST substitution
- **Symbolic composition queries** — `funA(funB(x)) = ?` evaluates and simplifies inline without storing
- **Polynomial solver** — equations of degree ≤ 2, solutions in ℝ or ℂ
- **Expression simplification** — e.g., `2 + 3 * 4` → `14`
- **Variable assignment** — type inference, reassignment, cross-type
- **List defined variables** — `vars` / `showvars` command
- **Command history** — last 100 commands stored; re-run with `!<index>`; no re-parsing
- **REPL** — interactive command-line interpreter

## Quick start

```bash
python -m computorv2
```

Type expressions at the `> ` prompt. Exit with `exit`, `quit`, or `Ctrl+D`/`Ctrl+C`.

## Usage

### Rational numbers

```
> x = 2
2
> y = 4.242
4.242
> z = -4.3
-4.3
```

### Complex numbers

```
> a = 2*i + 3
3 + 2i
> b = -4i - 4
-4 - 4i
> (1 + i) * (1 - i)
2
```

### Matrices

```
> m = [[1,2];[3,4]]
[ 1, 2 ]
[ 3, 4 ]
> n = [[5,6];[7,8]]
[ 5, 6 ]
[ 7, 8 ]
```

### Matrix operations

| Operator | Meaning |
|----------|---------|
| `+`, `-` | Element-wise addition/subtraction |
| `*` | Scalar multiplication or element-wise product |
| `**` | Matrix multiplication |
| `^` | Integer power (square matrices only); `^-1` for inverse |
| `@` | Function composition (`f @ g` = `f ∘ g`) |

```
> [[1,2];[3,4]] ** [[2,0];[1,2]]
[ 4, 4 ]
[ 10, 8 ]
```

### Matrix inversion

Square matrices (2×2, 3×3, and larger) can be inverted using `inverse(A)` or `A^-1`.

```
> A = [[1,2];[3,4]]
[ 1, 2 ]
[ 3, 4 ]
> inverse(A)
[ -2, 1 ]
[ 3/2, -1/2 ]
> A^-1
[ -2, 1 ]
[ 3/2, -1/2 ]
>
> B = [[1,0,2];[-1,3,1];[0,2,-2]]
[ 1, 0, 2 ]
[ -1, 3, 1 ]
[ 0, 2, -2 ]
> inverse(B)
[ 2/3, -1/3, 1/2 ]
[ 1/6, 1/6, 1/4 ]
[ 1/6, 1/6, -1/4 ]
```

**Determinant calculation** (no external libraries):

- **1×1**: the single element itself
- **2×2**: `det = a·d − b·c`  
- **3×3**: `det = a·(e·i − f·h) − b·(d·i − f·g) + c·(d·h − e·g)`  
- **n×n** (n > 3): recursive Laplace expansion along the first row  

All elements are stored as `Complex` values, so the determinant is computed using the arithmetic on `Rational` and `Complex` types defined in the project — no floating-point dependency for the determinant itself.

**Inverse** uses the adjugate formula:  
`A⁻¹ = (1 / det(A)) · adj(A)`  

1. Compute `det(A)`  
2. If `det(A) = 0` → error: `Matrix is singular (determinant is zero) — no inverse exists`  
3. Compute the cofactor matrix: `C[i][j] = (-1)^(i+j) · det(minor(A, i, j))`  
4. Transpose to get the adjugate: `adj(A) = Cᵀ`  
5. Multiply by `1/det`: `adj(A) · (1/det)`  

Singular matrices (det = 0) and non-square matrices are rejected with clear error messages:

```
> C = [[1,2];[2,4]]
[ 1, 2 ]
[ 2, 4 ]
> inverse(C)
Error: Matrix is singular (determinant is zero) — no inverse exists
```

### Norm / absolute value

Two syntaxes compute the norm of a value: `|expr|` and `norm(expr)`. The mathematical definition depends on the type:

| Type | Norm | Definition |
|------|------|------------|
| **Rational** `x` | Absolute value | `\|x\| = x` if `x ≥ 0`, `-x` otherwise |
| **Complex** `a + ib` | Modulus | `\|a + ib\| = √(a² + b²)` |
| **Matrix** `A` (m×n) | Frobenius norm | `‖A‖_F = √(∑ᵢ ∑ⱼ \|aᵢⱼ\|²)` |

All norms are computed using only the standard library:
- **Rational**: uses the existing `abs()` / `__abs__` implementation on `fractions.Fraction`
- **Complex**: `real² + imag²` → `Rational.sqrt()` returns a perfect-square rational when possible, or a `limit_denominator` approximation via `math.isqrt`
- **Matrix Frobenius**: sums `elem.real² + elem.imag²` for every element, takes the floating-point `math.sqrt`, then rounds the result with `Fraction.limit_denominator(1_000_000)`

```
> |-5|
5
> |3 + 4i|
5
> |[[1,2];[3,4]]|
5.4772255751
> norm(-5)
5
> norm(3 + 4i)
5
> norm([[1,0];[0,1]])
1.4142135624
```

The `|expr|` syntax is parsed as a `Norm` AST node, while `norm(expr)` is handled as a built-in function call in the interpreter (reserved name). Both evaluate the same `norm()` method on the runtime value.

### Functions

```
> funA(x) = 2*x + 1
2 * x + 1
> funB(y) = y^2 + 3*y - 5
y ^ 2 + 3 * y - 5
```

### Function image

```
> funA(x) = 2*4 + x
8 + x
> funA(5)
13
```

### Function composition

Two functions can be composed using the `@` operator. The expression `h = f @ g` creates a new function `h` such that `h(x) = f(g(x))`.

```
> f(x) = x + 1
x + 1
> g(t) = t * 2
t * 2
> h = f @ g
t * 2 + 1
> h(5)
11
> h(-3)
-5
```

Chaining is supported via right-associativity: `f @ g @ h2` is `f ∘ (g ∘ h2)`.

```
> h2(x) = x^2
x ^ 2
> k = f @ g @ h2
x ^ 2 * 2 + 1
> k(3)
19
```

**How it works**: `@` is parsed as a `Compose` AST node. The interpreter evaluates it by:
1. Looking up the function definitions for `f` and `g` from the environment
2. Calling `_substitute_var(f.body, Identifier(f.param), g.body)` — this replaces every occurrence of `f`'s parameter in f's body with the **AST** of `g`'s body (not a numeric value)
3. The result is a new `FunctionDef` with `g`'s parameter and the substituted body

This means the composed function is defined entirely at the AST level — no re-parsing needed, and the body is stored in a form that can be inspected and further composed.

### Queries

Use `= ?` to evaluate an expression:

```
> a = 2 * 4 + 4
12
> a + 2 = ?
14
> funA(2) + funB(4) = ?
41
```

Use `?` after an equation to solve it:

```
> funA(x) = x^2 + 2*x + 1
x ^ 2 + 2 * x + 1
> y = 0
0
> funA(x) = y ?
x ^ 2 + 2 * x + 1 = 0
One solution in R:
-1
```

### Symbolic composition queries

A nested function call followed by `= ?` evaluates the composition symbolically, substituting inner function bodies and algebraically simplifying the result. No new function is stored — the result is displayed and discarded.

```
> funA(x) = 2*x + 1
2 * x + 1
> funB(x) = 2*x + 1
2 * x + 1
> funA(funB(x)) = ?
4 * x + 3
```

Variable renaming handles differing parameter names automatically:

```
> f(t) = 2*t + 1
2 * t + 1
> g(y) = y + 3
y + 3
> f(g(x)) = ?
2 * x + 7
```

Chains of any depth are supported:

```
> h(z) = 3*z
3 * z
> f(g(h(x))) = ?
6 * x + 7
```

**How it works**:
1. The `_eval_query` method detects the pattern `FunctionCall(FunctionCall(...(Identifier)...))`
2. Instead of numeric evaluation, it walks from innermost to outermost, calling `_substitute_var` to replace each function's parameter with the next inner function's **AST body**
3. The final composed AST is passed to `simplify()` (in `simplify.py`) which performs:
   - **Distribution**: `a·(b + c)` → `a·b + a·c`
   - **Constant folding**: `2·3` → `6`, `x + 0` → `x`
   - **Term collection**: flattens `+` chains, groups same-variable terms, combines coefficients
4. The resulting simplified AST is passed to `print_expression` for clean output

### Command history

Every command entered at the REPL is stored in an in-memory history buffer (max 100 entries). Use `history` to list all entries with their indices, and `!<N>` to re-execute a previous command:

```text
> x = 42
42
> x + 8
50
> f(t) = t^2 + 2*t + 1
t ^ 2 + 2 * t + 1
> history
  1: x = 42
  2: x + 8
  3: f(t) = t^2 + 2*t + 1
> !2
Re-running: x + 8
50
> !3
Re-running: f(t) = t^2 + 2*t + 1
t ^ 2 + 2 * t + 1
> f(3)
16
```

Re-execution works by storing the parsed **AST node** alongside each command, so `!<N>` calls the interpreter directly on the saved AST — no lexing or re-parsing needed. This means re-execution always reflects the *current* environment (variable values, function definitions).

Meta-commands (`vars`, `showvars`, `history`) are also stored and can be re-executed, but their handler is re-invoked directly since they have no AST.

`!<N>` itself is not added to history, avoiding duplicate entries.

### Operators

| Operator | Meaning |
|----------|---------|
| `+` `-` | Addition / subtraction / unary minus |
| `*` `**` | Multiplication / matrix multiplication |
| `/` | Division |
| `%` | Modulo |
| `^` | Power (integer, non-negative); `^-1` for matrix inverse |
| `@` | Function composition (`f @ g` = `f ∘ g`) |
| `=` | Assignment (variables) or equation (solver) |
| `?` | Query / solve trigger |
| `\|` `\|` | Norm / absolute value (`|expr|`) |
| `()` | Parentheses for grouping |
| `[]` | Matrix literals |
| `;` | Row separator in matrices |
| `,` | Column separator in matrices |

### Variables

- Names: letters and digits, must start with a letter, case-insensitive (`varA` ≡ `vara`)
- `i` is reserved for the imaginary unit
- Type inference on assignment; types can change on reassignment

```
> x = 2
2
> x = 3 + 4i
3 + 4i
> x = -(7/3)
-7/3
```

### Listing defined variables

Use `vars` or `showvars` to display all defined variables, their types, and values:

```text
> x = 42
42
> y = 3 + 4i
3 + 4i
> f(t) = 2*t + 1
2 * t + 1
> vars
x (rational) = 42
y (complex) = 3 + 4i
f (function) = 2 * t + 1
> showvars
x (rational) = 42
y (complex) = 3 + 4i
f (function) = 2 * t + 1
```

## Project structure

```
computorv2/
├── __init__.py
├── __main__.py          # Entry point: python -m computorv2
├── repl.py              # REPL loop
├── lexer.py             # Tokenizer
├── parser.py            # Recursive descent parser
├── ast_nodes.py         # AST node definitions
├── interpreter.py       # Evaluator
├── environment.py       # Symbol table
├── solver.py            # Polynomial equation solver
├── simplify.py          # Algebraic simplification engine
├── printer.py           # Output formatting
├── exceptions.py        # Custom error types
└── types/
    ├── __init__.py
    ├── rational.py      # Q type (wraps fractions.Fraction)
    ├── complex_num.py   # C type (a + ib)
    └── matrix.py        # Matrix type (M_n,p)
```

## Solver

Solves polynomial equations of degree ≤ 2. The solver:
1. Interpolates polynomial coefficients from function evaluation
2. Computes discriminant Δ = b² − 4ac
3. Returns solutions in ℝ or ℂ:
   - Δ > 0: two real solutions
   - Δ = 0: one real solution
   - Δ < 0: two complex solutions (conjugate pair)

## Dependencies

Python 3.8+ with no external dependencies. Only uses the standard library (`fractions.Fraction`).

## Tests

Test files are in the project root:

```bash
python3 test_lexer.py
python3 test_parser.py
python3 test_advanced.py
python3 test_subject.py
```
