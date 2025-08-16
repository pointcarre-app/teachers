"""Test suite for as_decimal property functionality.

This test suite addresses the AttributeError when accessing the as_decimal
property on Integer objects, and validates the clean LaTeX output for
whole numbers without decimal separators.

The specific error was:
AttributeError: 'Integer' object has no attribute 'as_decimal'

This test suite ensures:
- Integer.as_decimal property returns a Decimal object
- Decimal.latex() renders whole numbers without decimal points
- Decimal.latex() uses periods (not commas) as decimal separators
- Consistency across different numeric representations
"""

from teachers.maths import Integer, Decimal, Fraction


def test_integer_as_decimal_property():
    """Test that Integer objects have as_decimal property."""
    integer = Integer(n=5)

    # Should have as_decimal property
    assert hasattr(integer, "as_decimal")

    # Should return a Decimal object
    decimal = integer.as_decimal
    assert isinstance(decimal, Decimal)

    # Should have the same numeric value
    assert decimal.eval() == 5.0
    assert integer.eval() == 5


def test_integer_as_decimal_values():
    """Test as_decimal property with various integer values."""
    test_cases = [
        (0, 0.0),
        (1, 1.0),
        (5, 5.0),
        (42, 42.0),
        (-3, -3.0),
        (100, 100.0),
    ]

    for int_val, expected_decimal in test_cases:
        integer = Integer(n=int_val)
        decimal = integer.as_decimal

        assert decimal.eval() == expected_decimal
        assert isinstance(decimal, Decimal)


def test_decimal_latex_whole_numbers():
    """Test that Decimal.latex() renders whole numbers without decimal point."""
    test_cases = [
        (Decimal(x=0.0), "0"),
        (Decimal(x=1.0), "1"),
        (Decimal(x=5.0), "5"),
        (Decimal(x=42.0), "42"),
        (Decimal(x=-3.0), "-3"),
        (Decimal(x=100.0), "100"),
    ]

    for decimal, expected_latex in test_cases:
        result = decimal.latex()
        assert result == expected_latex


def test_decimal_latex_fractional_numbers():
    """Test that Decimal.latex() renders fractional numbers with period separator."""
    test_cases = [
        (Decimal(x=0.5), "0.5"),
        (Decimal(x=1.25), "1.25"),
        (Decimal(x=3.14159), "3.14159"),
        (Decimal(x=-2.75), "-2.75"),
        (Decimal(x=0.001), "0.001"),
    ]

    for decimal, expected_latex in test_cases:
        result = decimal.latex()
        assert result == expected_latex
        # Ensure no comma is used as decimal separator
        assert "," not in result


def test_integer_as_decimal_latex_output():
    """Test the complete chain: Integer -> as_decimal -> latex()."""
    test_cases = [
        (Integer(n=0), "0"),
        (Integer(n=1), "1"),
        (Integer(n=5), "5"),
        (Integer(n=42), "42"),
        (Integer(n=-3), "-3"),
    ]

    for integer, expected_latex in test_cases:
        result = integer.as_decimal.latex()
        assert result == expected_latex


def test_original_user_scenario():
    """Test the exact scenario that was failing in the user's code."""
    # Reproduce the user's problematic line:
    # p1 = (p * n1).simplified().as_decimal

    # Create test data similar to user's generator
    n1 = Integer(n=3)
    p = Fraction(p=Integer(n=146), q=Integer(n=10))  # 14.6

    # This should not raise AttributeError
    result = (p * n1).simplified()

    # The result might be Integer or Fraction, both should have as_decimal
    assert hasattr(result, "as_decimal")

    # Get the as_decimal value
    decimal_result = result.as_decimal
    assert isinstance(decimal_result, Decimal)

    # Should be able to call latex() on it
    latex_output = decimal_result.latex()
    assert isinstance(latex_output, str)
    assert len(latex_output) > 0


def test_multiplication_scenarios():
    """Test various multiplication scenarios that could result in Integer or Fraction."""
    # Scenario 1: Fraction * Integer -> Integer (when it simplifies to whole number)
    p1 = Fraction(p=Integer(n=10), q=Integer(n=2))  # 5
    n1 = Integer(n=3)
    result1 = (p1 * n1).simplified()

    # Should have as_decimal regardless of final type
    assert hasattr(result1, "as_decimal")
    decimal1 = result1.as_decimal
    assert decimal1.latex() == "15"  # Should be whole number without decimal

    # Scenario 2: Fraction * Integer -> Fraction (when it doesn't simplify to whole)
    p2 = Fraction(p=Integer(n=1), q=Integer(n=3))  # 1/3
    n2 = Integer(n=2)
    result2 = (p2 * n2).simplified()

    assert hasattr(result2, "as_decimal")
    decimal2 = result2.as_decimal
    latex2 = decimal2.latex()
    # Should be a decimal number with period separator
    assert "." in latex2
    assert "," not in latex2


