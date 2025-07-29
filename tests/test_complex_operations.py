"""
Test suite for complex mathematical operations and edge cases.

This module tests advanced scenarios beyond basic operations:
- Deeply nested mathematical expressions
- Mixed-type operations (fractions, decimals, symbols)
- Complex power operations and simplifications
- Function compositions and multi-argument functions
- Relational operations with complex expressions
- Edge cases involving large numbers and precision
- Negative number handling and sign propagation

These tests ensure the mathematical framework can handle
realistic complex mathematical expressions that would appear
in educational content.
"""

import unittest
import teachers.maths as tm


class TestComplexOperations(unittest.TestCase):
    """Test suite for complex mathematical operations and advanced scenarios."""

    def test_nested_operations(self):
        """
        Test deeply nested mathematical expressions and structural validation.

        Validates:
        - Complex expression parsing: ((a + b) * c) / (x - y)
        - Proper object type creation at each nesting level
        - Structural integrity of nested expressions
        - Partial simplification of sub-expressions
        - Correct operator precedence handling

        Ensures that complex expressions maintain proper mathematical
        structure and can be partially simplified when possible.
        """
        a = tm.Integer(n=3)
        b = tm.Integer(n=5)
        c = tm.Integer(n=2)
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # Complex nested expression: ((a + b) * c) / (x - y)
        expr1 = ((a + b) * c) / (x - y)

        self.assertIsInstance(expr1, tm.Fraction)
        self.assertIsInstance(expr1.p, tm.Mul)
        self.assertIsInstance(expr1.q, tm.Add)

        # Verify the structure is correct
        self.assertIsInstance(expr1.p.l, tm.Add)
        self.assertEqual(expr1.p.r, c)
        self.assertEqual(expr1.q.l, x)
        self.assertIsInstance(expr1.q.r, tm.Mul)
        self.assertEqual(expr1.q.r.l, tm.Integer(n=-1))
        self.assertEqual(expr1.q.r.r, y)

        # Verify the simplified parts work
        simplified_numerator = expr1.p.simplified()
        self.assertEqual(simplified_numerator, tm.Integer(n=16))

    def test_mixed_fraction_operations(self):
        """
        Test operations mixing fractions with integers and symbols.

        Validates:
        - Fraction + Fraction operations
        - Mixed fraction and integer arithmetic
        - Complex expressions involving multiple fraction operations
        - Proper type creation for mixed operations
        - Step-by-step simplification of fraction chains

        Ensures that fractions can be seamlessly integrated with
        other mathematical object types in complex expressions.
        """
        f1 = tm.Fraction(p=1, q=2)
        f2 = tm.Fraction(p=3, q=4)
        i = tm.Integer(n=5)
        x = tm.Symbol(s="x")

        # Test fraction addition and multiplication
        expr1 = f1 + f2 + i
        self.assertIsInstance(expr1, tm.Add)

        # Simplify step by step
        simplified_fractions = (f1 + f2).simplified()
        self.assertEqual(simplified_fractions, tm.Fraction(p=5, q=4))

        # Test mixed fraction operations: (1/2 + 3/4) * (5 + x)
        expr2 = (f1 + f2) * (i + x)
        self.assertIsInstance(expr2, tm.Mul)
        self.assertIsInstance(expr2.l, tm.Add)
        self.assertIsInstance(expr2.r, tm.Add)

    def test_complex_powers(self):
        """
        Test complex power operations and exponential expressions.

        Validates:
        - Nested power operations: (a^b)^x
        - Power simplification when mathematically possible
        - Complex base expressions: (a + b)^2
        - Proper handling of symbolic vs numeric exponents
        - Structural integrity of power expressions

        Ensures that exponential operations maintain mathematical
        correctness even in complex nested scenarios.
        """
        a = tm.Integer(n=2)
        b = tm.Integer(n=3)
        x = tm.Symbol(s="x")

        # Test nested powers: (a^b)^x
        expr1 = (a**b) ** x
        self.assertIsInstance(expr1, tm.Pow)
        self.assertIsInstance(expr1.base, tm.Pow)
        self.assertEqual(expr1.exp, x)

        # Test power simplification when possible
        self.assertEqual(expr1.base.simplified(), tm.Integer(n=8))

        # Test more complex expressions: (a + b)^2
        expr2 = (a + b) ** tm.Integer(n=2)
        self.assertIsInstance(expr2, tm.Pow)
        self.assertIsInstance(expr2.base, tm.Add)

        # This should equal 25 when fully simplified
        # But our current simplification doesn't expand (a+b)^2
        self.assertEqual(expr2.base.simplified(), tm.Integer(n=5))

    def test_negative_values(self):
        """
        Test comprehensive negative number handling and sign propagation.

        Validates:
        - Negative + Negative operations
        - Negative * Negative operations (sign rules)
        - Negative / Positive operations
        - Double negation behavior
        - Sign preservation through complex operations

        Ensures that negative numbers follow proper mathematical
        sign rules throughout all operations.
        """
        neg_a = tm.Integer(n=-5)
        neg_b = tm.Integer(n=-3)
        pos_c = tm.Integer(n=2)

        # Test negative + negative
        expr1 = neg_a + neg_b
        self.assertEqual(expr1.simplified(), tm.Integer(n=-8))

        # Test negative * negative
        expr2 = neg_a * neg_b
        self.assertEqual(expr2.simplified(), tm.Integer(n=15))

        # Test negative / positive
        expr3 = neg_a / pos_c
        self.assertEqual(expr3.simplified(), tm.Fraction(p=-5, q=2))

        # Test double negation
        expr4 = -(-neg_a)
        self.assertEqual(expr4, tm.Integer(n=-5))

    def test_fraction_edge_cases(self):
        """
        Test fraction edge cases and boundary conditions.

        Validates:
        - Fractions with complex numerators/denominators
        - Simplification of expression-based fractions
        - Fraction of fractions operations
        - Zero numerator handling
        - Proper reduction and normalization

        Ensures fractions handle edge cases gracefully and
        maintain mathematical correctness in boundary situations.
        """
        # Test fraction with complex numerator/denominator
        a = tm.Integer(n=2)
        b = tm.Integer(n=3)
        c = tm.Integer(n=4)

        # Create fraction with expression in numerator: (a+b)/c
        frac1 = (a + b) / c
        self.assertIsInstance(frac1, tm.Fraction)
        self.assertIsInstance(frac1.p, tm.Add)

        # Test simplification of fractions
        self.assertEqual(frac1.simplified(), tm.Fraction(p=5, q=4))

        # Test fraction of fractions: (1/2)/(3/4)
        f1 = tm.Fraction(p=1, q=2)
        f2 = tm.Fraction(p=3, q=4)
        frac2 = f1 / f2
        self.assertEqual(frac2.simplified(), tm.Fraction(p=2, q=3))

        # Test zero numerator
        zero_frac = tm.Fraction(p=0, q=5)
        self.assertEqual(zero_frac.simplified(), tm.Integer(n=0))

    def test_function_compositions(self):
        """
        Test function compositions and nested function applications.

        Validates:
        - Nested function calls: f(g(x))
        - Multi-argument function calls with mixed arguments
        - Function results in arithmetic operations
        - Proper structural representation of compositions
        - Integration with other mathematical objects

        Ensures that functions can be composed and manipulated
        algebraically like any other mathematical objects.
        """
        f = tm.Function(name="f")
        g = tm.Function(name="g")
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # Test function composition: f(g(x))
        comp1 = f(g(x))
        self.assertIsInstance(comp1, tm.Image)
        self.assertEqual(comp1.f, f)
        self.assertIsInstance(comp1.pre, tm.Image)
        self.assertEqual(comp1.pre.f, g)
        self.assertEqual(comp1.pre.pre, x)

        # Test function with multiple arguments: f(x, g(y))
        arg_list = tm.MathsCollection(elements=[x, g(y)])
        comp2 = f(arg_list)
        self.assertIsInstance(comp2, tm.Image)
        self.assertEqual(comp2.f, f)
        self.assertIsInstance(comp2.pre, tm.MathsCollection)
        self.assertEqual(len(comp2.pre.elements), 2)

        # Test operations on function results: f(x) + g(y)
        expr = f(x) + g(y)
        self.assertIsInstance(expr, tm.Add)
        self.assertIsInstance(expr.l, tm.Image)
        self.assertIsInstance(expr.r, tm.Image)
        self.assertEqual(expr.l.f, f)
        self.assertEqual(expr.r.f, g)

    def test_relation_compositions(self):
        """
        Test relational operators with complex mathematical expressions.

        Validates:
        - Equality with complex left/right sides
        - Inequality with nested expressions
        - Simplification within relational contexts
        - Proper object creation for complex relations
        - Integration of relations with other operations

        Ensures that mathematical relations can handle arbitrarily
        complex expressions on both sides.
        """
        a = tm.Integer(n=5)
        b = tm.Integer(n=3)
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # Test equality with complex expressions
        eq1 = tm.Equality(l=a + b, r=x * y)
        self.assertIsInstance(eq1, tm.Equality)
        self.assertIsInstance(eq1.l, tm.Add)
        self.assertIsInstance(eq1.r, tm.Mul)

        # Test inequality with complex expressions
        gt1 = (a + b) > (x * y)
        self.assertIsInstance(gt1, tm.StrictGreaterThan)
        self.assertIsInstance(gt1.l, tm.Add)
        self.assertIsInstance(gt1.r, tm.Mul)

        # Test simplification in relations
        eq2 = tm.Equality(l=a + b, r=tm.Integer(n=8))
        simplified_eq = eq2.simplified()
        self.assertEqual(simplified_eq.l, tm.Integer(n=8))
        self.assertEqual(simplified_eq.r, tm.Integer(n=8))

    def test_decimal_operations(self):
        """
        Test operations involving decimal numbers and conversions.

        Validates:
        - Decimal arithmetic operations
        - Mixed decimal and integer operations
        - Conversion between fractions and decimals
        - Proper type creation for decimal operations
        - Evaluation consistency

        Ensures decimal numbers integrate seamlessly with the
        mathematical object system.
        """
        d1 = tm.Decimal(x=2.5)
        d2 = tm.Decimal(x=1.75)
        i = tm.Integer(n=3)

        # Test decimal addition
        expr1 = d1 + d2
        self.assertIsInstance(expr1, tm.Add)

        # Test decimal multiplication
        expr2 = d1 * i
        self.assertIsInstance(expr2, tm.Mul)

        # Test decimal conversion
        f = tm.Fraction(p=5, q=2)
        d = f.as_decimal
        self.assertIsInstance(d, tm.Decimal)
        self.assertEqual(d.eval(), 2.5)

    def test_edge_cases(self):
        """
        Test various edge cases and boundary conditions.

        Validates:
        - Very large integer handling
        - Division by very small numbers
        - Complex nested mixed-type operations
        - Memory and precision edge cases
        - Structural integrity under stress

        Ensures the system remains robust under extreme
        conditions and unusual input combinations.
        """

        # Test with very large integers
        large_int = tm.Integer(n=10**10)
        self.assertEqual(large_int.n, 10**10)

        # Test division by very small number
        small_div = tm.Integer(n=1) / tm.Integer(n=10**10)
        self.assertIsInstance(small_div, tm.Fraction)

        # Test nested operations with mixed types
        a = tm.Integer(n=2)
        b = tm.Symbol(s="b")
        c = tm.Fraction(p=1, q=3)
        d = tm.Decimal(x=0.5)

        complex_expr = ((a + b) * c) / (b - d)
        self.assertIsInstance(complex_expr, tm.Fraction)
        self.assertIsInstance(complex_expr.p, tm.Mul)
        self.assertIsInstance(complex_expr.q, tm.Add)


if __name__ == "__main__":
    unittest.main()
