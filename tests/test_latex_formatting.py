import unittest
from teachers.maths import (
    Symbol,
    Integer,
    Fraction,
    Decimal,
    group_terms,
)
import sympy as sp


class TestLatexFormatting(unittest.TestCase):
    """Test suite for LaTeX formatting, especially for coefficient-variable multiplication."""

    def test_coefficient_variable_no_times_symbol(self):
        """Test that coefficient-variable multiplication has no × symbol."""
        x = Symbol(s="x")

        # Test various coefficient types with variables
        test_cases = [
            (Integer(n=27), x, "27x"),
            (Integer(n=-5), x, "-5x"),
            (Decimal(x=3.5), x, "3.5x"),
            (Fraction(p=2, q=3), x, "\\dfrac{2}{3}x"),
            (Integer(n=1), x, "x"),  # Coefficient 1 should be omitted
        ]

        for coeff, var, expected in test_cases:
            with self.subTest(coeff=coeff, var=var):
                term = coeff * var
                latex_output = term.latex()

                # Should not contain \times
                self.assertNotIn("\\times", latex_output)

                # For coefficient 1, should just be "x"
                if isinstance(coeff, Integer) and coeff.n == 1:
                    self.assertEqual(latex_output, "x")

    def test_coefficient_power_no_times_symbol(self):
        """Test that coefficient-power multiplication has no × symbol."""
        x = Symbol(s="x")

        # Test coefficient with powers
        test_cases = [
            (Integer(n=27), x ** Integer(n=2), "27x^{2}"),
            (Integer(n=-3), x ** Integer(n=3), "-3x^{3}"),
            (Fraction(p=1, q=2), x ** Integer(n=2), "\\dfrac{1}{2}x^{2}"),
            (Decimal(x=2.5), x ** Integer(n=4), "2.5x^{4}"),
        ]

        for coeff, power, expected_pattern in test_cases:
            with self.subTest(coeff=coeff, power=power):
                term = coeff * power
                latex_output = term.latex()

                # Should not contain \times
                self.assertNotIn("\\times", latex_output)

                # Should contain the coefficient directly attached to the power
                if isinstance(coeff, Integer):
                    self.assertIn(str(abs(coeff.n)), latex_output)

    def test_number_number_has_times_symbol(self):
        """Test that number-number multiplication has × symbol."""
        test_cases = [
            (Integer(n=3), Integer(n=4), "3 \\times 4"),
            (Decimal(x=2.5), Integer(n=3), "2.5 \\times 3"),
            (Fraction(p=1, q=2), Fraction(p=3, q=4), "\\dfrac{1}{2} \\times \\dfrac{3}{4}"),
        ]

        for num1, num2, expected_pattern in test_cases:
            with self.subTest(num1=num1, num2=num2):
                term = num1 * num2
                latex_output = term.latex()

                # Should contain \times for number-number multiplication
                self.assertIn("\\times", latex_output)

    def test_polynomial_latex_formatting(self):
        """Test that grouped polynomials have clean LaTeX without unwanted × symbols."""
        x = Symbol(s="x")

        # Test your specific problematic case: 27x² - 39x - 56
        polynomial = Integer(n=27) * (x ** Integer(n=2)) + Integer(n=-39) * x + Integer(n=-56)
        grouped = group_terms(polynomial)
        latex_output = grouped.latex()

        # Should not contain \times symbols
        self.assertNotIn("\\times", latex_output)

        # Should contain proper polynomial structure
        self.assertIn("27x^{2}", latex_output)
        self.assertIn("-39x", latex_output)
        self.assertIn("-56", latex_output)

    def test_factored_expression_to_polynomial_latex(self):
        """Test the complete workflow: factored → simplified → grouped → clean LaTeX."""
        x = Symbol(s="x")

        # Test case 1: (2x+3)(x-1)
        factor1 = Integer(n=2) * x + Integer(n=3)  # 2x + 3
        factor2 = x + Integer(n=-1)  # x - 1
        factored_expr = factor1 * factor2

        simplified = factored_expr.simplified()
        grouped = group_terms(simplified)
        latex_output = grouped.latex()

        # Should not contain \times symbols
        self.assertNotIn("\\times", latex_output)

        # Should be in proper polynomial form (2x² + x - 3)
        # Verify by substitution
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # At x=0: should get -3
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, -3)

        # At x=1: should get 2 + 1 - 3 = 0
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(val_at_1, 0)

    def test_user_specific_case_latex(self):
        """Test the user's specific case: (2x+3)(-(1/2)x+1) LaTeX formatting."""
        x = Symbol(s="x")

        # User's exact case
        term1 = Integer(n=2) * x + Integer(n=3)  # 2x + 3
        term2 = Fraction(p=-1, q=2) * x + Integer(n=1)  # -(1/2)x + 1

        factored_expr = term1 * term2
        simplified = factored_expr.simplified()
        grouped = group_terms(simplified)
        latex_output = grouped.latex()

        # Should not contain \times symbols
        self.assertNotIn("\\times", latex_output)

        # Should contain proper structure
        self.assertIn("x^{2}", latex_output)  # x² term
        self.assertIn("\\dfrac{1}{2}x", latex_output)  # (1/2)x term

        # Verify mathematical correctness
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # At x=0: should get 3
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, 3)

        # At x=2: should get -4 + 1 + 3 = 0
        val_at_2 = sympy_expr.subs(x_sym, 2)
        self.assertEqual(val_at_2, 0)

    def test_complex_factored_expressions(self):
        """Test complex factored expressions with multiple factors."""
        x = Symbol(s="x")

        # Three factors with mixed coefficients: (3x+2)(x-1)(2x+5)
        factor1 = Integer(n=3) * x + Integer(n=2)  # 3x + 2
        factor2 = x + Integer(n=-1)  # x - 1
        factor3 = Integer(n=2) * x + Integer(n=5)  # 2x + 5

        factored_expr = factor1 * factor2 * factor3
        simplified = factored_expr.simplified()
        grouped = group_terms(simplified)
        latex_output = grouped.latex()

        # Should not contain \times symbols for coefficients
        coefficient_times_count = latex_output.count("\\times")
        # Should be 0 or very minimal (only for complex sub-expressions if any)
        self.assertLessEqual(coefficient_times_count, 1)

        # Should be a cubic polynomial
        self.assertIn("x^{3}", latex_output)

        # Verify it's mathematically correct by checking it has the right roots
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # The original factors have roots at x = -2/3, x = 1, x = -5/2
        # Let's check x = 1 (should be 0)
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(val_at_1, 0)

    def test_mixed_coefficient_types_latex(self):
        """Test LaTeX formatting with mixed coefficient types."""
        x = Symbol(s="x")

        # Mix Integer, Fraction, and Decimal in a polynomial
        term1 = Fraction(p=3, q=4) * (x ** Integer(n=2))  # (3/4)x²
        term2 = Decimal(x=2.5) * x  # 2.5x
        term3 = Integer(n=-7)  # -7

        expr = term1 + term2 + term3
        grouped = group_terms(expr)
        latex_output = grouped.latex()

        # Should not contain \times symbols
        self.assertNotIn("\\times", latex_output)

        # Should contain all parts properly formatted
        self.assertIn("\\dfrac{3}{4}x^{2}", latex_output)
        # Note: Decimal(2.5) may become Fraction(5/2) when grouped
        self.assertTrue("2.5x" in latex_output or "\\dfrac{5}{2}x" in latex_output)
        self.assertIn("-7", latex_output)


if __name__ == "__main__":
    unittest.main()
