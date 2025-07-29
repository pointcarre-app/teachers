"""
Test suite for MathsCollection sympy integration and sympy_expr_data functionality.

This module contains comprehensive tests for:
- MathsCollection sympy_expr field and its computation
- sympy_expr_data property and serialization
- Integration with sympy operations and conversions
- Compatibility with existing MathsObject functionality
- Edge cases and error handling

These tests ensure that MathsCollection properly integrates with the sympy
ecosystem and maintains consistency with other MathsObject classes.
"""

import unittest
import sympy as sp

import teachers.maths as tm
from pydantic import ValidationError


class TestMathsCollectionSympy(unittest.TestCase):
    """Test suite for MathsCollection sympy integration functionality."""

    def test_sympy_expr_creation(self):
        """
        Test that MathsCollection properly creates sympy_expr as sp.Tuple.

        Validates:
        - sympy_expr is automatically computed during creation
        - sympy_expr contains correct tuple structure
        - Individual elements maintain their sympy expressions
        - Empty collections are handled correctly
        """
        # Test with basic mathematical objects
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Integer(n=42)

        coll = tm.MathsCollection(elements=[x, y, z])

        # Check that sympy_expr is created
        self.assertIsInstance(coll.sympy_expr, sp.Tuple)

        # Check that sympy_expr contains the correct elements
        expected_sympy = sp.Tuple(x.sympy_expr, y.sympy_expr, z.sympy_expr)
        self.assertEqual(coll.sympy_expr, expected_sympy)

        # Check individual elements are preserved
        self.assertEqual(str(coll.sympy_expr.args[0]), "x")
        self.assertEqual(str(coll.sympy_expr.args[1]), "y")
        self.assertEqual(str(coll.sympy_expr.args[2]), "42")

    def test_sympy_expr_with_complex_objects(self):
        """
        Test sympy_expr creation with complex mathematical objects.

        Validates:
        - Collections containing fractions, additions, multiplications
        - Nested mathematical expressions
        - Function images and other complex types
        """
        # Create complex mathematical objects
        a = tm.Add(l=tm.Integer(n=1), r=tm.Integer(n=2))
        f = tm.Fraction(p=3, q=4)
        m = tm.Mul(l=tm.Integer(n=5), r=tm.Symbol(s="x"))

        coll = tm.MathsCollection(elements=[a, f, m])

        # Check sympy_expr structure
        self.assertIsInstance(coll.sympy_expr, sp.Tuple)
        self.assertEqual(len(coll.sympy_expr.args), 3)

        # Verify each element's sympy representation
        self.assertEqual(str(coll.sympy_expr.args[0]), "1 + 2")
        self.assertEqual(str(coll.sympy_expr.args[1]), "3/4")
        self.assertEqual(str(coll.sympy_expr.args[2]), "5*x")

    def test_sympy_expr_data_property(self):
        """
        Test the sympy_expr_data property for JSON serialization.

        Validates:
        - sympy_expr_data returns proper dictionary structure
        - Dictionary contains type, sp.srepr, and str fields
        - Data is JSON-serializable
        - Consistent with MathsObject serialization format
        """
        x = tm.Symbol(s="x")
        y = tm.Integer(n=10)

        coll = tm.MathsCollection(elements=[x, y])

        # Test sympy_expr_data property exists
        self.assertTrue(hasattr(coll, "sympy_expr_data"))

        # Get the serialized data
        expr_data = coll.sympy_expr_data

        # Check structure
        self.assertIsInstance(expr_data, dict)
        self.assertIn("type", expr_data)
        self.assertIn("sp.srepr", expr_data)
        self.assertIn("str", expr_data)

        # Check values
        self.assertEqual(expr_data["type"], "Tuple")
        self.assertIn("Tuple", expr_data["sp.srepr"])
        self.assertIn("(x, 10)", expr_data["str"])

    def test_field_serializer(self):
        """
        Test the field serializer for sympy_expr.

        Validates:
        - serialize_sympy_expr_data method works correctly
        - Serialization is consistent across different sympy expressions
        - Method can handle various sympy types
        """
        # Test with different collections
        collections = [
            tm.MathsCollection(elements=[tm.Integer(n=1)]),
            tm.MathsCollection(elements=[tm.Symbol(s="a"), tm.Symbol(s="b")]),
            tm.MathsCollection(
                elements=[tm.Fraction(p=1, q=2), tm.Add(l=tm.Integer(n=3), r=tm.Integer(n=4))]
            ),
        ]

        for coll in collections:
            # Test direct method call
            serialized = coll.serialize_sympy_expr_data(coll.sympy_expr)

            self.assertIsInstance(serialized, dict)
            self.assertIn("type", serialized)
            self.assertIn("sp.srepr", serialized)
            self.assertIn("str", serialized)

            # Ensure it matches property result
            self.assertEqual(serialized, coll.sympy_expr_data)

    def test_empty_collection(self):
        """
        Test MathsCollection with empty elements list.

        Validates:
        - Empty collections can be created
        - sympy_expr is created as empty tuple
        - sympy_expr_data works with empty collections
        """
        coll = tm.MathsCollection(elements=[])

        # Check sympy_expr is empty tuple
        self.assertIsInstance(coll.sympy_expr, sp.Tuple)
        self.assertEqual(len(coll.sympy_expr.args), 0)
        self.assertEqual(coll.sympy_expr, sp.Tuple())

        # Check sympy_expr_data works
        expr_data = coll.sympy_expr_data
        self.assertIsInstance(expr_data, dict)
        self.assertEqual(expr_data["type"], "Tuple")
        self.assertEqual(expr_data["str"], "()")

    def test_single_element_collection(self):
        """
        Test MathsCollection with single element.

        Validates:
        - Single element collections work correctly
        - sympy_expr maintains tuple structure even with one element
        - Consistency with multi-element collections
        """
        x = tm.Symbol(s="variable")
        coll = tm.MathsCollection(elements=[x])

        # Check structure
        self.assertIsInstance(coll.sympy_expr, sp.Tuple)
        self.assertEqual(len(coll.sympy_expr.args), 1)
        self.assertEqual(coll.sympy_expr.args[0], x.sympy_expr)

        # Check serialization
        expr_data = coll.sympy_expr_data
        self.assertEqual(expr_data["type"], "Tuple")
        self.assertIn("variable", expr_data["str"])

    def test_consistency_with_function_usage(self):
        """
        Test that sympy_expr integration doesn't break Function usage.

        Validates:
        - Function calls with MathsCollection still work
        - Image objects are created correctly
        - sympy expressions are properly handled in function context
        """
        # Create function and collection
        f = tm.Function(name="g")
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        coll = tm.MathsCollection(elements=[x, y])

        # Create function image
        img = f(coll)

        # Verify Image creation
        self.assertIsInstance(img, tm.Image)
        self.assertEqual(img.f, f)
        self.assertEqual(img.pre, coll)

        # Verify sympy expression
        self.assertEqual(str(img.sympy_expr), "g(x, y)")

        # Test that collection's sympy_expr_data is accessible
        coll_data = coll.sympy_expr_data
        self.assertIsInstance(coll_data, dict)

    def test_simplified_preserves_sympy_expr(self):
        """
        Test that simplified() method preserves sympy_expr functionality.

        Validates:
        - Simplified collections maintain sympy_expr
        - sympy_expr_data works on simplified collections
        - Element simplification is reflected in collection's sympy_expr
        """
        # Create collection with simplifiable elements
        a = tm.Add(l=tm.Integer(n=2), r=tm.Integer(n=3))  # Should simplify to 5
        b = tm.Fraction(p=4, q=2)  # Should simplify to 2

        coll = tm.MathsCollection(elements=[a, b])
        simplified_coll = coll.simplified()

        # Check that simplified collection has sympy_expr
        self.assertIsInstance(simplified_coll.sympy_expr, sp.Tuple)

        # Check that elements are simplified in sympy_expr
        self.assertEqual(str(simplified_coll.sympy_expr.args[0]), "5")
        self.assertEqual(str(simplified_coll.sympy_expr.args[1]), "2")

        # Check sympy_expr_data works
        expr_data = simplified_coll.sympy_expr_data
        self.assertIsInstance(expr_data, dict)
        self.assertIn("(5, 2)", expr_data["str"])

    def test_latex_compatibility(self):
        """
        Test that latex() method still works with sympy integration.

        Validates:
        - latex() method produces correct output
        - sympy integration doesn't interfere with latex generation
        - Complex mathematical expressions render correctly
        """
        # Create collection with various types
        x = tm.Symbol(s="x")
        f = tm.Fraction(p=1, q=2)
        p = tm.Pow(base=tm.Symbol(s="y"), exp=tm.Integer(n=2))

        coll = tm.MathsCollection(elements=[x, f, p])

        # Test latex generation
        latex_output = coll.latex()

        # Check structure (should be \left(...\right))
        self.assertTrue(latex_output.startswith("\\left("))
        self.assertTrue(latex_output.endswith("\\right)"))
        self.assertIn("x", latex_output)
        self.assertIn("\\dfrac{1}{2}", latex_output)
        self.assertIn("y^{2}", latex_output)

    def test_repr_str_consistency(self):
        """
        Test that __repr__ and __str__ still work correctly.

        Validates:
        - String representations are unchanged
        - sympy integration doesn't affect display methods
        - Consistency with original MathsCollection behavior
        """
        x = tm.Symbol(s="alpha")
        n = tm.Integer(n=42)

        coll = tm.MathsCollection(elements=[x, n])

        # Test repr
        repr_str = repr(coll)
        expected_repr = "(Symbol(s='alpha'), Integer(n=42))"
        self.assertEqual(repr_str, expected_repr)

        # Test str (should be same as repr)
        str_str = str(coll)
        self.assertEqual(str_str, repr_str)

    def test_model_validation(self):
        """
        Test that model validation works correctly with sympy integration.

        Validates:
        - Invalid inputs are properly rejected
        - ValidationError is raised appropriately
        - sympy_expr computation doesn't interfere with validation
        """
        # Test with valid input
        valid_coll = tm.MathsCollection(elements=[tm.Integer(n=1), tm.Symbol(s="x")])
        self.assertIsInstance(valid_coll.sympy_expr, sp.Tuple)

        # Test with invalid input (non-MathsObject elements)
        with self.assertRaises((ValidationError, TypeError)):
            tm.MathsCollection(elements=[1, 2, 3])  # Plain integers, not MathsObjects

        with self.assertRaises((ValidationError, TypeError)):
            tm.MathsCollection(elements=["not", "math", "objects"])

    def test_getitem_access(self):
        """
        Test that element access via [] operator still works.

        Validates:
        - __getitem__ method functionality is preserved
        - Individual elements can be accessed correctly
        - sympy integration doesn't affect indexing
        """
        elements = [tm.Symbol(s="first"), tm.Integer(n=100), tm.Fraction(p=3, q=7)]

        coll = tm.MathsCollection(elements=elements)

        # Test individual access
        self.assertEqual(coll[0], elements[0])
        self.assertEqual(coll[1], elements[1])
        self.assertEqual(coll[2], elements[2])

        # Verify sympy_expr is still accessible
        self.assertIsInstance(coll.sympy_expr, sp.Tuple)


if __name__ == "__main__":
    unittest.main()
