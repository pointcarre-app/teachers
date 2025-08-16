"""
Test suite for Add simplification functionality.

This module contains comprehensive tests for the Add.simplified() method,
specifically focusing on the newly implemented cases:
- Integer + Decimal combinations
- Decimal + Fraction combinations
- Complex nested expressions involving these types

These tests ensure that mathematical expressions involving mixed numeric types
can be properly simplified without raising NotImplementedError.
"""

import unittest
import teachers.maths as tm


class TestAddSimplification(unittest.TestCase):
    """Test suite for Add simplification with mixed numeric types."""

    def test_integer_plus_decimal_p_q_form(self):
        """Test Integer + Decimal where Decimal uses p/q form."""
        # Create: 5 + Decimal(p=1, q=4) = 5 + 0.25 = 5.25
        integer = tm.Integer(n=5)
        decimal = tm.Decimal(p=1, q=4)

        add_expr = integer + decimal
        simplified = add_expr.simplified()

        # Should return Decimal(x=5.25)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 5.25)

    def test_decimal_plus_integer_p_q_form(self):
        """Test Decimal + Integer where Decimal uses p/q form (commutative)."""
        # Create: Decimal(p=3, q=8) + 2 = 0.375 + 2 = 2.375
        decimal = tm.Decimal(p=3, q=8)
        integer = tm.Integer(n=2)

        add_expr = decimal + integer
        simplified = add_expr.simplified()

        # Should return Decimal(x=2.375)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 2.375)

    def test_integer_plus_decimal_x_form(self):
        """Test Integer + Decimal where Decimal uses x form."""
        # Create: 10 + Decimal(x=3.14) = 10 + 3.14 = 13.14
        integer = tm.Integer(n=10)
        decimal = tm.Decimal(x=3.14)

        add_expr = integer + decimal
        simplified = add_expr.simplified()

        # Should return Decimal(x=13.14)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 13.14)

    def test_decimal_plus_integer_x_form(self):
        """Test Decimal + Integer where Decimal uses x form (commutative)."""
        # Create: Decimal(x=7.5) + 8 = 7.5 + 8 = 15.5
        decimal = tm.Decimal(x=7.5)
        integer = tm.Integer(n=8)

        add_expr = decimal + integer
        simplified = add_expr.simplified()

        # Should return Decimal(x=15.5)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 15.5)

    def test_decimal_plus_fraction(self):
        """Test Decimal + Fraction combination."""
        # Create: Decimal(p=1, q=4) + Fraction(1/2) = 0.25 + 0.5 = 0.75
        decimal = tm.Decimal(p=1, q=4)  # 0.25
        fraction = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=2))  # 1/2 = 0.5

        add_expr = decimal + fraction
        simplified = add_expr.simplified()

        # Should return Decimal(x=0.75)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 0.75)

    def test_fraction_plus_decimal(self):
        """Test Fraction + Decimal combination (commutative)."""
        # Create: Fraction(3/4) + Decimal(x=0.1) = 0.75 + 0.1 = 0.85
        fraction = tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=4))  # 3/4 = 0.75
        decimal = tm.Decimal(x=0.1)

        add_expr = fraction + decimal
        simplified = add_expr.simplified()

        # Should return Decimal(x=0.85)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 0.85)

    def test_decimal_x_form_plus_fraction(self):
        """Test Decimal (x form) + Fraction combination."""
        # Create: Decimal(x=2.5) + Fraction(1/4) = 2.5 + 0.25 = 2.75
        decimal = tm.Decimal(x=2.5)
        fraction = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=4))  # 1/4 = 0.25

        add_expr = decimal + fraction
        simplified = add_expr.simplified()

        # Should return Decimal(x=2.75)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 2.75)

    def test_original_failing_case(self):
        """Test the original failing case from the user's code."""
        # Recreate the exact scenario that was failing:
        # 10^4 + Decimal(p=1, q=10000) + Fraction(1/10)

        # Create components
        a = tm.Integer(n=10) ** tm.Integer(n=4)  # 10^4 = 10000
        b = tm.Decimal(p=1, q=10000)  # 0.0001
        c = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=10))  # 1/10 = 0.1

        # Create the expression: a + b + c
        # This creates: Add(l=Add(l=Pow(...), r=Decimal(...)), r=Fraction(...))
        expr = a + b + c

        # This should not raise NotImplementedError anymore
        simplified = expr.simplified()

        # The result should be a Decimal representing 10000 + 0.0001 + 0.1 = 10000.1001
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 10000.1001)

    def test_nested_add_with_mixed_types(self):
        """Test nested Add expressions with mixed numeric types."""
        # Create: (Integer(5) + Decimal(0.5)) + Fraction(1/4)
        # = (5 + 0.5) + 0.25 = 5.5 + 0.25 = 5.75

        inner_add = tm.Integer(n=5) + tm.Decimal(x=0.5)
        outer_add = inner_add + tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=4))

        simplified = outer_add.simplified()

        # Should result in Decimal(x=5.75)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 5.75)

    def test_multiple_decimal_fraction_combinations(self):
        """Test multiple combinations of Decimal and Fraction operations."""
        # Create: Decimal(1/8) + Fraction(3/8) + Decimal(1/2)
        # = 0.125 + 0.375 + 0.5 = 1.0

        d1 = tm.Decimal(p=1, q=8)  # 0.125
        f1 = tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=8))  # 3/8 = 0.375
        d2 = tm.Decimal(x=0.5)  # 0.5

        expr = d1 + f1 + d2
        simplified = expr.simplified()

        # Should result in Decimal(x=1.0)
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 1.0)

    def test_zero_cases(self):
        """Test edge cases involving zero."""
        # Test Integer(0) + Decimal
        zero_int = tm.Integer(n=0)
        decimal = tm.Decimal(x=3.14)

        expr1 = zero_int + decimal
        simplified1 = expr1.simplified()

        # Should return the decimal value
        self.assertIsInstance(simplified1, tm.Decimal)
        self.assertEqual(simplified1.x, 3.14)

        # Test Decimal(0) + Fraction
        zero_decimal = tm.Decimal(x=0.0)
        fraction = tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=11))

        expr2 = zero_decimal + fraction
        simplified2 = expr2.simplified()

        # Should return decimal representation of the fraction
        self.assertIsInstance(simplified2, tm.Decimal)
        self.assertAlmostEqual(simplified2.x, 7 / 11, places=10)

    def test_large_numbers(self):
        """Test with large numbers to ensure no overflow issues."""
        # Test with large integer and small decimal
        large_int = tm.Integer(n=1000000)
        small_decimal = tm.Decimal(p=1, q=1000000)  # 0.000001

        expr = large_int + small_decimal
        simplified = expr.simplified()

        # Should result in 1000000.000001
        self.assertIsInstance(simplified, tm.Decimal)
        self.assertEqual(simplified.x, 1000000.000001)


if __name__ == "__main__":
    unittest.main()
