#!/usr/bin/env python3

import unittest
import teachers.maths as tm


class TestMultiplicationSymbols(unittest.TestCase):
    """
    Test multiplication symbol rendering in LaTeX output.

    Ensures that the \\times symbol appears correctly in various multiplication scenarios,
    especially after the fix for negative fraction parentheses.
    """

    def test_integer_times_fraction(self):
        """Test Integer × Fraction should have \\times symbol."""
        coef = tm.Integer(n=28)
        frac = tm.Fraction(p=tm.Integer(n=29), q=tm.Integer(n=4))
        mult = coef * frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertEqual(latex_output, "28 \\times \\dfrac{29}{4}")

    def test_integer_times_negative_fraction(self):
        """Test Integer × Negative Fraction should have \\times symbol and parentheses."""
        coef = tm.Integer(n=5)
        neg_frac = tm.Fraction(p=tm.Integer(n=-3), q=tm.Integer(n=7))
        mult = coef * neg_frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertIn("\\left(", latex_output)
        self.assertIn("\\right)", latex_output)
        self.assertEqual(latex_output, "5 \\times \\left(-\\dfrac{3}{7}\\right)")

    def test_fraction_times_fraction(self):
        """Test Fraction × Fraction should have \\times symbol."""
        frac1 = tm.Fraction(p=tm.Integer(n=19), q=tm.Integer(n=5))
        frac2 = tm.Fraction(p=tm.Integer(n=29), q=tm.Integer(n=4))
        mult = frac1 * frac2

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertEqual(latex_output, "\\dfrac{19}{5} \\times \\dfrac{29}{4}")

    def test_fraction_times_negative_fraction(self):
        """Test Fraction × Negative Fraction should have \\times symbol and parentheses."""
        frac1 = tm.Fraction(p=tm.Integer(n=17), q=tm.Integer(n=2))
        neg_frac = tm.Fraction(p=tm.Integer(n=-9), q=tm.Integer(n=10))
        mult = frac1 * neg_frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertIn("\\left(", latex_output)
        self.assertIn("\\right)", latex_output)
        self.assertEqual(latex_output, "\\dfrac{17}{2} \\times \\left(-\\dfrac{9}{10}\\right)")

    def test_decimal_times_fraction(self):
        """Test Decimal × Fraction should have \\times symbol."""
        dec = tm.Decimal(x=2.5)
        frac = tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=4))
        mult = dec * frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertEqual(latex_output, "2.5 \\times \\dfrac{3}{4}")

    def test_decimal_times_negative_fraction(self):
        """Test Decimal × Negative Fraction should have \\times symbol and parentheses."""
        dec = tm.Decimal(x=1.5)
        neg_frac = tm.Fraction(p=tm.Integer(n=-2), q=tm.Integer(n=3))
        mult = dec * neg_frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertIn("\\left(", latex_output)
        self.assertIn("\\right)", latex_output)
        self.assertEqual(latex_output, "1.5 \\times \\left(-\\dfrac{2}{3}\\right)")

    def test_integer_times_integer(self):
        """Test Integer × Integer should have \\times symbol."""
        int1 = tm.Integer(n=7)
        int2 = tm.Integer(n=8)
        mult = int1 * int2

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertEqual(latex_output, "7 \\times 8")

    def test_integer_times_negative_integer(self):
        """Test Integer × Negative Integer should have \\times symbol and parentheses."""
        int1 = tm.Integer(n=6)
        neg_int = tm.Integer(n=-4)
        mult = int1 * neg_int

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertIn("\\left(", latex_output)
        self.assertIn("\\right)", latex_output)
        self.assertEqual(latex_output, "6 \\times \\left(-4\\right)")

    def test_decimal_times_decimal(self):
        """Test Decimal × Decimal should have \\times symbol."""
        dec1 = tm.Decimal(x=2.5)
        dec2 = tm.Decimal(x=1.2)
        mult = dec1 * dec2

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        self.assertEqual(latex_output, "2.5 \\times 1.2")

    def test_coefficient_symbol_no_times(self):
        """Test Integer × Symbol should NOT have \\times symbol (coefficient notation)."""
        coef = tm.Integer(n=5)
        symbol = tm.Symbol(s="x")
        mult = coef * symbol

        latex_output = mult.latex()
        self.assertNotIn("\\times", latex_output)
        self.assertEqual(latex_output, "5x")

    def test_coefficient_one_omitted(self):
        """Test coefficient 1 should be omitted in coefficient × symbol."""
        one = tm.Integer(n=1)
        symbol = tm.Symbol(s="x")
        mult = one * symbol

        latex_output = mult.latex()
        self.assertNotIn("\\times", latex_output)
        self.assertNotIn("1", latex_output)
        self.assertEqual(latex_output, "x")

    def test_coefficient_power_no_times(self):
        """Test Integer × Power should NOT have \\times symbol (coefficient notation)."""
        coef = tm.Integer(n=3)
        symbol = tm.Symbol(s="x")
        power = symbol ** tm.Integer(n=2)
        mult = coef * power

        latex_output = mult.latex()
        self.assertNotIn("\\times", latex_output)
        self.assertEqual(latex_output, "3x^{2}")

    def test_user_scenario_exact(self):
        """Test the exact user scenario: 19/5 + 28 × 29/4."""
        # Create components
        frac1 = tm.Fraction(p=tm.Integer(n=19), q=tm.Integer(n=5))
        coef = tm.Integer(n=28)
        frac2 = tm.Fraction(p=tm.Integer(n=29), q=tm.Integer(n=4))

        # Create multiplication
        mult = coef * frac2
        mult_latex = mult.latex()

        # Verify multiplication has times symbol
        self.assertIn("\\times", mult_latex)
        self.assertEqual(mult_latex, "28 \\times \\dfrac{29}{4}")

        # Create full expression
        expr = frac1 + mult
        expr_latex = expr.latex()

        # Verify full expression
        expected = "\\dfrac{19}{5} + 28 \\times \\dfrac{29}{4}"
        self.assertEqual(expr_latex, expected)

    def test_generator_scenario_integration(self):
        """Test integration with the generator pattern from the user's code."""
        # Simulate the generator pattern
        a = tm.Fraction(p=tm.Integer(n=19), q=tm.Integer(n=5))  # 19/5
        b = tm.Integer(n=28)  # 28
        c = tm.Fraction(p=tm.Integer(n=29), q=tm.Integer(n=4))  # 29/4

        # Create expression: a + b * c
        expr = a + b * c
        latex_output = expr.latex()

        # Should have times symbol in the b * c part
        self.assertIn("\\times", latex_output)
        expected = "\\dfrac{19}{5} + 28 \\times \\dfrac{29}{4}"
        self.assertEqual(latex_output, expected)

    def test_negative_coefficient_scenario(self):
        """Test negative coefficient with fraction."""
        neg_coef = tm.Integer(n=-15)
        frac = tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=3))
        mult = neg_coef * frac

        latex_output = mult.latex()
        self.assertIn("\\times", latex_output)
        # Negative coefficient doesn't need parentheses, only negative right operands do
        self.assertEqual(latex_output, "-15 \\times \\dfrac{7}{3}")

    def test_complex_expression_with_multiple_multiplications(self):
        """Test complex expression with multiple multiplication terms."""
        # (2 × 3/4) + (5 × 7/8)
        mult1 = tm.Integer(n=2) * tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=4))
        mult2 = tm.Integer(n=5) * tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=8))
        expr = mult1 + mult2

        latex_output = expr.latex()

        # Should have times symbols in both multiplication terms
        times_count = latex_output.count("\\times")
        self.assertEqual(times_count, 2)

        expected = "2 \\times \\dfrac{3}{4} + 5 \\times \\dfrac{7}{8}"
        self.assertEqual(latex_output, expected)


if __name__ == "__main__":
    unittest.main()
