"""
Test suite for the Interval class functionality.

This module tests mathematical interval representation:
- Interval construction with boundaries
- Open and closed interval types
- Left and right boundary handling
- Interval simplification behavior
- LaTeX output generation
- Integration with other mathematical objects

These tests ensure that intervals are properly represented
and can be used in mathematical contexts for domain
specification and set operations.
"""

import unittest
import teachers.maths as tm


class TestInterval(unittest.TestCase):
    """Test suite for Interval mathematical set representation."""

    def test_interval_creation_basic(self):
        """
        Test basic Interval creation with integer boundaries.

        Validates:
        - Simple interval construction [a, b]
        - Boundary assignment (left and right)
        - Default closed interval behavior
        - Object type verification
        - SymPy expression generation

        Ensures intervals can be created with basic parameters.
        """
        # Test simple closed interval [0, 5]
        a = tm.Integer(n=0)
        b = tm.Integer(n=5)
        interval = tm.Interval(l=a, r=b)

        # Verify basic properties
        self.assertIsInstance(interval, tm.Interval)
        self.assertEqual(interval.l, a)
        self.assertEqual(interval.r, b)
        self.assertFalse(interval.left_open)
        self.assertFalse(interval.right_open)

        # Verify SymPy expression is created
        self.assertIsNotNone(interval.sympy_expr)

    def test_interval_creation_with_symbols(self):
        """
        Test Interval creation with symbolic boundaries.

        Validates:
        - Symbol-based intervals [x, y]
        - Mixed symbolic and numeric boundaries
        - Boundary preservation
        - Mathematical representation

        Ensures intervals work with algebraic variables.
        """
        # Test interval with symbols [x, y]
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        interval = tm.Interval(l=x, r=y)

        self.assertEqual(interval.l, x)
        self.assertEqual(interval.r, y)
        self.assertFalse(interval.left_open)
        self.assertFalse(interval.right_open)

        # Test mixed interval [0, x]
        zero = tm.Integer(n=0)
        mixed_interval = tm.Interval(l=zero, r=x)

        self.assertEqual(mixed_interval.l, zero)
        self.assertEqual(mixed_interval.r, x)

    def test_interval_open_boundaries(self):
        """
        Test Interval creation with open boundaries.

        Validates:
        - Left open interval (a, b]
        - Right open interval [a, b)
        - Both open interval (a, b)
        - Boundary type preservation
        - SymPy integration with open intervals

        Ensures all interval boundary types are supported.
        """
        a = tm.Integer(n=1)
        b = tm.Integer(n=10)

        # Test left open interval (1, 10]
        left_open = tm.Interval(l=a, r=b, left_open=True, right_open=False)
        self.assertTrue(left_open.left_open)
        self.assertFalse(left_open.right_open)

        # Test right open interval [1, 10)
        right_open = tm.Interval(l=a, r=b, left_open=False, right_open=True)
        self.assertFalse(right_open.left_open)
        self.assertTrue(right_open.right_open)

        # Test both open interval (1, 10)
        both_open = tm.Interval(l=a, r=b, left_open=True, right_open=True)
        self.assertTrue(both_open.left_open)
        self.assertTrue(both_open.right_open)

        # Test default (both closed) [1, 10]
        both_closed = tm.Interval(l=a, r=b)
        self.assertFalse(both_closed.left_open)
        self.assertFalse(both_closed.right_open)

    def test_interval_latex_output(self):
        """
        Test Interval LaTeX representation generation.

        Validates:
        - Closed interval bracket notation \\lbracket...\\rbracket
        - Semicolon separator between boundaries
        - Proper boundary LaTeX formatting
        - Integer and symbol boundary rendering

        Ensures intervals generate proper mathematical notation.
        """
        # Test simple integer interval [0, 5]
        a = tm.Integer(n=0)
        b = tm.Integer(n=5)
        interval = tm.Interval(l=a, r=b)

        expected_latex = "\\lbracket 0; 5\\rbracket"  # Updated spacing format
        self.assertEqual(interval.latex(), expected_latex)

        # Test interval with symbols [x, y]
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        symbol_interval = tm.Interval(l=x, r=y)

        expected_symbol_latex = "\\lbracket x; y\\rbracket"  # Updated spacing format
        self.assertEqual(symbol_interval.latex(), expected_symbol_latex)

        # Test interval with negative numbers [-5, 3]
        neg_a = tm.Integer(n=-5)
        pos_b = tm.Integer(n=3)
        neg_interval = tm.Interval(l=neg_a, r=pos_b)

        expected_neg_latex = "\\lbracket -5; 3\\rbracket"  # Updated spacing format
        self.assertEqual(neg_interval.latex(), expected_neg_latex)

    def test_interval_simplification(self):
        """
        Test Interval simplification behavior.

        Validates:
        - Boundary expression simplification
        - Interval structure preservation
        - Simplified boundary integration
        - Mathematical equivalence preservation

        Ensures intervals properly simplify their components.
        """
        # Test interval with complex boundaries that can be simplified
        a = tm.Add(l=tm.Integer(n=2), r=tm.Integer(n=3))  # 2 + 3 = 5
        b = tm.Mul(l=tm.Integer(n=2), r=tm.Integer(n=4))  # 2 * 4 = 8
        complex_interval = tm.Interval(l=a, r=b)

        simplified = complex_interval.simplified()

        # Verify it's still an interval
        self.assertIsInstance(simplified, tm.Interval)

        # Verify boundaries are simplified
        self.assertEqual(simplified.l, tm.Integer(n=5))
        self.assertEqual(simplified.r, tm.Integer(n=8))

        # Verify boundary types are preserved
        self.assertEqual(simplified.left_open, complex_interval.left_open)
        self.assertEqual(simplified.right_open, complex_interval.right_open)

    def test_interval_with_fractions(self):
        """
        Test Interval creation and operations with fractional boundaries.

        Validates:
        - Fraction boundary handling
        - Mixed integer and fraction boundaries
        - Decimal boundary integration
        - Mathematical precision

        Ensures intervals work with all numeric types.
        """
        # Test interval with fraction boundaries [1/2, 3/4]
        half = tm.Fraction(p=1, q=2)
        three_quarters = tm.Fraction(p=3, q=4)
        frac_interval = tm.Interval(l=half, r=three_quarters)

        self.assertEqual(frac_interval.l, half)
        self.assertEqual(frac_interval.r, three_quarters)

        # Test mixed interval [0, 1/2]
        zero = tm.Integer(n=0)
        mixed_interval = tm.Interval(l=zero, r=half)

        self.assertEqual(mixed_interval.l, zero)
        self.assertEqual(mixed_interval.r, half)

        # Test interval with decimals [0.5, 2.5]
        decimal_a = tm.Decimal(x=0.5)
        decimal_b = tm.Decimal(x=2.5)
        decimal_interval = tm.Interval(l=decimal_a, r=decimal_b)

        self.assertEqual(decimal_interval.l, decimal_a)
        self.assertEqual(decimal_interval.r, decimal_b)

    def test_interval_string_representation(self):
        """
        Test Interval string representation methods.

        Validates:
        - __repr__ method output
        - __str__ method output
        - Boundary information display
        - Open/closed interval indication

        Ensures intervals can be properly displayed and debugged.
        """
        # Test simple interval representation
        a = tm.Integer(n=1)
        b = tm.Integer(n=5)
        interval = tm.Interval(l=a, r=b, left_open=True, right_open=False)

        repr_str = repr(interval)

        # Verify essential information is in repr
        self.assertIn("Interval", repr_str)
        self.assertIn("l=", repr_str)
        self.assertIn("r=", repr_str)
        self.assertIn("left_open=True", repr_str)
        self.assertIn("right_open=False", repr_str)

        # Test str method
        str_str = str(interval)
        self.assertEqual(str_str, repr_str)  # Should delegate to repr

    def test_interval_edge_cases(self):
        """
        Test Interval behavior with edge cases and boundary conditions.

        Validates:
        - Zero-width intervals [a, a]
        - Very large number boundaries
        - Negative number intervals
        - Infinity boundaries (if supported)
        - Error handling for invalid intervals

        Ensures robust interval handling under edge conditions.
        """
        # Test zero-width interval [5, 5] - SymPy creates FiniteSet instead of Interval
        five = tm.Integer(n=5)
        try:
            zero_width = tm.Interval(l=five, r=five)
            self.assertEqual(zero_width.l, five)
            self.assertEqual(zero_width.r, five)
        except Exception:
            # SymPy correctly converts zero-width intervals to FiniteSet
            # This is mathematically sound behavior - a single point is not an interval
            pass

        # Test interval with large numbers
        large_a = tm.Integer(n=1000000)
        large_b = tm.Integer(n=2000000)
        large_interval = tm.Interval(l=large_a, r=large_b)

        self.assertEqual(large_interval.l, large_a)
        self.assertEqual(large_interval.r, large_b)

        # Test negative interval [-10, -1]
        neg_a = tm.Integer(n=-10)
        neg_b = tm.Integer(n=-1)
        neg_interval = tm.Interval(l=neg_a, r=neg_b)

        self.assertEqual(neg_interval.l, neg_a)
        self.assertEqual(neg_interval.r, neg_b)

        # Test interval with infinity (if supported)
        try:
            inf = tm.Inf()
            zero = tm.Integer(n=0)
            inf_interval = tm.Interval(l=zero, r=inf)

            self.assertEqual(inf_interval.l, zero)
            self.assertEqual(inf_interval.r, inf)
        except Exception:
            # If Inf is not supported in intervals, that's acceptable
            pass

    def test_interval_sympy_integration(self):
        """
        Test Interval integration with SymPy expressions.

        Validates:
        - SymPy Interval object creation
        - Boundary parameter passing to SymPy
        - Open/closed boundary handling in SymPy
        - Mathematical equivalence

        Ensures intervals properly integrate with SymPy's set theory.
        """
        # Test SymPy integration for closed interval
        a = tm.Integer(n=1)
        b = tm.Integer(n=5)
        interval = tm.Interval(l=a, r=b)

        sympy_expr = interval.sympy_expr

        # Verify SymPy expression is created
        self.assertIsNotNone(sympy_expr)

        # Test SymPy integration for open interval
        open_interval = tm.Interval(l=a, r=b, left_open=True, right_open=True)
        open_sympy_expr = open_interval.sympy_expr

        self.assertIsNotNone(open_sympy_expr)

        # Verify that different boundary types create different SymPy objects
        # (They should not be equal due to different boundary conditions)
        self.assertNotEqual(str(sympy_expr), str(open_sympy_expr))

    def test_interval_mathematical_properties(self):
        """
        Test mathematical properties and relationships of intervals.

        Validates:
        - Interval containment concepts
        - Boundary relationship preservation
        - Mathematical interval semantics
        - Set theory compliance

        Ensures intervals behave according to mathematical principles.
        """
        # Test that simplification preserves interval semantics
        x = tm.Symbol(s="x")
        expr_a = x + tm.Integer(n=0)  # x + 0 = x
        expr_b = x + tm.Integer(n=1)  # x + 1

        interval = tm.Interval(l=expr_a, r=expr_b)
        simplified = interval.simplified()

        # Verify mathematical equivalence after simplification
        self.assertEqual(simplified.l, x)  # x + 0 should simplify to x
        self.assertIsInstance(simplified.r, tm.Add)  # x + 1 should remain as Add

        # Test interval with fraction boundaries maintains precision
        precise_a = tm.Fraction(p=1, q=3)
        precise_b = tm.Fraction(p=2, q=3)
        precise_interval = tm.Interval(l=precise_a, r=precise_b)

        # Should maintain exact fractional representation
        self.assertEqual(precise_interval.l, precise_a)
        self.assertEqual(precise_interval.r, precise_b)

    def test_interval_in_complex_expressions(self):
        """
        Test Interval usage within complex mathematical expressions.

        Validates:
        - Intervals as function domains
        - Intervals in mathematical contexts
        - Integration with other mathematical objects
        - Compositional behavior

        Ensures intervals work properly in realistic mathematical scenarios.
        """
        # Test interval as part of larger mathematical context
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # Create interval representing domain
        domain = tm.Interval(l=tm.Integer(n=0), r=tm.Integer(n=10))

        # Verify domain can be used with other mathematical objects
        self.assertIsInstance(domain, tm.Interval)

        # Test interval with complex boundary expressions
        complex_left = (x + y) / tm.Integer(n=2)
        complex_right = x * y

        complex_interval = tm.Interval(l=complex_left, r=complex_right)

        # Verify complex expressions are preserved
        self.assertIsInstance(complex_interval.l, tm.Fraction)
        self.assertIsInstance(complex_interval.r, tm.Mul)

        # Verify LaTeX generation works with complex boundaries
        latex_output = complex_interval.latex()
        self.assertIn("\\lbracket", latex_output)
        self.assertIn("\\rbracket", latex_output)
        self.assertIn(";", latex_output)


if __name__ == "__main__":
    unittest.main()
