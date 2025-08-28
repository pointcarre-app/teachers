"""
Test suite for the double minus issue fix in Add.latex().

This module tests the fix for the double minus LaTeX rendering issue
where expressions like 'x - (-5 + 1/2)' would incorrectly render as
'x --5 + 1/2' instead of the correct 'x - \\left(-5 + 1/2\\right)'.

The fix ensures complex negative expressions are properly parenthesized
for educational clarity while preserving simplicity for basic cases.
"""

import unittest
import teachers.maths as tm


class TestDoubleMinusFix(unittest.TestCase):
    """Test cases for the double minus issue fix in Add.latex()"""

    def test_original_issue_case(self):
        """Test the exact case that caused the double minus issue"""
        # Simulate: a2 * x - (b2 + tm.Integer(n=1) / (c2 ** (tm.Integer(n=1) / tm.Integer(n=2))))
        # where a2 = 1/5, b2 = -8, c2 = 8

        x = tm.Symbol(s="x")
        a2 = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=5))
        b2 = tm.Integer(n=-8)
        c2 = tm.Integer(n=8)

        # Build: b2 + 1 / sqrt(c2)
        inner_expr = tm.Add(
            l=b2,
            r=tm.Fraction(
                p=tm.Integer(n=1),
                q=tm.Pow(base=c2, exp=tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=2))),
            ),
        )

        # Build: a2 * x - (inner_expr)
        expr2 = tm.Add(l=tm.Mul(l=a2, r=x), r=tm.Mul(l=tm.Integer(n=-1), r=inner_expr))

        latex_result = expr2.latex()

        # Should NOT contain double minus "--"
        assert "--" not in latex_result
        # Should contain proper parentheses around the complex expression
        assert "\\left(" in latex_result and "\\right)" in latex_result
        # Should look like: \dfrac{1}{5}x - \left(-8 + \dfrac{1}{\sqrt{8}}\right)
        expected_parts = [
            "\\dfrac{1}{5}",
            "x",
            "-",
            "\\left(",
            "-8",
            "+",
            "\\dfrac{1}",
            "\\sqrt{8}",
            "\\right)",
        ]
        for part in expected_parts:
            assert part in latex_result

    def test_simple_negative_number_no_parentheses(self):
        """Simple negative numbers should not get extra parentheses"""
        x = tm.Symbol(s="x")
        expr = tm.Add(l=x, r=tm.Integer(n=-5))

        latex_result = expr.latex()

        # Should be "x -5" (no extra parentheses for simple negative numbers)
        assert latex_result == "x -5"
        assert "\\left(" not in latex_result

    def test_negative_fraction_gets_parentheses(self):
        """Negative fractions should get parentheses"""
        x = tm.Symbol(s="x")
        frac = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=3))
        expr = tm.Add(l=x, r=tm.Mul(l=tm.Integer(n=-1), r=frac))

        latex_result = expr.latex()

        # Should have parentheses around the fraction
        assert "\\left(" in latex_result and "\\right)" in latex_result
        assert "--" not in latex_result

    def test_negative_add_expression_gets_parentheses(self):
        """Negative Add expressions should get parentheses"""
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # x - (y + z)
        inner_add = tm.Add(l=y, r=z)
        expr = tm.Add(l=x, r=tm.Mul(l=tm.Integer(n=-1), r=inner_add))

        latex_result = expr.latex()

        # Should have parentheses around (y + z)
        assert "\\left(" in latex_result and "\\right)" in latex_result
        assert "--" not in latex_result
        assert "x - \\left(y + z\\right)" == latex_result

    def test_negative_mul_complex_gets_parentheses(self):
        """Negative complex Mul expressions should get parentheses"""
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # x - (y * z) where the multiplication is not just -1 * something
        inner_mul = tm.Mul(l=y, r=z)
        expr = tm.Add(l=x, r=tm.Mul(l=tm.Integer(n=-1), r=inner_mul))

        latex_result = expr.latex()

        # Should have parentheses around the multiplication
        assert "\\left(" in latex_result and "\\right)" in latex_result
        assert "--" not in latex_result

    def test_negative_simple_mul_no_extra_parentheses(self):
        """Simple negative multiplications like -2x should not get extra parentheses"""
        x = tm.Symbol(s="x")
        # This creates: x + (-2 * x) = x - 2x
        expr = tm.Add(l=x, r=tm.Mul(l=tm.Integer(n=-2), r=x))

        latex_result = expr.latex()

        # Should be "x -2x" (the Mul.latex() handles -2*x as "-2x")
        # No extra parentheses needed
        assert "\\left(" not in latex_result

    def test_nested_complex_expressions(self):
        """Test deeply nested expressions"""
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # x - ((y + 1) + 2)
        inner_add1 = tm.Add(l=y, r=tm.Integer(n=1))
        inner_add2 = tm.Add(l=inner_add1, r=tm.Integer(n=2))
        expr = tm.Add(l=x, r=tm.Mul(l=tm.Integer(n=-1), r=inner_add2))

        latex_result = expr.latex()

        # Should have parentheses and no double minus
        assert "\\left(" in latex_result and "\\right)" in latex_result
        assert "--" not in latex_result

    def test_positive_complex_expressions_unchanged(self):
        """Positive complex expressions should not be affected"""
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # x + (y + z) - should remain unchanged
        inner_add = tm.Add(l=y, r=z)
        expr = tm.Add(l=x, r=inner_add)

        latex_result = expr.latex()

        # Should be "x + y + z" (no extra parentheses for positive expressions)
        assert latex_result == "x + y + z"
        assert "\\left(" not in latex_result
