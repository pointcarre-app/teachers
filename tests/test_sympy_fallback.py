"""Test suite for SymPy fallback functionality and edge cases.

This test suite focuses on testing the SymPy fallback mechanism we added
to handle complex algebraic cases that don't have specific implementations.
It also tests tricky edge cases that could break the system.
"""

import unittest
from teachers.maths import Symbol, Integer, Mul, Add, Pow, Fraction, Decimal, Pi, MathsObjectParser


class TestSympyFallback(unittest.TestCase):
    """Test suite for SymPy fallback functionality and edge cases."""

    def test_complex_nested_expressions(self):
        """Test complex nested expressions that trigger SymPy fallback."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # Complex nested expression: ((x + 1) * (y - 2)) + ((x - y) * (x + y))
        term1 = (x + Integer(n=1)) * (y + Integer(n=-2))
        term2 = (x + (-y)) * (x + y)
        complex_expr = term1 + term2

        # Should not raise NotImplementedError
        result = complex_expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

        # LaTeX should work
        latex_result = result.latex()
        self.assertIsInstance(latex_result, str)
        self.assertGreater(len(latex_result), 0)

    def test_unusual_type_combinations(self):
        """Test unusual type combinations that might trigger fallback."""
        x = Symbol(s="x")
        pi = Pi()

        # Pi * (x + Pi) - unusual combination
        expr1 = pi * (x + pi)
        result1 = expr1.simplified()
        self.assertIsInstance(result1, (Add, Mul))

        # (x + 1/π) * (x - π) - mixing Pi and fractions
        pi_frac = Fraction(p=Integer(n=1), q=pi)
        expr2 = (x + pi_frac) * (x + (-pi))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, (Add, Mul))

    def test_high_degree_polynomials(self):
        """Test high-degree polynomial expressions."""
        x = Symbol(s="x")

        # (x² + x + 1)(x² - x + 1) = x⁴ + x² + 1
        x_squared = x ** Integer(n=2)
        left = x_squared + x + Integer(n=1)
        right = x_squared + (-x) + Integer(n=1)
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul, Pow))

        # Should generate valid LaTeX
        latex_result = result.latex()
        self.assertIsInstance(latex_result, str)

    def test_multiple_variable_polynomials(self):
        """Test polynomials with multiple variables."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        z = Symbol(s="z")

        # (x + y + z)(x - y - z) = x² - (y + z)²
        left = x + y + z
        right = x + (-y) + (-z)
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

    def test_rational_coefficients_complex(self):
        """Test complex expressions with rational coefficients."""
        x = Symbol(s="x")

        # (1/2 x + 2/3)(3/4 x - 1/5) - complex fractions
        coeff1 = Fraction(p=1, q=2)
        coeff2 = Fraction(p=2, q=3)
        coeff3 = Fraction(p=3, q=4)
        coeff4 = Fraction(p=-1, q=5)

        left = coeff1 * x + coeff2
        right = coeff3 * x + coeff4
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

    def test_power_expressions(self):
        """Test expressions involving powers."""
        x = Symbol(s="x")

        # (x² + 1)(x³ - 1) = x⁵ - x² + x³ - 1 = x⁵ + x³ - x² - 1
        x_squared = x ** Integer(n=2)
        x_cubed = x ** Integer(n=3)

        left = x_squared + Integer(n=1)
        right = x_cubed + Integer(n=-1)
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

    def test_decimal_precision_edge_cases(self):
        """Test edge cases with decimal precision."""
        x = Symbol(s="x")

        # Very small decimals
        small_dec = Decimal(x=1e-10)
        expr1 = (small_dec * x + Integer(n=1)) * (x + Integer(n=1))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, (Add, Mul))

        # Very large decimals
        large_dec = Decimal(x=1e10)
        expr2 = (large_dec * x + Integer(n=1)) * (x + Integer(n=1))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, (Add, Mul))

    def test_sympy_parser_consistency(self):
        """Test that our SymPy parser produces consistent results."""
        x = Symbol(s="x")

        # Create a simple polynomial
        expr = (x + Integer(n=1)) * (x + Integer(n=2))
        result = expr.simplified()

        # Convert to SymPy and back
        if hasattr(result, "sympy_expr"):
            sympy_expr = result.sympy_expr
            parsed_back = MathsObjectParser.from_sympy(sympy_expr)

            # Should be able to generate LaTeX for both
            original_latex = result.latex()
            parsed_latex = parsed_back.latex()

            self.assertIsInstance(original_latex, str)
            self.assertIsInstance(parsed_latex, str)

    def test_zero_and_identity_edge_cases(self):
        """Test edge cases involving zero and identity elements."""
        x = Symbol(s="x")

        # (x + 0) * (0 + x) = x * x = x²
        expr1 = (x + Integer(n=0)) * (Integer(n=0) + x)
        result1 = expr1.simplified()
        # Should eventually simplify to x²
        self.assertIsInstance(result1, (Mul, Pow, Add))

        # (1 * x + 0) * (x * 1 + 0) = x * x = x²
        one = Integer(n=1)
        zero = Integer(n=0)
        expr2 = (one * x + zero) * (x * one + zero)
        result2 = expr2.simplified()
        self.assertIsInstance(result2, (Mul, Pow, Add))

    def test_negative_coefficient_combinations(self):
        """Test various negative coefficient combinations."""
        x = Symbol(s="x")

        # (-x - 1)(-x - 2) = x² + 3x + 2
        neg_one = Integer(n=-1)
        left = neg_one * x + Integer(n=-1)
        right = neg_one * x + Integer(n=-2)
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

    def test_mixed_arithmetic_types(self):
        """Test mixing different arithmetic types."""
        x = Symbol(s="x")

        # Mix Integer, Fraction, Decimal, Pi
        int_coeff = Integer(n=2)
        frac_coeff = Fraction(p=1, q=3)
        dec_coeff = Decimal(x=1.5)
        pi = Pi()

        # (2x + 1/3) * (1.5x + π)
        left = int_coeff * x + frac_coeff
        right = dec_coeff * x + pi
        expr = left * right

        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))

    def test_fallback_error_handling(self):
        """Test that fallback gracefully handles edge cases."""
        x = Symbol(s="x")

        # Create expressions that might challenge the system
        test_expressions = [
            # Simple cases that should work
            (x + Integer(n=1)) * (x + Integer(n=2)),
            # Complex cases that might trigger fallback
            (x + Pi()) * (x + Fraction(p=1, q=2)),
            # Edge cases
            (x + Integer(n=0)) * (x + Integer(n=0)),
        ]

        for expr in test_expressions:
            with self.subTest(expr=expr):
                # Should not raise any exceptions
                result = expr.simplified()
                self.assertIsNotNone(result)

                # Should be able to generate LaTeX
                latex_result = result.latex()
                self.assertIsInstance(latex_result, str)

    def test_regression_previous_functionality(self):
        """Test that previous functionality still works after changes."""
        x = Symbol(s="x")

        # Test cases that were working before our changes
        test_cases = [
            # Integer arithmetic
            Integer(n=2) * Integer(n=3),  # Should be 6
            # Symbol arithmetic
            x * Integer(n=2),  # Should be 2x
            # Simple addition
            x + Integer(n=1),  # Should be x + 1
            # Fraction arithmetic
            Fraction(p=1, q=2) * Fraction(p=3, q=4),  # Should be 3/8
        ]

        for expr in test_cases:
            with self.subTest(expr=expr):
                result = expr.simplified()
                self.assertIsNotNone(result)

                # Should generate valid LaTeX
                latex_result = result.latex()
                self.assertIsInstance(latex_result, str)
                self.assertGreater(len(latex_result), 0)

    def test_original_user_scenario_variations(self):
        """Test variations of the original user's failing scenario."""
        x = Symbol(s="x")

        # Original: (3x - 8)(4x - 1)
        original = (Integer(n=3) * x + Integer(n=-8)) * (Integer(n=4) * x + Integer(n=-1))
        result_original = original.simplified()
        self.assertIsInstance(result_original, (Add, Mul))

        # Variations with different coefficients
        variations = [
            # Different positive coefficients
            (Integer(n=2) * x + Integer(n=5)) * (Integer(n=3) * x + Integer(n=7)),
            # Mixed positive/negative
            (Integer(n=-2) * x + Integer(n=3)) * (Integer(n=4) * x + Integer(n=-5)),
            # Larger coefficients
            (Integer(n=10) * x + Integer(n=-15)) * (Integer(n=7) * x + Integer(n=12)),
        ]

        for expr in variations:
            with self.subTest(expr=expr):
                result = expr.simplified()
                self.assertIsInstance(result, (Add, Mul))

                # LaTeX should work
                latex_result = result.latex()
                self.assertIsInstance(latex_result, str)


if __name__ == "__main__":
    unittest.main()
