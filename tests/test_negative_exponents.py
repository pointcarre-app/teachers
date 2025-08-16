"""
Test file for negative exponent handling in Pow operations.
This addresses the bug where 10^(-2) was trying to create Integer(n=0.01)
instead of properly returning a Fraction or Decimal.
"""

import unittest
import teachers.maths as tm
import teachers.generator as tg


class TestNegativeExponents(unittest.TestCase):
    """Test suite for negative exponent operations."""

    def test_power_negative_one(self):
        """Test that x^(-1) returns 1/x as a Fraction."""
        # Test with Integer base
        result = (tm.Integer(n=10) ** tm.Integer(n=-1)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 10
        assert result.eval() == 0.1

    def test_power_negative_two(self):
        """Test that 10^(-2) returns 1/100 as a Fraction."""
        result = (tm.Integer(n=10) ** tm.Integer(n=-2)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 100
        assert result.eval() == 0.01

    def test_power_negative_three(self):
        """Test that 10^(-3) returns 1/1000 as a Fraction."""
        result = (tm.Integer(n=10) ** tm.Integer(n=-3)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 1000
        assert result.eval() == 0.001

    def test_power_negative_four(self):
        """Test that 10^(-4) returns 1/10000 as a Fraction."""
        result = (tm.Integer(n=10) ** tm.Integer(n=-4)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 10000
        assert result.eval() == 0.0001

    def test_various_bases_negative_exponents(self):
        """Test negative exponents with different bases."""
        # 2^(-3) = 1/8
        result = (tm.Integer(n=2) ** tm.Integer(n=-3)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 8

        # 3^(-2) = 1/9
        result = (tm.Integer(n=3) ** tm.Integer(n=-2)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 9

        # 5^(-2) = 1/25
        result = (tm.Integer(n=5) ** tm.Integer(n=-2)).simplified()
        assert isinstance(result, tm.Fraction)
        assert result.p.n == 1
        assert result.q.n == 25

    def test_conversion_to_decimal(self):
        """Test that negative exponent results can be converted to Decimal."""
        # This mimics the problematic code from the original issue
        b = tm.Integer(n=10) ** tm.Integer(n=-2)
        b_simplified = b.simplified()

        # Check that simplified returns a Fraction
        assert isinstance(b_simplified, tm.Fraction)

        # Check that we can convert to decimal
        b_decimal = b_simplified.as_decimal
        assert isinstance(b_decimal, tm.Decimal)
        assert b_decimal.eval() == 0.01

    def test_original_problematic_scenario(self):
        """Test the exact scenario that was causing the error."""
        gen = tg.MathsGenerator(0)

        # Simulate the original code
        n2 = 2  # Example value that was causing issues
        b = tm.Integer(n=10) ** tm.Integer(n=-n2)
        b_simplified = b.simplified()
        b_decimal = b_simplified.as_decimal

        # Verify it works correctly
        assert isinstance(b_simplified, tm.Fraction)
        assert isinstance(b_decimal, tm.Decimal)
        assert b_decimal.eval() == 0.01

        # Test with different values
        for n in [1, 2, 3, 4]:
            b = tm.Integer(n=10) ** tm.Integer(n=-n)
            b_simplified = b.simplified()
            assert isinstance(b_simplified, tm.Fraction)
            b_decimal = b_simplified.as_decimal
            assert isinstance(b_decimal, tm.Decimal)
            expected = 10 ** (-n)
            assert abs(b_decimal.eval() - expected) < 1e-10

    def test_addition_with_negative_exponents(self):
        """Test that addition works with negative exponent results."""
        # Recreate the full scenario: 10^4 + 10^(-4) + 1/10
        a = tm.Integer(n=10) ** tm.Integer(n=4)
        b = tm.Integer(n=10) ** tm.Integer(n=-4)
        c = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=10))

        # Simplify b to get Fraction, then convert to Decimal
        b_simplified = b.simplified()
        b_decimal = b_simplified.as_decimal
        c_simplified = c.simplified()

        # Test addition
        result = a + b_decimal + c_simplified
        assert result is not None

        # Verify the calculation
        expected_value = 10000 + 0.0001 + 0.1
        assert abs(result.eval() - expected_value) < 1e-10

    def test_latex_representation(self):
        """Test that negative exponents render correctly in LaTeX."""
        # Test direct Pow representation
        pow_expr = tm.Integer(n=10) ** tm.Integer(n=-2)
        assert pow_expr.latex() == "10^{-2}"

        # Test simplified Fraction representation
        simplified = pow_expr.simplified()
        assert isinstance(simplified, tm.Fraction)
        # Fraction LaTeX should be something like \frac{1}{100}
        latex_str = simplified.latex()
        assert "frac" in latex_str or "dfrac" in latex_str

    def test_edge_cases(self):
        """Test edge cases for negative exponents."""
        # 1^(-n) should always be 1
        for n in [1, 2, 3, 4]:
            result = (tm.Integer(n=1) ** tm.Integer(n=-n)).simplified()
            assert result.eval() == 1.0

        # 0^(-n) should raise an error (division by zero)
        try:
            result = (tm.Integer(n=0) ** tm.Integer(n=-1)).simplified()
            result.eval()
            assert False, "Should have raised an error for division by zero"
        except Exception as e:
            # Either a ZeroDivisionError or a Pydantic validation error for zero denominator
            assert "zero" in str(e).lower() or "denominator" in str(e).lower()
            pass  # Expected behavior


if __name__ == "__main__":
    # Run tests if executed directly using unittest
    unittest.main()
