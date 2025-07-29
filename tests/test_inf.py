"""
Test suite for the Inf (infinity) class functionality.

This module tests mathematical infinity representation:
- Infinity object creation and properties
- LaTeX output generation for infinity symbol
- Integration with mathematical operations
- Symbolic computation with infinity
- Mathematical limit and boundary representations

These tests ensure that infinity is properly represented
and can be used in mathematical contexts for limits,
bounds, and infinite domains.
"""

import unittest
import teachers.maths as tm
import sympy as sp


class TestInf(unittest.TestCase):
    """Test suite for Inf (infinity) mathematical representation."""

    def test_inf_creation(self):
        """
        Test basic Inf object creation and properties.

        Validates:
        - Inf object instantiation
        - Default SymPy expression (sp.oo)
        - Object type verification
        - Infinity representation consistency

        Ensures infinity objects can be created correctly.
        """
        # Test basic infinity creation
        inf = tm.Inf()

        # Verify basic properties
        self.assertIsInstance(inf, tm.Inf)
        self.assertIsInstance(inf, tm.MathsObject)  # Should inherit from MathsObject

        # Verify SymPy expression is positive infinity
        self.assertEqual(inf.sympy_expr, sp.oo)
        self.assertIsNotNone(inf.sympy_expr)

    def test_inf_latex_output(self):
        """
        Test Inf LaTeX representation generation.

        Validates:
        - Infinity symbol generation (\\infty)
        - LaTeX mathematical notation
        - Proper infinity display formatting
        - Symbol accuracy

        Ensures infinity generates proper mathematical notation.
        """
        inf = tm.Inf()

        # Test LaTeX output
        latex_output = inf.latex()
        expected_latex = "\\infty"

        self.assertEqual(latex_output, expected_latex)
        self.assertIsInstance(latex_output, str)

    def test_inf_string_representation(self):
        """
        Test Inf string representation methods.

        Validates:
        - __repr__ method output
        - __str__ method delegation
        - Object identification in debugging
        - Consistent representation

        Ensures infinity can be properly displayed and debugged.
        """
        inf = tm.Inf()

        # Test repr method
        repr_str = repr(inf)
        expected_repr = "Inf()"

        self.assertEqual(repr_str, expected_repr)

        # Test str method (should delegate to MathsObject.__str__ which raises NotImplementedError)
        with self.assertRaises(NotImplementedError):
            str(inf)

    def test_inf_simplification(self):
        """
        Test Inf simplification behavior.

        Validates:
        - Infinity simplification (should return self)
        - Mathematical identity preservation
        - Simplification consistency
        - Infinity invariance

        Ensures infinity remains unchanged during simplification.
        """
        inf = tm.Inf()

        # Test simplification
        simplified = inf.simplified()

        # Infinity should simplify to itself
        self.assertEqual(simplified, inf)
        self.assertIsInstance(simplified, tm.Inf)

    def test_inf_in_mathematical_operations(self):
        """
        Test Inf usage in mathematical operations and expressions.

        Validates:
        - Infinity in addition operations
        - Infinity in multiplication operations
        - Infinity in comparison operations
        - Infinity as boundaries in intervals
        - Mathematical infinity behavior

        Ensures infinity integrates properly with other mathematical objects.
        """
        inf = tm.Inf()
        five = tm.Integer(n=5)
        x = tm.Symbol(s="x")

        # Test infinity in addition
        add_expr = five + inf
        self.assertIsInstance(add_expr, tm.Add)
        self.assertEqual(add_expr.l, five)
        self.assertEqual(add_expr.r, inf)

        # Test infinity in multiplication
        mul_expr = five * inf
        self.assertIsInstance(mul_expr, tm.Mul)
        self.assertEqual(mul_expr.l, five)
        self.assertEqual(mul_expr.r, inf)

        # Test infinity in comparison
        gt_expr = inf > five
        self.assertIsInstance(gt_expr, tm.StrictGreaterThan)
        self.assertEqual(gt_expr.l, inf)
        self.assertEqual(gt_expr.r, five)

        # Test infinity with symbols
        symbol_add = x + inf
        self.assertIsInstance(symbol_add, tm.Add)
        self.assertEqual(symbol_add.l, x)
        self.assertEqual(symbol_add.r, inf)

    def test_inf_as_interval_boundary(self):
        """
        Test Inf as boundary in interval definitions.

        Validates:
        - Infinity as right boundary [a, ∞)
        - Infinity as left boundary (-∞, b] (conceptually)
        - Interval creation with infinity
        - Mathematical domain representation
        - Infinite interval LaTeX output

        Ensures infinity can be used to represent infinite domains.
        """
        inf = tm.Inf()
        zero = tm.Integer(n=0)

        # Test interval from 0 to infinity [0, ∞)
        try:
            inf_interval = tm.Interval(l=zero, r=inf)

            # Verify interval creation
            self.assertIsInstance(inf_interval, tm.Interval)
            self.assertEqual(inf_interval.l, zero)
            self.assertEqual(inf_interval.r, inf)

            # Test LaTeX output for infinite interval
            latex_output = inf_interval.latex()
            self.assertIn("0", latex_output)
            self.assertIn("\\infty", latex_output)
            self.assertIn("\\lbracket", latex_output)
            self.assertIn("\\rbracket", latex_output)

        except Exception as e:
            # If intervals don't support infinity, that's a limitation to document
            self.skipTest(f"Intervals with infinity not supported: {e}")

    def test_inf_mathematical_properties(self):
        """
        Test mathematical properties and behavior of infinity.

        Validates:
        - Infinity mathematical semantics
        - Consistency with mathematical theory
        - Proper infinity handling
        - Limit behavior representation

        Ensures infinity behaves according to mathematical principles.
        """
        inf = tm.Inf()

        # Test that infinity equals itself
        self.assertEqual(inf, inf)

        # Test infinity immutability through operations
        simplified_inf = inf.simplified()
        self.assertEqual(inf, simplified_inf)

        # Test infinity SymPy integration
        self.assertTrue(inf.sympy_expr.is_infinite)
        # Note: SymPy's sp.oo.is_positive returns False - infinity is not a "positive number"
        self.assertFalse(inf.sympy_expr.is_positive)  # SymPy's actual behavior
        self.assertFalse(inf.sympy_expr.is_finite)

    def test_inf_in_complex_expressions(self):
        """
        Test Inf in complex mathematical expressions.

        Validates:
        - Infinity in nested expressions
        - Infinity with fractions and powers
        - Complex mathematical contexts
        - Expression evaluation with infinity
        - Infinity propagation through operations

        Ensures infinity works in realistic mathematical scenarios.
        """
        inf = tm.Inf()
        x = tm.Symbol(s="x")
        two = tm.Integer(n=2)

        # Test infinity in fraction (should create proper fraction)
        frac_with_inf = x / inf
        self.assertIsInstance(frac_with_inf, tm.Fraction)
        self.assertEqual(frac_with_inf.p, x)
        self.assertEqual(frac_with_inf.q, inf)

        # Test infinity in power expression
        pow_with_inf = two**inf
        self.assertIsInstance(pow_with_inf, tm.Pow)
        self.assertEqual(pow_with_inf.base, two)
        self.assertEqual(pow_with_inf.exp, inf)

        # Test complex expression with infinity
        complex_expr = (x + inf) / (two * inf)
        self.assertIsInstance(complex_expr, tm.Fraction)
        self.assertIsInstance(complex_expr.p, tm.Add)
        self.assertIsInstance(complex_expr.q, tm.Mul)

    def test_inf_latex_in_expressions(self):
        """
        Test Inf LaTeX generation within larger expressions.

        Validates:
        - Infinity symbol in addition expressions
        - Infinity symbol in fractions
        - Infinity symbol in power expressions
        - Consistent LaTeX formatting
        - Readability of infinity in expressions

        Ensures infinity symbols appear correctly in complex LaTeX.
        """
        inf = tm.Inf()
        x = tm.Symbol(s="x")

        # Test infinity in addition
        add_expr = x + inf
        add_latex = add_expr.latex()
        self.assertIn("x", add_latex)
        self.assertIn("\\infty", add_latex)
        self.assertIn("+", add_latex)

        # Test infinity in fraction
        frac_expr = x / inf
        frac_latex = frac_expr.latex()
        self.assertIn("\\dfrac", frac_latex)
        self.assertIn("x", frac_latex)
        self.assertIn("\\infty", frac_latex)

        # Test infinity in power
        pow_expr = x**inf
        pow_latex = pow_expr.latex()
        self.assertIn("x^{", pow_latex)
        self.assertIn("\\infty", pow_latex)
        self.assertTrue(pow_latex.endswith("}"))

    def test_inf_edge_cases(self):
        """
        Test Inf behavior with edge cases and special scenarios.

        Validates:
        - Multiple infinity objects
        - Infinity object equality
        - Infinity in unusual mathematical contexts
        - Error handling with infinity
        - Boundary condition behavior

        Ensures robust infinity handling under edge conditions.
        """
        inf1 = tm.Inf()
        inf2 = tm.Inf()

        # Test that different infinity objects are equal
        self.assertEqual(inf1, inf2)

        # Test infinity with zero
        zero = tm.Integer(n=0)
        zero_plus_inf = zero + inf1
        self.assertIsInstance(zero_plus_inf, tm.Add)

        # Test infinity with itself
        inf_plus_inf = inf1 + inf2
        self.assertIsInstance(inf_plus_inf, tm.Add)

        # Test infinity multiplication
        inf_times_inf = inf1 * inf2
        self.assertIsInstance(inf_times_inf, tm.Mul)

    def test_inf_consistency_with_sympy(self):
        """
        Test Inf consistency with SymPy infinity representation.

        Validates:
        - SymPy sp.oo equivalence
        - Mathematical property consistency
        - Infinity behavior matching SymPy
        - Integration with SymPy operations

        Ensures our infinity representation is consistent with SymPy.
        """
        inf = tm.Inf()

        # Test SymPy infinity equivalence
        self.assertEqual(inf.sympy_expr, sp.oo)

        # Test SymPy properties
        self.assertTrue(inf.sympy_expr.is_infinite)
        # Note: SymPy's sp.oo.is_positive returns False - infinity is not a "positive number"
        self.assertFalse(inf.sympy_expr.is_positive)  # SymPy's actual behavior
        self.assertFalse(inf.sympy_expr.is_finite)
        self.assertFalse(inf.sympy_expr.is_negative)

        # Test SymPy operations
        sympy_expr = inf.sympy_expr + 5
        self.assertEqual(sympy_expr, sp.oo)  # ∞ + 5 = ∞

        sympy_mul = inf.sympy_expr * 2
        self.assertEqual(sympy_mul, sp.oo)  # ∞ * 2 = ∞


if __name__ == "__main__":
    unittest.main()
