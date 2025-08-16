"""
Test suite for the Pi (mathematical constant π) class functionality.

This module tests mathematical pi constant representation:
- Pi object creation and properties
- LaTeX output generation for pi symbol
- Integration with mathematical operations (multiplication, addition, powers)
- Symbolic computation with pi
- Numerical evaluation and precision
- Mathematical formulas involving pi (geometry, trigonometry)

These tests ensure that pi is properly represented
and can be used in mathematical contexts for geometric
calculations, trigonometric functions, and analytical expressions.
"""

import unittest
import math
import teachers.maths as tm
import sympy as sp


class TestPi(unittest.TestCase):
    """Test suite for Pi (mathematical constant π) representation."""

    def test_pi_creation(self):
        """
        Test basic Pi object creation and properties.

        Validates:
        - Pi object instantiation
        - Default SymPy expression (sp.pi)
        - Object type verification
        - Pi representation consistency

        Ensures pi objects can be created correctly.
        """
        # Test basic pi creation
        pi = tm.Pi()

        # Verify basic properties
        self.assertIsInstance(pi, tm.Pi)
        self.assertIsInstance(pi, tm.MathsObject)  # Should inherit from MathsObject

        # Verify SymPy expression is pi
        self.assertEqual(pi.sympy_expr, sp.pi)
        self.assertIsNotNone(pi.sympy_expr)

    def test_pi_latex_output(self):
        """
        Test Pi LaTeX representation generation.

        Validates:
        - Proper LaTeX infinity symbol (\\pi)
        - String format consistency
        - Mathematical notation standards
        - Integration with LaTeX rendering pipeline

        Ensures pi generates correct LaTeX for mathematical display.
        """
        pi = tm.Pi()

        # Test LaTeX output
        latex_output = pi.latex()
        expected_latex = "\\pi"
        self.assertEqual(latex_output, expected_latex)

        # Verify LaTeX is a string
        self.assertIsInstance(latex_output, str)
        self.assertGreater(len(latex_output), 0)

    def test_pi_numerical_evaluation(self):
        """
        Test Pi numerical evaluation.

        Validates:
        - eval() method returns correct float value
        - Precision matches standard mathematical pi
        - Consistency with math.pi and sympy.pi
        - Numerical accuracy for calculations

        Ensures pi evaluates to correct numerical value.
        """
        pi = tm.Pi()

        # Test numerical evaluation
        pi_value = pi.eval()
        expected_value = math.pi

        # Should be a float
        self.assertIsInstance(pi_value, float)

        # Should match math.pi
        self.assertEqual(pi_value, expected_value)

        # Should be approximately 3.14159...
        self.assertAlmostEqual(pi_value, 3.141592653589793, places=10)

        # Should match SymPy's pi evaluation
        sympy_pi_value = float(sp.pi)
        self.assertEqual(pi_value, sympy_pi_value)

    def test_pi_string_representation(self):
        """
        Test Pi string representation methods.

        Validates:
        - __repr__ method output format
        - __str__ method consistency
        - String representation standards
        - Debug output formatting

        Ensures pi has proper string representations.
        """
        pi = tm.Pi()

        # Test repr
        repr_output = repr(pi)
        expected_repr = "Pi()"
        self.assertEqual(repr_output, expected_repr)

        # Test str (should match repr for consistency)
        str_output = str(pi)
        self.assertEqual(str_output, expected_repr)

        # Verify string types
        self.assertIsInstance(repr_output, str)
        self.assertIsInstance(str_output, str)

    def test_pi_simplification(self):
        """
        Test Pi simplification behavior.

        Validates:
        - simplified() returns self (pi is already in simplest form)
        - Simplification preserves object identity
        - Mathematical simplification rules
        - Consistency with other constants

        Ensures pi simplification behaves correctly.
        """
        pi = tm.Pi()

        # Test simplification
        simplified_pi = pi.simplified()

        # Should return the same object (pi is already simplified)
        self.assertIs(simplified_pi, pi)
        self.assertEqual(simplified_pi, pi)

        # Should still be Pi type
        self.assertIsInstance(simplified_pi, tm.Pi)

    def test_pi_equality_and_identity(self):
        """
        Test Pi object equality and identity behavior.

        Validates:
        - Multiple Pi objects are equal
        - Object identity behavior
        - Equality comparison methods
        - Hash consistency (if applicable)

        Ensures pi objects behave consistently in comparisons.
        """
        pi1 = tm.Pi()
        pi2 = tm.Pi()

        # Test equality
        self.assertEqual(pi1, pi2)

        # Test that they have the same SymPy expression
        self.assertEqual(pi1.sympy_expr, pi2.sympy_expr)

        # Test that they generate the same LaTeX
        self.assertEqual(pi1.latex(), pi2.latex())

        # Test that they evaluate to the same value
        self.assertEqual(pi1.eval(), pi2.eval())

    def test_pi_multiplication_with_integers(self):
        """
        Test Pi multiplication with Integer objects.

        Validates:
        - Integer * Pi multiplication
        - Pi * Integer multiplication (commutative)
        - Proper coefficient ordering in results
        - LaTeX rendering of multiplied expressions

        Ensures pi works correctly with integer coefficients.
        """
        pi = tm.Pi()

        # Test 2 * pi
        two = tm.Integer(n=2)
        two_pi = two * pi
        self.assertIsInstance(two_pi, tm.Mul)

        # Test simplification and LaTeX
        simplified = two_pi.simplified()
        latex_output = simplified.latex()
        self.assertEqual(latex_output, "2\\pi")

        # Test commutative property: pi * 2
        pi_two = pi * two
        simplified_commute = pi_two.simplified()
        latex_commute = simplified_commute.latex()
        self.assertEqual(latex_commute, "2\\pi")  # Should maintain coefficient-first ordering

        # Test other integers
        three = tm.Integer(n=3)
        three_pi = three * pi
        self.assertEqual(three_pi.simplified().latex(), "3\\pi")

        # Test negative integers
        neg_one = tm.Integer(n=-1)
        neg_pi = neg_one * pi
        self.assertEqual(neg_pi.simplified().latex(), "-\\pi")

    def test_pi_multiplication_with_fractions(self):
        """
        Test Pi multiplication with Fraction objects.

        Validates:
        - Fraction * Pi multiplication
        - Pi * Fraction multiplication (commutative)
        - Proper LaTeX rendering with fractions
        - Mathematical accuracy of fractional coefficients

        Ensures pi works correctly with fractional coefficients.
        """
        pi = tm.Pi()

        # Test 1/2 * pi
        half = tm.Fraction(p=1, q=2)
        half_pi = half * pi
        simplified = half_pi.simplified()
        latex_output = simplified.latex()
        self.assertEqual(latex_output, "\\dfrac{1}{2}\\pi")

        # Test commutative property
        pi_half = pi * half
        simplified_commute = pi_half.simplified()
        latex_commute = simplified_commute.latex()
        self.assertEqual(latex_commute, "\\dfrac{1}{2}\\pi")

        # Test other fractions
        third = tm.Fraction(p=1, q=3)
        third_pi = third * pi
        self.assertEqual(third_pi.simplified().latex(), "\\dfrac{1}{3}\\pi")

        # Test improper fractions
        seven_thirds = tm.Fraction(p=7, q=3)
        complex_pi = seven_thirds * pi
        self.assertEqual(complex_pi.simplified().latex(), "\\dfrac{7}{3}\\pi")

    def test_pi_multiplication_with_decimals(self):
        """
        Test Pi multiplication with Decimal objects.

        Validates:
        - Decimal * Pi multiplication
        - Pi * Decimal multiplication (commutative)
        - Both p/q and x forms of Decimal objects
        - Proper LaTeX rendering with decimal coefficients

        Ensures pi works correctly with decimal coefficients.
        """
        pi = tm.Pi()

        # Test 0.5 * pi (using p/q form)
        half_decimal = tm.Decimal(p=1, q=2)
        half_pi = half_decimal * pi
        simplified = half_pi.simplified()
        latex_output = simplified.latex()
        self.assertEqual(latex_output, "0.5\\pi")

        # Test commutative property
        pi_half = pi * half_decimal
        simplified_commute = pi_half.simplified()
        latex_commute = simplified_commute.latex()
        self.assertEqual(latex_commute, "0.5\\pi")

        # Test x form decimal
        decimal_x = tm.Decimal(x=0.75)
        decimal_pi = decimal_x * pi
        self.assertEqual(decimal_pi.simplified().latex(), "0.75\\pi")

        # Test whole number decimal
        two_decimal = tm.Decimal(x=2.0)
        two_pi = two_decimal * pi
        self.assertEqual(two_pi.simplified().latex(), "2\\pi")

    def test_pi_in_geometric_formulas(self):
        """
        Test Pi in common geometric formulas.

        Validates:
        - Circle area: π * r²
        - Circle circumference: 2 * π * r  
        - Cylinder volume: π * r² * h
        - Sphere volume: (4/3) * π * r³

        Ensures pi works correctly in real-world geometric contexts.
        """
        pi = tm.Pi()
        r = tm.Symbol(s="r")
        h = tm.Symbol(s="h")

        # Circle area: A = π * r²
        r_squared = r ** tm.Integer(n=2)
        area = pi * r_squared
        area_latex = area.simplified().latex()
        self.assertEqual(area_latex, "\\pir^{2}")

        # Circle circumference: C = 2 * π * r
        two = tm.Integer(n=2)
        circumference = two * pi * r
        circ_latex = circumference.simplified().latex()
        self.assertEqual(circ_latex, "2\\pir")

        # Cylinder volume: V = π * r² * h
        cylinder_volume = pi * r_squared * h
        cyl_latex = cylinder_volume.simplified().latex()
        self.assertEqual(cyl_latex, "\\pir^{2}h")

        # Sphere volume: V = (4/3) * π * r³
        four_thirds = tm.Fraction(p=4, q=3)
        r_cubed = r ** tm.Integer(n=3)
        sphere_volume = four_thirds * pi * r_cubed
        sphere_latex = sphere_volume.simplified().latex()
        self.assertEqual(sphere_latex, "\\dfrac{4}{3}\\pir^{3}")

    def test_pi_original_failing_case(self):
        """
        Test the exact case from the original error report.

        Validates:
        - tm.Fraction(p=1, q=3) * tm.Pi() * r**tm.Integer(n=2) * h
        - Complex expression simplification
        - Proper LaTeX rendering of the full formula
        - No NotImplementedError exceptions

        Ensures the original generator failure is completely resolved.
        """
        # Reproduce the exact original failing case
        r = tm.Symbol(s="r")
        h = tm.Symbol(s="h")
        pi = tm.Pi()

        # This should not raise NotImplementedError anymore
        volume_expr = tm.Fraction(p=1, q=3) * pi * r**tm.Integer(n=2) * h
        
        # Verify it simplifies without errors
        result = volume_expr.simplified()
        self.assertIsNotNone(result)

        # Verify LaTeX works
        latex_output = result.latex()
        self.assertIsInstance(latex_output, str)
        self.assertGreater(len(latex_output), 0)

        # Should contain the expected components
        self.assertIn("\\dfrac{1}{3}", latex_output)
        self.assertIn("\\pi", latex_output)
        self.assertIn("r", latex_output)
        self.assertIn("h", latex_output)

        print(f"✅ Original failing case fixed: {latex_output}")

    def test_pi_addition_operations(self):
        """
        Test Pi in addition operations.

        Validates:
        - Pi + Integer combinations
        - Pi + Decimal combinations  
        - Pi + Fraction combinations
        - Proper LaTeX rendering of sums

        Ensures pi works correctly in additive expressions.
        """
        pi = tm.Pi()

        # Test pi + 1
        one = tm.Integer(n=1)
        pi_plus_one = pi + one
        latex_sum = pi_plus_one.simplified().latex()
        self.assertEqual(latex_sum, "\\pi + 1")

        # Test pi + 0.5
        half = tm.Decimal(p=1, q=2)
        pi_plus_half = pi + half
        latex_decimal = pi_plus_half.simplified().latex()
        self.assertEqual(latex_decimal, "\\pi + 0.5")

        # Test pi + 1/4
        quarter = tm.Fraction(p=1, q=4)
        pi_plus_quarter = pi + quarter
        latex_frac = pi_plus_quarter.simplified().latex()
        self.assertEqual(latex_frac, "\\pi + \\dfrac{1}{4}")

    def test_pi_sympy_integration(self):
        """
        Test Pi integration with SymPy operations.

        Validates:
        - SymPy expression compatibility
        - Symbolic manipulation accuracy
        - Numerical evaluation consistency
        - Mathematical property preservation

        Ensures pi maintains SymPy compatibility for advanced operations.
        """
        pi = tm.Pi()

        # Test SymPy expression access
        sympy_expr = pi.sympy_expr
        self.assertEqual(sympy_expr, sp.pi)

        # Test SymPy operations
        self.assertTrue(sympy_expr.is_real)
        self.assertTrue(sympy_expr.is_positive)
        self.assertFalse(sympy_expr.is_integer)
        self.assertFalse(sympy_expr.is_rational)

        # Test numerical evaluation consistency
        pi_float = float(sympy_expr)
        self.assertEqual(pi_float, pi.eval())
        self.assertEqual(pi_float, math.pi)


if __name__ == "__main__":
    unittest.main()
