"""Test suite for Mul simplification operations.

This test suite addresses the NotImplementedError when simplifying
Mul operations involving nested Mul objects, particularly when
expanding polynomial expressions like (ax + b)^2.

The specific error occurs when trying to simplify expressions like:
- Integer * Mul(Integer, Symbol)
- Mul(Integer, Symbol) * Integer
- Other combinations involving nested Mul objects

This is similar to the Add simplification bug fixed in version 0.0.7.
"""

from teachers.maths import Integer, Symbol, Mul, Add, Pow


def test_integer_times_mul_integer_symbol():
    """Test Integer * Mul(Integer, Symbol) simplification."""
    # This represents: 2 * (3 * x) = 6x
    x = Symbol(s="x")
    inner_mul = Mul(l=Integer(n=3), r=x)
    outer_mul = Mul(l=Integer(n=2), r=inner_mul)

    result = outer_mul.simplified()
    expected = Mul(l=Integer(n=6), r=x)

    assert result == expected


def test_mul_integer_symbol_times_integer():
    """Test Mul(Integer, Symbol) * Integer simplification."""
    # This represents: (3 * x) * 2 = 6x
    x = Symbol(s="x")
    inner_mul = Mul(l=Integer(n=3), r=x)
    outer_mul = Mul(l=inner_mul, r=Integer(n=2))

    result = outer_mul.simplified()
    expected = Mul(l=Integer(n=6), r=x)

    assert result == expected


def test_polynomial_expansion_scenario():
    """Test the exact scenario from user's code: (ax + b)^2 expansion."""
    # This reproduces the user's failing case
    x = Symbol(s="x")
    a = Integer(n=3)
    b = Integer(n=4)

    # Create (3x + 4)^2
    polynomial = Pow(base=Add(l=Mul(l=a, r=x), r=b), exp=Integer(n=2))

    # This should expand to: 9x^2 + 24x + 16
    # During expansion, we get terms like: 2 * (3 * x) * 4 = 24x
    result = polynomial.simplified()

    # The result should be an Add expression with three terms
    assert isinstance(result, Add)
    # We'll verify the structure matches expected polynomial expansion


def test_nested_mul_with_different_coefficients():
    """Test various coefficient combinations in nested Mul operations."""
    x = Symbol(s="x")

    test_cases = [
        # (coeff1, coeff2, expected_result)
        (2, 3, 6),
        (-2, 3, -6),
        (2, -3, -6),
        (-2, -3, 6),
        (1, 5, 5),
        (0, 3, 0),  # Should handle zero multiplication
    ]

    for coeff1, coeff2, expected_coeff in test_cases:
        inner_mul = Mul(l=Integer(n=coeff1), r=x)
        outer_mul = Mul(l=Integer(n=coeff2), r=inner_mul)

        result = outer_mul.simplified()

        if expected_coeff == 0:
            assert result == Integer(n=0)
        elif expected_coeff == 1:
            assert result == x
        else:
            expected = Mul(l=Integer(n=expected_coeff), r=x)
            assert result == expected


def test_mul_associativity_flattening():
    """Test that nested Mul operations are properly flattened."""
    # Test: a * (b * (c * x)) should flatten to (a*b*c) * x
    x = Symbol(s="x")

    # Build nested: 2 * (3 * (4 * x))
    innermost = Mul(l=Integer(n=4), r=x)
    middle = Mul(l=Integer(n=3), r=innermost)
    outermost = Mul(l=Integer(n=2), r=middle)

    result = outermost.simplified()
    expected = Mul(l=Integer(n=24), r=x)  # 2 * 3 * 4 = 24

    assert result == expected


def test_mul_with_zero_coefficient():
    """Test multiplication by zero simplifies correctly."""
    x = Symbol(s="x")

    # 0 * (3 * x) = 0
    inner_mul = Mul(l=Integer(n=3), r=x)
    zero_mul = Mul(l=Integer(n=0), r=inner_mul)

    result = zero_mul.simplified()
    assert result == Integer(n=0)


def test_mul_with_one_coefficient():
    """Test multiplication by one simplifies correctly."""
    x = Symbol(s="x")

    # 1 * (3 * x) = 3 * x
    inner_mul = Mul(l=Integer(n=3), r=x)
    one_mul = Mul(l=Integer(n=1), r=inner_mul)

    result = one_mul.simplified()
    expected = Mul(l=Integer(n=3), r=x)

    assert result == expected


def test_complex_polynomial_expansion_terms():
    """Test individual terms that appear in polynomial expansion."""
    x = Symbol(s="x")
    a = Integer(n=3)
    b = Integer(n=4)

    # Test the cross term: 2 * a * x * b = 2 * 3 * x * 4 = 24x
    # This is the problematic term from (ax + b)^2 expansion
    cross_term = Mul(l=Integer(n=2), r=Mul(l=Mul(l=a, r=x), r=b))

    result = cross_term.simplified()
    expected = Mul(l=Integer(n=24), r=x)  # 2 * 3 * 4 = 24

    assert result == expected


def test_reproduction_of_user_error():
    """Direct reproduction of the user's failing scenario."""
    # This should reproduce the exact error message:
    # "Simplification of Mul of and l=Integer(n=2) r=Mul(l=Integer(n=3), r=Symbol(s='x'))"

    x = Symbol(s="x")
    inner_mul = Mul(l=Integer(n=3), r=x)  # 3x
    outer_mul = Mul(l=Integer(n=2), r=inner_mul)  # 2 * (3x)

    # This should not raise NotImplementedError
    result = outer_mul.simplified()

    # Should simplify to 6x
    expected = Mul(l=Integer(n=6), r=x)
    assert result == expected


# Run tests individually for compatibility with existing test framework
if __name__ == "__main__":
    test_functions = [
        test_integer_times_mul_integer_symbol,
        test_mul_integer_symbol_times_integer,
        test_polynomial_expansion_scenario,
        test_nested_mul_with_different_coefficients,
        test_mul_associativity_flattening,
        test_mul_with_zero_coefficient,
        test_mul_with_one_coefficient,
        test_complex_polynomial_expansion_terms,
        test_reproduction_of_user_error,
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