def test_edge_cases():
    """Test edge cases for as_decimal property."""
    # Zero
    zero = Integer(n=0)
    assert zero.as_decimal.latex() == "0"

    # Negative numbers
    neg = Integer(n=-5)
    assert neg.as_decimal.latex() == "-5"

    # Large numbers
    large = Integer(n=999999)
    assert large.as_decimal.latex() == "999999"


def test_consistency_with_fraction_as_decimal():
    """Test that Integer.as_decimal is consistent with Fraction.as_decimal."""
    # Create equivalent values
    integer = Integer(n=5)
    fraction = Fraction(p=Integer(n=5), q=Integer(n=1))  # 5/1 = 5

    # Both should have as_decimal
    int_decimal = integer.as_decimal
    frac_decimal = fraction.as_decimal

    # Should evaluate to same value
    assert int_decimal.eval() == frac_decimal.eval()

    # Should have same LaTeX output
    assert int_decimal.latex() == frac_decimal.latex()


def test_decimal_types_consistency():
    """Test consistency between different Decimal creation methods."""
    # Create same value in different ways
    decimal_x = Decimal(x=5.0)
    decimal_pq = Decimal(p=5, q=1)
    integer_as_decimal = Integer(n=5).as_decimal

    # All should evaluate to same value
    assert decimal_x.eval() == decimal_pq.eval() == integer_as_decimal.eval()

    # All should have same LaTeX output
    latex_x = decimal_x.latex()
    latex_pq = decimal_pq.latex()
    latex_int = integer_as_decimal.latex()

    assert latex_x == latex_pq == latex_int == "5"


def test_no_comma_in_decimal_latex():
    """Test that Decimal.latex() never uses comma as decimal separator."""
    test_values = [0.1, 0.5, 1.5, 3.14159, 99.99, -2.75]

    for value in test_values:
        decimal = Decimal(x=value)
        latex_output = decimal.latex()

        # Should never contain comma
        assert "," not in latex_output

        # If it contains a decimal separator, it should be a period
        if "." in latex_output:
            # Should be valid float representation
            assert float(latex_output) == value


def test_integer_as_percent_property():
    """Test that Integer objects have as_percent property."""
    integer = Integer(n=4)

    # Should have as_percent property
    assert hasattr(integer, "as_percent")

    # Should return an Integer object (since 4 * 100 = 400 is a whole number)
    percent = integer.as_percent
    assert isinstance(percent, Integer)

    # Should have the correct value (multiply by 100)
    assert percent.n == 400
    assert percent.latex() == "400"


def test_integer_as_percent_values():
    """Test as_percent property with various integer values."""
    test_cases = [
        (0, 0),
        (1, 100),
        (2, 200),
        (3, 300),
        (4, 400),
        (5, 500),
        (-1, -100),
        (-2, -200),
    ]

    for int_val, expected_percent in test_cases:
        integer = Integer(n=int_val)
        percent = integer.as_percent

        assert percent.n == expected_percent
        assert isinstance(percent, Integer)
        assert percent.latex() == str(expected_percent)


def test_user_percent_scenario():
    """Test the exact user scenario that was failing."""
    # From the user's code: (n-tm.Integer(n=1)).simplified().as_percent
    n = Integer(n=5)
    result = (n - Integer(n=1)).simplified()

    # This should not raise AttributeError
    percent_result = result.as_percent

    # Should match the expected doctest result
    assert isinstance(percent_result, Integer)
    assert percent_result.n == 400
    assert repr(percent_result) == "Integer(n=400)"
    assert percent_result.latex() == "400"


# Run tests individually for compatibility with existing test framework
if __name__ == "__main__":
    test_functions = [
        test_integer_as_decimal_property,
        test_integer_as_decimal_values,
        test_decimal_latex_whole_numbers,
        test_decimal_latex_fractional_numbers,
        test_integer_as_decimal_latex_output,
        test_original_user_scenario,
        test_multiplication_scenarios,
        test_edge_cases,
        test_consistency_with_fraction_as_decimal,
        test_decimal_types_consistency,
        test_no_comma_in_decimal_latex,
        test_integer_as_percent_property,
        test_integer_as_percent_values,
        test_user_percent_scenario,
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
