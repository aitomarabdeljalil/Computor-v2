# Computor v2

> "Your homemade basic calculator"

An interpreter for advanced mathematical computations — rational numbers, complex numbers, matrices, functions, and polynomial equation solving (degree ≤ 2). Inspired by `bc` and Google calculator.

## Features

- **Rational numbers** — any `x ∈ Q`
- **Complex numbers** — `a + ib` with rational coefficients
- **Matrices** — `M_{n,p}(Q)` with term-by-term (`*`) and matrix product (`**`)
- **Functions** — single-variable functions with symbolic evaluation
- **Polynomial solver** — equations of degree ≤ 2, solutions in ℝ or ℂ
- **Expression simplification** — e.g., `2 + 3 * 4` → `14`
- **Variable assignment** — type inference, reassignment, cross-type
- **List defined variables** — `vars` / `showvars` command
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
| `^` | Integer power (square matrices only) |

```
> [[1,2];[3,4]] ** [[2,0];[1,2]]
[ 4, 4 ]
[ 10, 8 ]
```

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

### Operators

| Operator | Meaning |
|----------|---------|
| `+` `-` | Addition / subtraction / unary minus |
| `*` `**` | Multiplication / matrix multiplication |
| `/` | Division |
| `%` | Modulo |
| `^` | Power (integer, non-negative) |
| `=` | Assignment (variables) or equation (solver) |
| `?` | Query / solve trigger |
| `()` | Parentheses for grouping |
| `[]` | Matrix literals |
| `;` | Row separator in matrices |
| `,` | Column separator in matrices |

### Variables

- Names: only letters, case-insensitive (`varA` ≡ `vara`)
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
