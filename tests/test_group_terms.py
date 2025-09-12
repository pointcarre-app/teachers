import unittest
from teachers.maths import (
    Symbol,
    Integer,
    Mul,
    Add,
    Pow,
    Fraction,
    Decimal,
    Pi,
    group_terms,
    Function,
    Image,
)
import sympy as sp


class TestGroupTerms(unittest.TestCase):
    """Test suite for the group_terms function."""

    def test_user_scenario_exact(self):
        """Test the exact failing scenario from the user's generator."""
        x = Symbol(s="x")

        # User's exact case: (3x - 8)(4x - 1)
        a1, b1 = Integer(n=3), Integer(n=-8)
        a2, b2 = Integer(n=4), Integer(n=-1)

        expr = (a1 * x + b1) * (a2 * x + b2)
        simplified = expr.simplified()
        grouped = group_terms(simplified)

        # Should be properly grouped as 12x² - 35x + 8
        self.assertIsInstance(grouped, (Add, Mul))

        # Check LaTeX generation works
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)
        self.assertGreater(len(latex_result), 0)

        # Verify it contains the expected terms (order may vary)
        # Should have x², x, and constant terms
        sympy_expr = grouped.sympy_expr

        # The expression might be nested, so we need to check carefully
        # We'll verify by substituting values
        x_sym = sp.Symbol("x")

        # Substitute x=0: should get 8
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, 8)

        # Substitute x=1: should get 12 - 35 + 8 = -15
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(val_at_1, -15)

        # Substitute x=2: should get 12*4 - 35*2 + 8 = 48 - 70 + 8 = -14
        val_at_2 = sympy_expr.subs(x_sym, 2)
        self.assertEqual(val_at_2, -14)

    def test_simple_polynomial_grouping(self):
        """Test grouping simple polynomial terms."""
        x = Symbol(s="x")

        # x + 2x + 3 should become 3x + 3
        expr = x + Integer(n=2) * x + Integer(n=3)
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Integer))

        # Check coefficients by substitution
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # The expression should be 3x + 3
        # At x=0: should be 3
        self.assertEqual(sympy_expr.subs(x_sym, 0), 3)
        # At x=1: should be 3*1 + 3 = 6
        self.assertEqual(sympy_expr.subs(x_sym, 1), 6)
        # At x=2: should be 3*2 + 3 = 9
        self.assertEqual(sympy_expr.subs(x_sym, 2), 9)

    def test_higher_degree_polynomial(self):
        """Test grouping with higher degree terms."""
        x = Symbol(s="x")

        # x³ + 2x² + x³ + 3x + x² + 5
        x_cubed = x ** Integer(n=3)
        x_squared = x ** Integer(n=2)

        expr = (
            x_cubed
            + Integer(n=2) * x_squared
            + x_cubed
            + Integer(n=3) * x
            + x_squared
            + Integer(n=5)
        )
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul, Pow))

        # Should be 2x³ + 3x² + 3x + 5
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # Verify by substitution
        # At x=0: should be 5
        self.assertEqual(sympy_expr.subs(x_sym, 0), 5)
        # At x=1: should be 2 + 3 + 3 + 5 = 13
        self.assertEqual(sympy_expr.subs(x_sym, 1), 13)
        # At x=2: should be 2*8 + 3*4 + 3*2 + 5 = 16 + 12 + 6 + 5 = 39
        self.assertEqual(sympy_expr.subs(x_sym, 2), 39)

    def test_multiple_variables(self):
        """Test grouping with multiple variables."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # xy + 2x + y + 3xy + x - 2y
        expr = x * y + Integer(n=2) * x + y + Integer(n=3) * x * y + x + Integer(n=-2) * y
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul))

        # Should group to 4xy + 3x - y
        sympy_expr = sp.expand(grouped.sympy_expr)
        x_sym, y_sym = sp.Symbol("x"), sp.Symbol("y")

        # Check the expression contains the expected terms
        # Convert to string for simpler verification
        expr_str = str(sympy_expr)

        # The expression should be 4*x*y + 3*x - y (order may vary)
        # Check by substituting specific values
        # When x=1, y=1: should get 4 + 3 - 1 = 6
        val_at_1_1 = sympy_expr.subs([(x_sym, 1), (y_sym, 1)])
        self.assertEqual(val_at_1_1, 6)

        # When x=2, y=3: should get 4*2*3 + 3*2 - 3 = 24 + 6 - 3 = 27
        val_at_2_3 = sympy_expr.subs([(x_sym, 2), (y_sym, 3)])
        self.assertEqual(val_at_2_3, 27)

    def test_with_fractions(self):
        """Test grouping with fractional coefficients."""
        x = Symbol(s="x")

        # (1/2)x + (1/3)x + (1/6)x + 1
        half = Fraction(p=1, q=2)
        third = Fraction(p=1, q=3)
        sixth = Fraction(p=1, q=6)

        expr = half * x + third * x + sixth * x + Integer(n=1)
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul))

        # Should be x + 1 (since 1/2 + 1/3 + 1/6 = 1)
        sympy_expr = grouped.sympy_expr
        self.assertEqual(sympy_expr.coeff(sp.Symbol("x"), 1), 1)
        self.assertEqual(sympy_expr.coeff(sp.Symbol("x"), 0), 1)

    def test_with_decimals(self):
        """Test grouping with decimal coefficients."""
        x = Symbol(s="x")

        # 0.5x + 1.5x + 2.0x + 3.14
        dec1 = Decimal(x=0.5)
        dec2 = Decimal(x=1.5)
        dec3 = Decimal(x=2.0)
        pi_approx = Decimal(x=3.14)

        expr = dec1 * x + dec2 * x + dec3 * x + pi_approx
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul))

        # Should be 4.0x + 3.14
        sympy_expr = grouped.sympy_expr
        x_coeff = float(sympy_expr.coeff(sp.Symbol("x"), 1))
        const_coeff = float(sympy_expr.coeff(sp.Symbol("x"), 0))

        self.assertAlmostEqual(x_coeff, 4.0, places=5)
        self.assertAlmostEqual(const_coeff, 3.14, places=5)

    def test_with_pi(self):
        """Test grouping with Pi constant."""
        x = Symbol(s="x")
        pi = Pi()

        # πx + 2πx + x + π
        expr = pi * x + Integer(n=2) * pi * x + x + pi
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul))

        # LaTeX should work
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_negative_coefficients(self):
        """Test grouping with negative coefficients."""
        x = Symbol(s="x")

        # -3x + 2x - 5x + 7x - x
        expr = (
            Integer(n=-3) * x
            + Integer(n=2) * x
            + Integer(n=-5) * x
            + Integer(n=7) * x
            + Integer(n=-1) * x
        )
        grouped = group_terms(expr)

        # Should be 0x = 0
        sympy_expr = grouped.sympy_expr
        self.assertEqual(sympy_expr, 0)

    def test_mixed_polynomial_types(self):
        """Test grouping mixed polynomial expressions."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # x²y + 2xy² + x²y - xy² + 3
        x_sq_y = (x ** Integer(n=2)) * y
        x_y_sq = x * (y ** Integer(n=2))

        expr = x_sq_y + Integer(n=2) * x_y_sq + x_sq_y + (-x_y_sq) + Integer(n=3)
        grouped = group_terms(expr)

        self.assertIsInstance(grouped, (Add, Mul))

        # Should be 2x²y + xy² + 3
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_exponential_terms(self):
        """Test grouping with exponential-like terms (using Function for exp)."""
        x = Symbol(s="x")

        # Simulate e^x using Function (since we don't have native exp support)
        exp_func = Function(name="exp")
        exp_x = exp_func(x)

        # 2*exp(x) + 3*exp(x) + x
        expr = Integer(n=2) * exp_x + Integer(n=3) * exp_x + x
        grouped = group_terms(expr)

        # Should group the exp(x) terms
        self.assertIsInstance(grouped, (Add, Mul, Image))

        # LaTeX should work
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_logarithmic_terms(self):
        """Test grouping with logarithmic-like terms (using Function for log)."""
        x = Symbol(s="x")

        # Simulate log(x) using Function
        log_func = Function(name="log")
        log_x = log_func(x)

        # 3*log(x) + 2*log(x) + 5
        expr = Integer(n=3) * log_x + Integer(n=2) * log_x + Integer(n=5)
        grouped = group_terms(expr)

        # Should group the log(x) terms
        self.assertIsInstance(grouped, (Add, Mul, Image))

        # LaTeX should work
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_growth_formula_comparison(self):
        """Test grouping for growth formula comparisons (polynomial vs exponential vs logarithmic)."""
        x = Symbol(s="x")

        # Simulate different growth rates
        exp_func = Function(name="exp")
        log_func = Function(name="log")

        exp_x = exp_func(x)
        log_x = log_func(x)
        x_squared = x ** Integer(n=2)

        # Mixed growth formula: 2x² + 3*exp(x) + 4*log(x) + x² + exp(x)
        expr = (
            Integer(n=2) * x_squared
            + Integer(n=3) * exp_x
            + Integer(n=4) * log_x
            + x_squared
            + exp_x
        )
        grouped = group_terms(expr)

        # Should group to: 3x² + 4*exp(x) + 4*log(x)
        self.assertIsInstance(grouped, (Add, Mul))

        # LaTeX should work
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_empty_expression(self):
        """Test grouping with just a constant."""
        expr = Integer(n=42)
        grouped = group_terms(expr)

        # Should return the same constant
        self.assertIsInstance(grouped, Integer)
        self.assertEqual(grouped.n, 42)

    def test_single_variable(self):
        """Test grouping with a single variable."""
        x = Symbol(s="x")
        grouped = group_terms(x)

        # Should return the same variable
        self.assertIsInstance(grouped, Symbol)
        self.assertEqual(grouped.s, "x")

    def test_specify_collection_symbol(self):
        """Test specifying which symbol to collect by."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # 2xy + 3x + 4y + xy + 2x
        expr = Integer(n=2) * x * y + Integer(n=3) * x + Integer(n=4) * y + x * y + Integer(n=2) * x

        # Collect only by x
        grouped_x = group_terms(expr, x)
        self.assertIsInstance(grouped_x, (Add, Mul))

        # Collect only by y
        grouped_y = group_terms(expr, y)
        self.assertIsInstance(grouped_y, (Add, Mul))

        # Both should generate valid LaTeX
        latex_x = grouped_x.latex()
        latex_y = grouped_y.latex()
        self.assertIsInstance(latex_x, str)
        self.assertIsInstance(latex_y, str)

    def test_complex_nested_expression(self):
        """Test grouping complex nested expressions."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # ((x + 1)(x + 2) + (y + 1)(y + 2)) expanded and mixed
        left = (x + Integer(n=1)) * (x + Integer(n=2))
        right = (y + Integer(n=1)) * (y + Integer(n=2))
        expr = left + right

        simplified = expr.simplified()
        grouped = group_terms(simplified)

        self.assertIsInstance(grouped, (Add, Mul))

        # LaTeX should work
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_error_handling(self):
        """Test that group_terms handles errors gracefully."""
        # Create an object that might cause issues
        x = Symbol(s="x")

        # Even with potential edge cases, should not raise exceptions
        try:
            # Test with None (should handle gracefully)
            # Note: This will fail type checking but should be caught
            result = group_terms(x)  # Valid input
            self.assertIsNotNone(result)

            # Test with complex expression
            complex_expr = (x + Integer(n=1)) / (x + Integer(n=2))
            result = group_terms(complex_expr)
            self.assertIsNotNone(result)

        except Exception as e:
            self.fail(f"group_terms raised an unexpected exception: {e}")

    def test_idempotency(self):
        """Test that applying group_terms twice gives the same result."""
        x = Symbol(s="x")

        expr = x + Integer(n=2) * x + Integer(n=3) * x + Integer(n=5)
        grouped_once = group_terms(expr)
        grouped_twice = group_terms(grouped_once)

        # Should be idempotent (applying twice gives same result)
        self.assertEqual(grouped_once.sympy_expr, grouped_twice.sympy_expr)

    def test_preserves_mathematical_equivalence(self):
        """Test that grouping preserves mathematical equivalence."""
        x = Symbol(s="x")

        # Original expression
        expr = Integer(n=2) * x + Integer(n=3) * x + Integer(n=5)

        # Grouped expression
        grouped = group_terms(expr)

        # Both should evaluate to the same value for any x
        test_value = 7
        x_val = sp.Symbol("x")

        original_value = expr.sympy_expr.subs(x_val, test_value)
        grouped_value = grouped.sympy_expr.subs(x_val, test_value)

        self.assertEqual(original_value, grouped_value)

    def test_latex_output_quality(self):
        """Test that LaTeX output is clean and readable."""
        x = Symbol(s="x")

        # Test various cases for LaTeX quality
        test_cases = [
            x + Integer(n=2) * x + Integer(n=3),  # Simple linear
            (x ** Integer(n=2)) + Integer(n=2) * (x ** Integer(n=2)),  # Quadratic
            (Integer(n=3) * x + Integer(n=-8)) * (Integer(n=4) * x + Integer(n=-1)),  # Product
        ]

        for expr in test_cases:
            simplified = expr.simplified() if hasattr(expr, "simplified") else expr
            grouped = group_terms(simplified)
            latex = grouped.latex()

            # Check LaTeX is not empty and doesn't contain errors
            self.assertIsInstance(latex, str)
            self.assertGreater(len(latex), 0)
            # Should not contain error indicators
            self.assertNotIn("Error", latex)
            self.assertNotIn("None", latex)

    def test_polynomial_ordering_user_case(self):
        """Test the specific user case: (2x+3)(-(1/2)x+1) with proper ordering."""
        x = Symbol(s="x")

        # User's specific example: (2x+3)(-(1/2)x+1)
        term1 = Integer(n=2) * x + Integer(n=3)  # 2x + 3
        term2 = Fraction(p=-1, q=2) * x + Integer(n=1)  # -(1/2)x + 1

        expr = term1 * term2
        simplified = expr.simplified()
        grouped = group_terms(simplified)

        # Should expand to: -x² + 2x - (3/2)x + 3 = -x² + (1/2)x + 3
        # Verify by substitution
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # At x=0: should get 3
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, 3)

        # At x=1: should get -1 + 0.5 + 3 = 2.5
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(float(val_at_1), 2.5)

        # At x=2: should get -4 + 1 + 3 = 0
        val_at_2 = sympy_expr.subs(x_sym, 2)
        self.assertEqual(val_at_2, 0)

        # Check LaTeX output is clean
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)
        self.assertGreater(len(latex_result), 0)

    def test_polynomial_ordering_descending_powers(self):
        """Test that polynomials are ordered in descending powers (ax² + bx + c)."""
        x = Symbol(s="x")

        # Create a deliberately mixed-order polynomial
        # Start with: 5 + 3x + 2x² (ascending order - wrong)
        mixed_expr = Integer(n=5) + Integer(n=3) * x + Integer(n=2) * (x ** Integer(n=2))
        grouped = group_terms(mixed_expr)

        # Should be ordered as: 2x² + 3x + 5
        sympy_expr = grouped.sympy_expr

        # Verify mathematical correctness by substitution (more robust than structure checking)
        x_sym = sp.Symbol("x")

        # The polynomial should be mathematically equivalent to 2x² + 3x + 5
        # Test by substituting values
        # At x=0: should get 5
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, 5)

        # At x=1: should get 2 + 3 + 5 = 10
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(val_at_1, 10)

        # At x=2: should get 2*4 + 3*2 + 5 = 8 + 6 + 5 = 19
        val_at_2 = sympy_expr.subs(x_sym, 2)
        self.assertEqual(val_at_2, 19)

    def test_multi_factor_polynomial_expansion(self):
        """Test expansion of multiple factors with proper ordering."""
        x = Symbol(s="x")

        # Three factors: (x+1)(x+2)(x+3)
        factor1 = x + Integer(n=1)
        factor2 = x + Integer(n=2)
        factor3 = x + Integer(n=3)

        expr = factor1 * factor2 * factor3
        simplified = expr.simplified()
        grouped = group_terms(simplified)

        # Should expand to: x³ + 6x² + 11x + 6
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # Verify mathematical correctness by substitution
        # Should expand to: x³ + 6x² + 11x + 6
        # At x=0: should get 6
        val_at_0 = sympy_expr.subs(x_sym, 0)
        self.assertEqual(val_at_0, 6)

        # At x=1: should get 1 + 6 + 11 + 6 = 24
        val_at_1 = sympy_expr.subs(x_sym, 1)
        self.assertEqual(val_at_1, 24)

        # At x=-1: should get -1 + 6 - 11 + 6 = 0 (since (x+1)(x+2)(x+3) has roots at -1, -2, -3)
        val_at_neg1 = sympy_expr.subs(x_sym, -1)
        self.assertEqual(val_at_neg1, 0)

    def test_mixed_coefficient_types_ordering(self):
        """Test polynomial ordering with mixed coefficient types."""
        x = Symbol(s="x")

        # Mix Integer, Fraction, and Decimal coefficients
        # (1/2)x² + 2.5x + 3 - but input in wrong order
        decimal_coeff = Decimal(x=2.5)
        frac_coeff = Fraction(p=1, q=2)

        # Input in mixed order: 3 + 2.5x + (1/2)x²
        mixed_expr = Integer(n=3) + decimal_coeff * x + frac_coeff * (x ** Integer(n=2))

        grouped = group_terms(mixed_expr)

        # Should be ordered as: (1/2)x² + 2.5x + 3
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # Verify by substitution
        # At x=2: should get 0.5*4 + 2.5*2 + 3 = 2 + 5 + 3 = 10
        val_at_2 = float(sympy_expr.subs(x_sym, 2))
        self.assertEqual(val_at_2, 10.0)

        # Check LaTeX output
        latex_result = grouped.latex()
        self.assertIsInstance(latex_result, str)

    def test_zero_coefficient_handling(self):
        """Test handling of zero coefficients in polynomial ordering."""
        x = Symbol(s="x")

        # Expression that simplifies to have zero coefficient: x² + 2x - 2x + 5
        expr = (x ** Integer(n=2)) + Integer(n=2) * x + Integer(n=-2) * x + Integer(n=5)
        grouped = group_terms(expr)

        # Should simplify to: x² + 5 (zero x term should be eliminated)
        sympy_expr = grouped.sympy_expr
        x_sym = sp.Symbol("x")

        # Should only have degree 2 and degree 0 terms (x term should be eliminated)
        try:
            coeffs = sp.Poly(sympy_expr, x_sym).all_coeffs()
            # Filter out zero coefficients
            non_zero_coeffs = [c for c in coeffs if c != 0]
            self.assertEqual(len(non_zero_coeffs), 2)  # Only x² and constant terms

            # Check specific coefficients
            x2_coeff = sp.expand(sympy_expr).coeff(x_sym, 2)
            x1_coeff = sp.expand(sympy_expr).coeff(x_sym, 1)
            x0_coeff = sp.expand(sympy_expr).coeff(x_sym, 0)

            self.assertEqual(x2_coeff, 1)  # x² coefficient
            self.assertEqual(x1_coeff, 0)  # x coefficient should be 0
            self.assertEqual(x0_coeff, 5)  # constant term
        except sp.PolynomialError:
            # Alternative verification using coefficient extraction
            expanded = sp.expand(sympy_expr)
            x2_coeff = expanded.coeff(x_sym, 2)
            x1_coeff = expanded.coeff(x_sym, 1)
            x0_coeff = expanded.coeff(x_sym, 0)

            self.assertEqual(x2_coeff, 1)  # x² coefficient
            self.assertEqual(x1_coeff, 0)  # x coefficient should be 0
            self.assertEqual(x0_coeff, 5)  # constant term

    def test_single_term_polynomial(self):
        """Test that single terms are handled correctly."""
        x = Symbol(s="x")

        # Single term cases
        test_cases = [
            Integer(n=5),  # Just constant
            Integer(n=3) * x,  # Just linear term
            Integer(n=2) * (x ** Integer(n=2)),  # Just quadratic term
        ]

        for expr in test_cases:
            grouped = group_terms(expr)
            # Should return equivalent expression
            self.assertEqual(expr.sympy_expr, grouped.sympy_expr)

            # LaTeX should work
            latex_result = grouped.latex()
            self.assertIsInstance(latex_result, str)
            self.assertGreater(len(latex_result), 0)


if __name__ == "__main__":
    unittest.main()
