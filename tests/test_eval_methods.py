"""
Test suite for eval() method functionality across all mathematical objects.

This module tests numerical evaluation capabilities:
- Atomic objects (Integer, Decimal) numerical evaluation
- Binary operators (Add, Mul, Fraction, Pow) computation
- Complex nested expression evaluation
- Floating-point precision and accuracy
- Mathematical correctness of computations

These tests ensure that mathematical objects can be evaluated
to numerical values for computational purposes while maintaining
mathematical accuracy and proper error handling.
"""

import unittest
import math
import teachers.maths as tm


class TestEvalMethods(unittest.TestCase):
    """Test suite for numerical evaluation across all mathematical objects."""

    def test_integer_eval(self):
        """
        Test Integer eval() method for basic numerical conversion.

        Validates:
        - Positive integer evaluation
        - Negative integer evaluation
        - Zero evaluation
        - Large number evaluation
        - Return type consistency (int)

        Ensures integers correctly return their numerical values.
        """
        # Test positive integer
        i = tm.Integer(n=42)
        self.assertEqual(i.eval(), 42)
        self.assertIsInstance(i.eval(), int)

        # Test negative integer
        i_neg = tm.Integer(n=-17)
        self.assertEqual(i_neg.eval(), -17)

        # Test zero
        i_zero = tm.Integer(n=0)
        self.assertEqual(i_zero.eval(), 0)

        # Test large number
        i_large = tm.Integer(n=1000000)
        self.assertEqual(i_large.eval(), 1000000)

    def test_decimal_eval(self):
        """
        Test Decimal eval() method for floating-point evaluation.

        Validates:
        - Decimal with x parameter evaluation
        - Decimal with p/q parameter evaluation
        - Floating-point precision
        - Different decimal representations
        - Return type consistency (float)

        Ensures decimals correctly return their numerical values.
        """
        # Test decimal with x parameter
        d1 = tm.Decimal(x=3.14)
        self.assertAlmostEqual(d1.eval(), 3.14, places=10)
        self.assertIsInstance(d1.eval(), float)

        # Test decimal with p/q parameters
        d2 = tm.Decimal(p=5, q=2)
        self.assertAlmostEqual(d2.eval(), 2.5, places=10)

        # Test zero decimal
        d3 = tm.Decimal(x=0.0)
        self.assertEqual(d3.eval(), 0.0)

        # Test negative decimal
        d4 = tm.Decimal(x=-1.5)
        self.assertAlmostEqual(d4.eval(), -1.5, places=10)

    def test_add_eval(self):
        """
        Test Add eval() method for addition computation.

        Validates:
        - Integer + Integer addition
        - Decimal + Decimal addition
        - Mixed Integer + Decimal addition
        - Negative number addition
        - Zero addition

        Ensures addition operations compute correctly.
        """
        # Test integer addition
        a = tm.Integer(n=5)
        b = tm.Integer(n=3)
        add_expr = a + b
        self.assertEqual(add_expr.eval(), 8)

        # Test decimal addition
        d1 = tm.Decimal(x=2.5)
        d2 = tm.Decimal(x=1.5)
        add_decimal = d1 + d2
        self.assertAlmostEqual(add_decimal.eval(), 4.0, places=10)

        # Test mixed addition
        mixed_add = a + d1
        self.assertAlmostEqual(mixed_add.eval(), 7.5, places=10)

        # Test addition with negative
        neg = tm.Integer(n=-2)
        add_neg = a + neg
        self.assertEqual(add_neg.eval(), 3)

        # Test addition with zero
        zero = tm.Integer(n=0)
        add_zero = a + zero
        self.assertEqual(add_zero.eval(), 5)

    def test_mul_eval(self):
        """
        Test Mul eval() method for multiplication computation.

        Validates:
        - Integer * Integer multiplication
        - Decimal * Decimal multiplication
        - Mixed Integer * Decimal multiplication
        - Multiplication by zero
        - Multiplication by negative numbers

        Ensures multiplication operations compute correctly.
        """
        # Test integer multiplication
        a = tm.Integer(n=4)
        b = tm.Integer(n=3)
        mul_expr = a * b
        self.assertEqual(mul_expr.eval(), 12)

        # Test decimal multiplication
        d1 = tm.Decimal(x=2.5)
        d2 = tm.Decimal(x=2.0)
        mul_decimal = d1 * d2
        self.assertAlmostEqual(mul_decimal.eval(), 5.0, places=10)

        # Test mixed multiplication
        mixed_mul = a * d1
        self.assertAlmostEqual(mixed_mul.eval(), 10.0, places=10)

        # Test multiplication by zero
        zero = tm.Integer(n=0)
        mul_zero = a * zero
        self.assertEqual(mul_zero.eval(), 0)

        # Test multiplication by negative
        neg = tm.Integer(n=-2)
        mul_neg = a * neg
        self.assertEqual(mul_neg.eval(), -8)

    def test_fraction_eval(self):
        """
        Test Fraction eval() method for division computation.

        Validates:
        - Simple fraction evaluation
        - Improper fraction evaluation
        - Negative fraction evaluation
        - Fraction with large numbers
        - Floating-point precision

        Ensures fractions correctly compute their decimal values.
        """
        # Test simple fraction
        frac = tm.Fraction(p=1, q=2)
        self.assertAlmostEqual(frac.eval(), 0.5, places=10)

        # Test improper fraction
        improper = tm.Fraction(p=7, q=3)
        expected = 7.0 / 3.0
        self.assertAlmostEqual(improper.eval(), expected, places=10)

        # Test negative fraction
        neg_frac = tm.Fraction(p=-3, q=4)
        self.assertAlmostEqual(neg_frac.eval(), -0.75, places=10)

        # Test fraction with expressions (after simplification)
        a = tm.Integer(n=6)
        b = tm.Integer(n=4)
        expr_frac = tm.Fraction(p=a, q=b)
        self.assertAlmostEqual(expr_frac.eval(), 1.5, places=10)

        # Test unit fraction
        unit = tm.Fraction(p=1, q=1)
        self.assertEqual(unit.eval(), 1.0)

    def test_pow_eval(self):
        """
        Test Pow eval() method for exponentiation computation.

        Validates:
        - Integer base and exponent
        - Decimal base and integer exponent
        - Fractional exponents (roots)
        - Negative exponents
        - Zero and one exponents

        Ensures power operations compute correctly.
        """
        # Test integer power
        base = tm.Integer(n=2)
        exp = tm.Integer(n=3)
        pow_expr = base**exp
        self.assertEqual(pow_expr.eval(), 8)

        # Test decimal base
        dec_base = tm.Decimal(x=2.5)
        pow_decimal = dec_base ** tm.Integer(n=2)
        self.assertAlmostEqual(pow_decimal.eval(), 6.25, places=10)

        # Test fractional exponent (square root)
        sqrt_exp = tm.Fraction(p=1, q=2)
        four = tm.Integer(n=4)
        sqrt_expr = four**sqrt_exp
        self.assertAlmostEqual(sqrt_expr.eval(), 2.0, places=10)

        # Test negative exponent
        neg_exp = tm.Integer(n=-2)
        neg_pow = base**neg_exp
        self.assertAlmostEqual(neg_pow.eval(), 0.25, places=10)

        # Test exponent of zero
        zero_exp = tm.Integer(n=0)
        zero_pow = base**zero_exp
        self.assertEqual(zero_pow.eval(), 1)

        # Test exponent of one
        one_exp = tm.Integer(n=1)
        one_pow = base**one_exp
        self.assertEqual(one_pow.eval(), 2)

    def test_complex_expression_eval(self):
        """
        Test eval() for complex nested mathematical expressions.

        Validates:
        - Multi-level nested expressions
        - Mixed operation types
        - Operator precedence in evaluation
        - Complex fraction expressions
        - Mathematical accuracy

        Ensures complex expressions evaluate to correct numerical results.
        """
        # Test expression: (2 + 3) * 4 = 20
        a = tm.Integer(n=2)
        b = tm.Integer(n=3)
        c = tm.Integer(n=4)
        expr1 = (a + b) * c
        self.assertEqual(expr1.eval(), 20)

        # Test expression: (1/2) + (1/4) = 0.75
        half = tm.Fraction(p=1, q=2)
        quarter = tm.Fraction(p=1, q=4)
        expr2 = half + quarter
        self.assertAlmostEqual(expr2.eval(), 0.75, places=10)

        # Test expression: 2^3 + 1 = 9
        two = tm.Integer(n=2)
        three = tm.Integer(n=3)
        one = tm.Integer(n=1)
        expr3 = (two**three) + one
        self.assertEqual(expr3.eval(), 9)

        # Test complex fraction: (3 + 4) / (2 * 5) = 0.7
        numerator = tm.Integer(n=3) + tm.Integer(n=4)
        denominator = tm.Integer(n=2) * tm.Integer(n=5)
        complex_frac = numerator / denominator
        self.assertAlmostEqual(complex_frac.eval(), 0.7, places=10)

    def test_eval_precision(self):
        """
        Test eval() method precision with various floating-point operations.

        Validates:
        - High-precision decimal operations
        - Floating-point arithmetic accuracy
        - Rounding and precision handling
        - Edge cases with very small/large numbers

        Ensures numerical evaluation maintains appropriate precision.
        """
        # Test high-precision decimal
        pi_approx = tm.Decimal(x=3.141592653589793)
        self.assertAlmostEqual(pi_approx.eval(), math.pi, places=10)

        # Test very small fraction
        tiny = tm.Fraction(p=1, q=1000000)
        self.assertAlmostEqual(tiny.eval(), 1e-6, places=12)

        # Test large number operations
        large1 = tm.Integer(n=1000000)
        large2 = tm.Integer(n=999999)
        large_diff = large1 - large2
        self.assertEqual(large_diff.eval(), 1)

        # Test precision with repeated operations
        point_one = tm.Decimal(x=0.1)
        sum_expr = point_one + point_one + point_one
        # Note: floating point may have precision issues, so we use places=10
        self.assertAlmostEqual(sum_expr.eval(), 0.3, places=10)

    def test_eval_edge_cases(self):
        """
        Test eval() method with edge cases and boundary conditions.

        Validates:
        - Division by very small numbers
        - Large exponentiation
        - Zero in various operations
        - Mathematical limits and edge cases

        Ensures robust evaluation under edge conditions.
        """
        # Test very large power (but not overflow)
        two = tm.Integer(n=2)
        ten = tm.Integer(n=10)
        large_pow = two**ten
        self.assertEqual(large_pow.eval(), 1024)

        # Test fraction close to zero
        tiny_frac = tm.Fraction(p=1, q=1000)
        self.assertAlmostEqual(tiny_frac.eval(), 0.001, places=10)

        # Test operations with zero
        zero = tm.Integer(n=0)
        five = tm.Integer(n=5)

        # Zero addition
        zero_add = zero + five
        self.assertEqual(zero_add.eval(), 5)

        # Zero multiplication
        zero_mul = zero * five
        self.assertEqual(zero_mul.eval(), 0)

        # Zero power
        zero_pow = five**zero
        self.assertEqual(zero_pow.eval(), 1)

    def test_eval_type_consistency(self):
        """
        Test eval() method return type consistency.

        Validates:
        - Integer operations return appropriate types
        - Decimal operations return floats
        - Mixed operations handle type promotion
        - Type consistency across operations

        Ensures evaluation returns appropriate Python numeric types.
        """
        # Integer operations should return int when possible
        int_result = (tm.Integer(n=4) + tm.Integer(n=2)).eval()
        self.assertIsInstance(int_result, int)

        # Decimal operations should return float
        dec_result = (tm.Decimal(x=2.5) + tm.Decimal(x=1.5)).eval()
        self.assertIsInstance(dec_result, float)

        # Fraction operations should return float
        frac_result = tm.Fraction(p=1, q=2).eval()
        self.assertIsInstance(frac_result, float)

        # Mixed operations with decimals should return float
        mixed_result = (tm.Integer(n=2) + tm.Decimal(x=1.5)).eval()
        self.assertIsInstance(mixed_result, float)

    def test_eval_mathematical_properties(self):
        """
        Test eval() method adherence to mathematical properties.

        Validates:
        - Commutative property: a + b = b + a
        - Associative property: (a + b) + c = a + (b + c)
        - Distributive property: a * (b + c) = a * b + a * c
        - Identity properties

        Ensures evaluation preserves fundamental mathematical properties.
        """
        a = tm.Integer(n=3)
        b = tm.Integer(n=4)
        c = tm.Integer(n=5)

        # Test commutative property for addition
        add1 = (a + b).eval()
        add2 = (b + a).eval()
        self.assertEqual(add1, add2)

        # Test commutative property for multiplication
        mul1 = (a * b).eval()
        mul2 = (b * a).eval()
        self.assertEqual(mul1, mul2)

        # Test associative property for addition
        assoc1 = ((a + b) + c).eval()
        assoc2 = (a + (b + c)).eval()
        self.assertEqual(assoc1, assoc2)

        # Test distributive property
        dist1 = (a * (b + c)).eval()
        dist2 = ((a * b) + (a * c)).eval()
        self.assertEqual(dist1, dist2)

        # Test additive identity
        zero = tm.Integer(n=0)
        identity_add = (a + zero).eval()
        self.assertEqual(identity_add, a.eval())

        # Test multiplicative identity
        one = tm.Integer(n=1)
        identity_mul = (a * one).eval()
        self.assertEqual(identity_mul, a.eval())


if __name__ == "__main__":
    unittest.main()
