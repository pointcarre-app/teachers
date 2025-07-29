
from sympy.parsing.latex import parse_latex
import sympy as sp

original_expr = sp.Eq(sp.sqrt(sp.Symbol('x')), 1)
parsed_expr = parse_latex("\\sqrt{x} = 1")
assert original_expr == parsed_expr
# expr = parse_latex("\\sqrt{x} = 1")


# missive({"key": "coucou", "expr": str(expr)})
# missive({"key": "coucou", "expr": str(expr)})
# missive({"key": "coucou", "expr": str(expr)})
