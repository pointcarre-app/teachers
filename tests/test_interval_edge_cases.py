"""
Test suite for Interval edge cases and validation errors.

This module tests specific edge cases that were causing validation errors
in the generator, particularly:
- EmptySet returns from sympy when bounds are invalid
- Proper ordering of interval bounds
- Division by zero in fraction creation
- Interval creation with infinity bounds

These tests ensure the robustness of interval creation and help prevent
regression of the bugs fixed in the generator logic.
"""

import unittest
from pydantic import ValidationError
import sympy as sp
import teachers.maths as tm


class TestIntervalEdgeCases(unittest.TestCase):
    """Test suite for Interval edge cases that were causing EmptySet errors."""

    def test_interval_bounds_ordering(self):
        """
        Test that intervals require left bound < right bound.

        When left >= right, sympy returns EmptySet which causes validation errors.
        This test ensures we catch these cases properly.
        """
        # Valid interval: left < right
        a = tm.Integer(n=2)
        b = tm.Integer(n=5)
        valid_interval = tm.Interval(l=a, r=b, left_open=True, right_open=True)
        self.assertEqual(valid_interval.l, a)
        self.assertEqual(valid_interval.r, b)

        # Invalid interval: left > right should fail
        # sympy.Interval(5, 2) returns EmptySet
        with self.assertRaises(ValidationError) as context:
            invalid_interval = tm.Interval(l=b, r=a, left_open=True, right_open=True)

        # Check that the error mentions the type mismatch
        error_msg = str(context.exception)
        self.assertTrue(
            "Input should be an instance of Interval" in error_msg or "EmptySet" in error_msg,
            f"Expected error about Interval/EmptySet, got: {error_msg}",
        )

    def test_interval_with_equal_bounds_open(self):
        """
        Test that open intervals with equal bounds fail properly.

        An open interval (a, a) is empty and sympy returns EmptySet.
        """
        a = tm.Integer(n=3)

        # Open interval with same bounds should fail
        with self.assertRaises(ValidationError) as context:
            empty_interval = tm.Interval(l=a, r=a, left_open=True, right_open=True)

        error_msg = str(context.exception)
        self.assertTrue(
            "EmptySet" in error_msg or "Input should be an instance of Interval" in error_msg,
            f"Expected EmptySet error, got: {error_msg}",
        )

    def test_interval_with_equal_bounds_closed(self):
        """
        Test closed interval with equal bounds.

        A closed interval [a, a] represents a single point.
        Note: sympy may convert this to a FiniteSet rather than Interval.
        """
        a = tm.Integer(n=3)

        try:
            # Closed interval [3, 3] might work or might become FiniteSet
            single_point = tm.Interval(l=a, r=a, left_open=False, right_open=False)
            # If it works, verify the bounds
            self.assertEqual(single_point.l, a)
            self.assertEqual(single_point.r, a)
        except ValidationError:
            # This is acceptable - sympy converts [a, a] to FiniteSet{a}
            # which is mathematically correct but not an Interval
            pass

    def test_interval_with_infinity(self):
        """
        Test intervals with infinity bounds as used in the generator.

        These are the three types of intervals the generator creates:
        1. (-∞, root1) - before the first root
        2. (root1, root2) - between roots
        3. (root2, +∞) - after the second root
        """
        # Test with infinity bounds
        zero = tm.Integer(n=0)
        five = tm.Integer(n=5)

        # Test (-∞, 5)
        neg_inf = tm.Mul(l=tm.Integer(n=-1), r=tm.Inf())  # -Inf
        interval1 = tm.Interval(l=neg_inf, r=five, left_open=True, right_open=True)
        self.assertEqual(interval1.r, five)

        # Test (0, +∞)
        pos_inf = tm.Inf()
        interval2 = tm.Interval(l=zero, r=pos_inf, left_open=True, right_open=True)
        self.assertEqual(interval2.l, zero)

        # Test (-∞, +∞) - the entire real line
        interval3 = tm.Interval(l=neg_inf, r=pos_inf, left_open=True, right_open=True)
        self.assertIsNotNone(interval3.sympy_expr)

    def test_interval_with_fractions_from_division(self):
        """
        Test intervals with fractions created from division operations.

        This simulates the generator's root calculation: root = -(b/a)
        """
        # Simulate root calculations as in the generator
        a1 = tm.Integer(n=2)
        b1 = tm.Integer(n=-9)
        root1 = tm.Mul(l=tm.Integer(n=-1), r=tm.Fraction(p=b1, q=a1))  # -(b1/a1) = 9/2

        a2 = tm.Integer(n=3)
        b2 = tm.Integer(n=-2)
        root2 = tm.Mul(l=tm.Integer(n=-1), r=tm.Fraction(p=b2, q=a2))  # -(b2/a2) = 2/3

        # Ensure proper ordering (root2 < root1 in this case)
        # 2/3 ≈ 0.667 < 9/2 = 4.5
        interval = tm.Interval(l=root2, r=root1, left_open=True, right_open=True)

        self.assertEqual(interval.l, root2)
        self.assertEqual(interval.r, root1)
        self.assertIsInstance(interval.sympy_expr, sp.Interval)

    def test_fraction_zero_denominator(self):
        """
        Test that Fraction properly rejects zero denominators.

        This was one of the original errors in the generator when
        a1 or a2 could be zero.
        """
        numerator = tm.Integer(n=5)
        zero = tm.Integer(n=0)

        # Direct fraction creation with zero denominator should fail
        with self.assertRaises(ValidationError) as context:
            invalid_frac = tm.Fraction(p=numerator, q=zero)

        error_msg = str(context.exception)
        self.assertIn("Denominator cannot be zero", error_msg)

        # Division by zero using operator should also fail
        with self.assertRaises(ValidationError) as context:
            result = numerator / zero

        error_msg = str(context.exception)
        self.assertIn("Denominator cannot be zero", error_msg)

    def test_generator_scenario_with_proper_ordering(self):
        """
        Test the exact scenario from the generator with proper root ordering.

        This test simulates the generator logic after the fix:
        1. Calculate two roots
        2. Ensure root1 <= root2
        3. Create valid intervals
        """
        # Test case from seed 3 that was failing
        a1 = tm.Integer(n=-3)
        b1 = tm.Integer(n=7)
        a2 = tm.Integer(n=8)
        b2 = tm.Integer(n=-6)

        # Calculate roots: root = -(b/a)
        root1_num = tm.Mul(l=tm.Integer(n=-1), r=b1)  # -7
        root1 = tm.Fraction(p=root1_num, q=a1)  # -7/-3 = 7/3 ≈ 2.333

        root2_num = tm.Mul(l=tm.Integer(n=-1), r=b2)  # 6
        root2 = tm.Fraction(p=root2_num, q=a2)  # 6/8 = 3/4 = 0.75

        # Swap if needed to ensure root1 <= root2
        if root1.eval() > root2.eval():
            root1, root2 = root2, root1

        # Now all three interval types should work
        # Type 0: (-∞, smaller_root)
        neg_inf = tm.Mul(l=tm.Integer(n=-1), r=tm.Inf())
        interval0 = tm.Interval(l=neg_inf, r=root1, left_open=True, right_open=True)
        self.assertIsInstance(interval0.sympy_expr, sp.Interval)

        # Type 1: (smaller_root, larger_root)
        interval1 = tm.Interval(l=root1, r=root2, left_open=True, right_open=True)
        self.assertIsInstance(interval1.sympy_expr, sp.Interval)

        # Type 2: (larger_root, +∞)
        pos_inf = tm.Inf()
        interval2 = tm.Interval(l=root2, r=pos_inf, left_open=True, right_open=True)
        self.assertIsInstance(interval2.sympy_expr, sp.Interval)

    def test_multiple_problematic_seeds(self):
        """
        Test multiple seed values that were causing failures.

        These seeds (3, 4, 16, 17, 20) all failed with EmptySet errors
        before the fix to ensure proper root ordering.
        """
        test_cases = [
            # (a1, b1, a2, b2) from failing seeds
            (-3, 7, 8, -6),  # seed 3
            (-3, -7, -1, 2),  # seed 4
            (1, 5, 5, -1),  # seed 16
            (6, -1, 3, 1),  # seed 17
            (-6, 10, -2, -7),  # seed 20
        ]

        for a1_val, b1_val, a2_val, b2_val in test_cases:
            a1 = tm.Integer(n=a1_val)
            b1 = tm.Integer(n=b1_val)
            a2 = tm.Integer(n=a2_val)
            b2 = tm.Integer(n=b2_val)

            # Calculate roots
            root1 = tm.Fraction(p=tm.Mul(l=tm.Integer(n=-1), r=b1), q=a1)
            root2 = tm.Fraction(p=tm.Mul(l=tm.Integer(n=-1), r=b2), q=a2)

            # Ensure proper ordering
            if root1.eval() > root2.eval():
                root1, root2 = root2, root1

            # Create interval between roots - this was failing before
            try:
                interval = tm.Interval(l=root1, r=root2, left_open=True, right_open=True)
                self.assertIsInstance(interval.sympy_expr, sp.Interval)
                # Verify left < right
                self.assertLess(root1.eval(), root2.eval())
            except ValidationError as e:
                self.fail(f"Interval creation failed for test case {test_cases}: {e}")

    def test_interval_latex_output(self):
        """
        Test that intervals produce correct LaTeX output.
        """
        a = tm.Integer(n=2)
        b = tm.Integer(n=5)

        # Test basic interval LaTeX
        interval = tm.Interval(l=a, r=b, left_open=True, right_open=True)
        latex = interval.latex()

        # Should contain the bracket notation
        self.assertIn("\\lbracket", latex)
        self.assertIn("\\rbracket", latex)
        self.assertIn("2", latex)
        self.assertIn("5", latex)
        self.assertIn(";", latex)  # separator

    def test_interval_simplification(self):
        """
        Test that interval simplification works correctly.
        """
        # Create interval with fractions that can be simplified
        num1 = tm.Integer(n=4)
        den1 = tm.Integer(n=2)  # 4/2 = 2
        frac1 = tm.Fraction(p=num1, q=den1)

        num2 = tm.Integer(n=15)
        den2 = tm.Integer(n=3)  # 15/3 = 5
        frac2 = tm.Fraction(p=num2, q=den2)

        interval = tm.Interval(l=frac1, r=frac2, left_open=False, right_open=False)
        simplified = interval.simplified()

        # The bounds should be simplified
        self.assertIsNotNone(simplified)
        self.assertEqual(simplified.l.simplified().eval(), 2)
        self.assertEqual(simplified.r.simplified().eval(), 5)


if __name__ == "__main__":
    unittest.main()
