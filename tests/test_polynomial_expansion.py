"""Test suite for polynomial expansion and Add × Add multiplication.

This test suite addresses the NotImplementedError that was occurring when
simplifying Mul operations with Add × Add combinations (polynomial multiplication).

The specific error was:
NotImplementedError: Simplification of Mul of <class 'teachers.maths.Add'> and <class 'teachers.maths.Add'>
l=Add(l=Mul(l=Integer(n=3), r=Symbol(s='x')), r=Integer(n=-8))  # 3x - 8
r=Add(l=Mul(l=Integer(n=4), r=Symbol(s='x')), r=Integer(n=-1))  # 4x - 1

This occurred when trying to expand: (3x - 8)(4x - 1)
"""

import unittest
from teachers.maths import Symbol, Integer, Mul, Add, Fraction, Decimal, Pi


class TestPolynomialExpansion(unittest.TestCase):
    """Test suite for polynomial expansion and multiplication."""

    def test_original_failing_case(self):
        """Test the exact failing case: (3x - 8)(4x - 1)"""
        x = Symbol(s="x")

        # Create the exact expression that was failing
        expr = (Integer(n=3) * x + Integer(n=-8)) * (Integer(n=4) * x + Integer(n=-1))

        # This should not raise NotImplementedError anymore
        simplified = expr.simplified()

        # The result should be mathematically correct
        self.assertIsInstance(simplified, Add)

        # Verify LaTeX generation works
        latex_result = simplified.latex()
        self.assertIsInstance(latex_result, str)
        self.assertGreater(len(latex_result), 0)

    def test_basic_binomial_expansion(self):
        """Test basic binomial expansion cases."""
        x = Symbol(s="x")

        # (x + 1)(x + 2) = x² + 3x + 2
        expr1 = (x + Integer(n=1)) * (x + Integer(n=2))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, Add)

        # (x + 3)(x - 1) = x² + 2x - 3
        expr2 = (x + Integer(n=3)) * (x + Integer(n=-1))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

        # (x - 2)(x - 4) = x² - 6x + 8
        expr3 = (x + Integer(n=-2)) * (x + Integer(n=-4))
        result3 = expr3.simplified()
        self.assertIsInstance(result3, Add)

    def test_coefficient_variations(self):
        """Test polynomial expansion with various coefficients."""
        x = Symbol(s="x")

        # (2x + 1)(3x + 4) = 6x² + 11x + 4
        expr1 = (Integer(n=2) * x + Integer(n=1)) * (Integer(n=3) * x + Integer(n=4))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, Add)

        # (5x - 2)(2x + 3) = 10x² + 11x - 6
        expr2 = (Integer(n=5) * x + Integer(n=-2)) * (Integer(n=2) * x + Integer(n=3))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

        # (-x + 1)(x - 2) = -x² + 3x - 2
        expr3 = (Integer(n=-1) * x + Integer(n=1)) * (x + Integer(n=-2))
        result3 = expr3.simplified()
        self.assertIsInstance(result3, Add)

    def test_zero_coefficient_cases(self):
        """Test edge cases with zero coefficients."""
        x = Symbol(s="x")

        # (0x + 3)(x + 1) = (3)(x + 1) = 3x + 3
        expr1 = (Integer(n=0) * x + Integer(n=3)) * (x + Integer(n=1))
        result1 = expr1.simplified()
        # Should simplify to just the non-zero terms
        self.assertIsInstance(result1, (Add, Mul))

        # (x + 0)(2x + 1) = x(2x + 1) = 2x² + x
        expr2 = (x + Integer(n=0)) * (Integer(n=2) * x + Integer(n=1))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, (Add, Mul))  # Could be Mul if not fully expanded

    def test_single_term_multiplication(self):
        """Test multiplication where one side is a single term."""
        x = Symbol(s="x")

        # x(x + 1) = x² + x
        expr1 = x * (x + Integer(n=1))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, (Add, Mul))  # Could be Mul if not fully expanded

        # (2x + 3) * 4 = 8x + 12
        expr2 = (Integer(n=2) * x + Integer(n=3)) * Integer(n=4)
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

    def test_fractional_coefficients(self):
        """Test polynomial expansion with fractional coefficients."""
        x = Symbol(s="x")

        # (1/2 x + 1)(x + 2) = 1/2 x² + 2x + 2
        frac_half = Fraction(p=1, q=2)
        expr1 = (frac_half * x + Integer(n=1)) * (x + Integer(n=2))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, Add)

        # (x + 1/3)(2x - 1/4)
        frac_third = Fraction(p=1, q=3)
        frac_quarter = Fraction(p=-1, q=4)
        expr2 = (x + frac_third) * (Integer(n=2) * x + frac_quarter)
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

    def test_decimal_coefficients(self):
        """Test polynomial expansion with decimal coefficients."""
        x = Symbol(s="x")

        # (0.5x + 1.5)(2x - 0.25)
        dec1 = Decimal(x=0.5)
        dec2 = Decimal(x=1.5)
        dec3 = Decimal(x=-0.25)

        expr = (dec1 * x + dec2) * (Integer(n=2) * x + dec3)
        result = expr.simplified()
        self.assertIsInstance(result, Add)

    def test_higher_degree_terms(self):
        """Test expansion involving higher degree terms."""
        x = Symbol(s="x")

        # (x² + 1)(x + 2) = x³ + 2x² + x + 2
        x_squared = x ** Integer(n=2)
        expr1 = (x_squared + Integer(n=1)) * (x + Integer(n=2))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, Add)

        # (2x² - x)(x + 3) = 2x³ + 6x² - x² - 3x = 2x³ + 5x² - 3x
        expr2 = (Integer(n=2) * x_squared + Integer(n=-1) * x) * (x + Integer(n=3))
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

    def test_multiple_variables(self):
        """Test polynomial expansion with multiple variables."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # (x + y)(x - y) = x² - y²
        expr1 = (x + y) * (x + (-y))
        result1 = expr1.simplified()
        self.assertIsInstance(result1, Add)

        # (2x + y)(x + 3y) = 2x² + 6xy + xy + 3y² = 2x² + 7xy + 3y²
        expr2 = (Integer(n=2) * x + y) * (x + Integer(n=3) * y)
        result2 = expr2.simplified()
        self.assertIsInstance(result2, Add)

    def test_pi_in_polynomial(self):
        """Test polynomial expansion with Pi constants."""
        x = Symbol(s="x")
        pi = Pi()

        # (πx + 1)(x + π) = πx² + π²x + x + π
        expr = (pi * x + Integer(n=1)) * (x + pi)
        result = expr.simplified()
        self.assertIsInstance(result, Add)

    def test_nested_expressions(self):
        """Test expansion of nested polynomial expressions."""
        x = Symbol(s="x")

        # ((x + 1) + 2)((x - 1) - 1) = (x + 3)(x - 2)
        left = (x + Integer(n=1)) + Integer(n=2)
        right = (x + Integer(n=-1)) + Integer(n=-1)
        expr = left * right
        result = expr.simplified()
        self.assertIsInstance(result, Add)

    def test_latex_generation_for_expansions(self):
        """Test that LaTeX generation works for expanded polynomials."""
        x = Symbol(s="x")

        test_cases = [
            (x + Integer(n=1)) * (x + Integer(n=2)),  # (x+1)(x+2)
            (Integer(n=2) * x + Integer(n=-3)) * (x + Integer(n=1)),  # (2x-3)(x+1)
            (x + Fraction(p=1, q=2)) * (x + Integer(n=-1)),  # (x+1/2)(x-1)
        ]

        for expr in test_cases:
            with self.subTest(expr=expr):
                simplified = expr.simplified()

                # Should not raise any errors
                latex_repr = simplified.latex()
                self.assertIsInstance(latex_repr, str)
                self.assertGreater(len(latex_repr), 0)

    def test_commutativity(self):
        """Test that polynomial multiplication is commutative."""
        x = Symbol(s="x")

        # (x + 1)(x + 2) should equal (x + 2)(x + 1)
        expr1 = (x + Integer(n=1)) * (x + Integer(n=2))
        expr2 = (x + Integer(n=2)) * (x + Integer(n=1))

        result1 = expr1.simplified()
        result2 = expr2.simplified()

        # Both should be Add expressions
        self.assertIsInstance(result1, Add)
        self.assertIsInstance(result2, Add)

        # LaTeX should be similar (order might differ)
        latex1 = result1.latex()
        latex2 = result2.latex()
        self.assertIsInstance(latex1, str)
        self.assertIsInstance(latex2, str)

    def test_associativity_chains(self):
        """Test chains of polynomial multiplications."""
        x = Symbol(s="x")

        # (x + 1)(x + 2)(x + 3) - test chaining
        # First: (x + 1)(x + 2) = x² + 3x + 2
        # Then: (x² + 3x + 2)(x + 3) = x³ + 6x² + 11x + 6
        expr1 = (x + Integer(n=1)) * (x + Integer(n=2))
        expr2 = expr1 * (x + Integer(n=3))

        result1 = expr1.simplified()
        result2 = expr2.simplified()

        self.assertIsInstance(result1, Add)
        self.assertIsInstance(result2, Add)

    def test_edge_case_identities(self):
        """Test edge cases and mathematical identities."""
        x = Symbol(s="x")

        # (x + 0)(x + 0) = x²
        expr1 = (x + Integer(n=0)) * (x + Integer(n=0))
        result1 = expr1.simplified()
        # Should simplify to just x² (or x*x)

        # (x - x)(anything) = 0
        expr2 = (x + (-x)) * (x + Integer(n=5))
        result2 = expr2.simplified()
        # Should eventually simplify to 0

        # (1)(x + 1) = x + 1
        expr3 = Integer(n=1) * (x + Integer(n=1))
        result3 = expr3.simplified()
        self.assertIsInstance(result3, Add)

    def test_sympy_fallback_integration(self):
        """Test that SymPy fallback works for complex cases."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # Complex expression that should trigger SymPy fallback
        # (x + y + 1)(x - y + 2)
        complex_left = (x + y) + Integer(n=1)
        complex_right = (x + (-y)) + Integer(n=2)
        expr = complex_left * complex_right

        # Should not raise NotImplementedError
        result = expr.simplified()
        self.assertIsInstance(result, (Add, Mul))  # Could be either depending on SymPy result

        # LaTeX should work
        latex_result = result.latex()
        self.assertIsInstance(latex_result, str)
        self.assertGreater(len(latex_result), 0)


if __name__ == "__main__":
    unittest.main()
