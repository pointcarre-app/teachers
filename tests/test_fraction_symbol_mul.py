"""Test suite for Fraction simplification with Symbol and Mul combinations.

This test suite addresses the NotImplementedError that was occurring when
simplifying Fraction objects with Symbol numerators and Mul denominators,
as well as other missing cases in Fraction.simplified().

The specific error was:
NotImplementedError: Simplification of <class 'teachers.maths.Fraction'> of
<class 'teachers.maths.Symbol'> and <class 'teachers.maths.Mul'>
p=Symbol(s='V')
q=Mul(l=Pi(), r=Pow(base=Symbol(s='r'), exp=Integer(n=2)))

This occurred when trying to simplify: V / (π * r²)
"""

import unittest
from teachers.maths import Symbol, Integer, Mul, Fraction, Pi, Pow


class TestFractionSymbolMul(unittest.TestCase):
    """Test suite for Fraction simplification with Symbol and Mul combinations."""

    def test_original_failing_case(self):
        """Test the exact failing case: Symbol('V') / (Pi() * Symbol('r')**Integer(2))"""
        # Create the exact expression that was failing
        v = Symbol(s="V")
        r = Symbol(s="r")
        pi_r_squared = Pi() * r ** Integer(n=2)

        # This represents: V / (π * r²)
        fraction = Fraction(p=v, q=pi_r_squared)

        # This should not raise NotImplementedError anymore
        simplified = fraction.simplified()

        # The result should be the same fraction (already in simplest form)
        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, v)
        self.assertEqual(simplified.q, pi_r_squared)

    def test_symbol_over_mul_various_combinations(self):
        """Test Symbol over Mul with various combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        a = Integer(n=3)

        # x / (y * 3)
        fraction1 = Fraction(p=x, q=y * a)
        simplified1 = fraction1.simplified()
        self.assertIsInstance(simplified1, Fraction)
        self.assertEqual(simplified1.p, x)

        # x / (3 * y)
        fraction2 = Fraction(p=x, q=a * y)
        simplified2 = fraction2.simplified()
        self.assertIsInstance(simplified2, Fraction)
        self.assertEqual(simplified2.p, x)

    def test_symbol_over_symbol(self):
        """Test Symbol over Symbol combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")

        # x / y
        fraction = Fraction(p=x, q=y)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, x)
        self.assertEqual(simplified.q, y)

    def test_symbol_over_pi(self):
        """Test Symbol over Pi."""
        x = Symbol(s="x")
        pi = Pi()

        # x / π
        fraction = Fraction(p=x, q=pi)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, x)
        self.assertEqual(simplified.q, pi)

    def test_symbol_over_power(self):
        """Test Symbol over Pow combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        n = Integer(n=2)

        # x / y²
        power = Pow(base=y, exp=n)
        fraction = Fraction(p=x, q=power)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, x)
        self.assertEqual(simplified.q, power)

    def test_mul_over_symbol(self):
        """Test Mul over Symbol combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        z = Symbol(s="z")

        # (x * y) / z
        mul_expr = Mul(l=x, r=y)
        fraction = Fraction(p=mul_expr, q=z)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, mul_expr)
        self.assertEqual(simplified.q, z)

    def test_mul_over_mul(self):
        """Test Mul over Mul combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        a = Symbol(s="a")
        b = Symbol(s="b")

        # (x * y) / (a * b)
        mul_num = Mul(l=x, r=y)
        mul_den = Mul(l=a, r=b)
        fraction = Fraction(p=mul_num, q=mul_den)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, mul_num)
        self.assertEqual(simplified.q, mul_den)

    def test_mul_over_pi(self):
        """Test Mul over Pi combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        pi = Pi()

        # (x * y) / π
        mul_expr = Mul(l=x, r=y)
        fraction = Fraction(p=mul_expr, q=pi)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, mul_expr)
        self.assertEqual(simplified.q, pi)

    def test_mul_over_power(self):
        """Test Mul over Pow combinations."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        z = Symbol(s="z")
        n = Integer(n=3)

        # (x * y) / z³
        mul_expr = Mul(l=x, r=y)
        power = Pow(base=z, exp=n)
        fraction = Fraction(p=mul_expr, q=power)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, mul_expr)
        self.assertEqual(simplified.q, power)

    def test_pi_over_symbol(self):
        """Test Pi over Symbol."""
        pi = Pi()
        x = Symbol(s="x")

        # π / x
        fraction = Fraction(p=pi, q=x)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, pi)
        self.assertEqual(simplified.q, x)

    def test_pi_over_mul(self):
        """Test Pi over Mul."""
        pi = Pi()
        x = Symbol(s="x")
        y = Symbol(s="y")

        # π / (x * y)
        mul_expr = Mul(l=x, r=y)
        fraction = Fraction(p=pi, q=mul_expr)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, pi)
        self.assertEqual(simplified.q, mul_expr)

    def test_pi_over_pi(self):
        """Test Pi over Pi should equal 1."""
        pi1 = Pi()
        pi2 = Pi()

        # π / π = 1
        fraction = Fraction(p=pi1, q=pi2)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Integer)
        self.assertEqual(simplified.n, 1)

    def test_power_over_symbol(self):
        """Test Pow over Symbol."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        n = Integer(n=2)

        # x² / y
        power = Pow(base=x, exp=n)
        fraction = Fraction(p=power, q=y)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, power)
        self.assertEqual(simplified.q, y)

    def test_power_over_mul(self):
        """Test Pow over Mul."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        z = Symbol(s="z")
        n = Integer(n=2)

        # x² / (y * z)
        power = Pow(base=x, exp=n)
        mul_expr = Mul(l=y, r=z)
        fraction = Fraction(p=power, q=mul_expr)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, power)
        self.assertEqual(simplified.q, mul_expr)

    def test_power_over_power(self):
        """Test Pow over Pow."""
        x = Symbol(s="x")
        y = Symbol(s="y")
        m = Integer(n=2)
        n = Integer(n=3)

        # x² / y³
        power1 = Pow(base=x, exp=m)
        power2 = Pow(base=y, exp=n)
        fraction = Fraction(p=power1, q=power2)
        simplified = fraction.simplified()

        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, power1)
        self.assertEqual(simplified.q, power2)

    def test_complex_expression_from_user_case(self):
        """Test the complex expression from the user's original failing case."""
        # Recreate the exact scenario: V / (π * r²)
        v = Symbol(s="V")
        r = Symbol(s="r")
        h = Symbol(s="h")

        # Create π * r²
        pi_r_squared = Pi() * (r ** Integer(n=2))

        # Create V / (π * r²)
        fraction = v / pi_r_squared

        # This should work without errors
        simplified = fraction.simplified()
        latex_repr = simplified.latex()

        # Verify the structure is preserved
        self.assertIsInstance(simplified, Fraction)
        self.assertEqual(simplified.p, v)
        self.assertIsInstance(simplified.q, Mul)

        # Verify LaTeX generation works
        self.assertIn("V", latex_repr)
        self.assertIn("\\pi", latex_repr)
        self.assertIn("r", latex_repr)

    def test_latex_generation_for_new_cases(self):
        """Test that LaTeX generation works for all the new fraction cases."""
        test_cases = [
            (Symbol(s="x"), Symbol(s="y")),  # x/y
            (Symbol(s="x"), Pi()),  # x/π
            (Symbol(s="V"), Pi() * Symbol(s="r") ** Integer(n=2)),  # V/(π*r²)
            (Pi(), Symbol(s="x")),  # π/x
        ]

        for numerator, denominator in test_cases:
            with self.subTest(num=numerator, den=denominator):
                fraction = Fraction(p=numerator, q=denominator)
                simplified = fraction.simplified()

                # Should not raise any errors
                latex_repr = simplified.latex()
                self.assertIsInstance(latex_repr, str)
                self.assertGreater(len(latex_repr), 0)


if __name__ == "__main__":
    unittest.main()
