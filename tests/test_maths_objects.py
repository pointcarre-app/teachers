"""
Test suite for the core MathsObject classes and their functionality.

This module contains comprehensive tests for:
- Atomic mathematical objects (Integer, Symbol, Function, Decimal, Image, Inf)
- Binary operators (Add, Mul, Fraction, Pow)
- Relations (Equality, StrictGreaterThan)
- Collections (MathsCollection)
- Operator overloads and mathematical operations
- Object creation, validation, and simplification
- Liskov substitution principle compliance

The tests ensure that mathematical objects can be created, manipulated,
and simplified correctly according to mathematical rules.
"""

import unittest

import teachers.maths as tm

from pydantic import ValidationError


class TestMathsObject(unittest.TestCase):
    """Test suite for MathsObject base class and all derived mathematical objects."""

    def test_liskov_substitution_principle(self):
        """
        Test that all MathsObject subclasses properly inherit field types.

        Validates the Liskov Substitution Principle by ensuring that:
        - All subclasses have compatible field types with their parent
        - The sympy_expr field maintains proper type hierarchy
        - No subclass breaks the contract established by the parent class

        This is crucial for ensuring polymorphic behavior works correctly.
        """

        # TODO: this can be largely improved

        # Get all classes defined in the teachers package
        clss = [cls for cls in vars(tm).values() if isinstance(cls, type)]

        for cls in clss:
            if not issubclass(cls, tm.MathsObject):
                continue
            if cls is tm.MathsObject:
                continue

            parent_cls = cls.__base__

            for field_name, field_info in cls.model_fields.items():
                if field_name != "sympy_expr":
                    continue

                self.assertTrue(
                    issubclass(
                        field_info.annotation, parent_cls.model_fields[field_name].annotation
                    ),
                    f"""
{cls.__name__}.{field_name} is of type {field_info.annotation} which does not inherit from {parent_cls.model_fields[field_name].annotation}
""",
                )

    def test_creation_atoms(self):
        """
        Test the creation and validation of atomic mathematical expressions.

        Covers:
        - Integer: Valid/invalid creation, type validation
        - Symbol: String validation, empty string handling
        - Function: Name validation, function calling syntax
        - Decimal: Multiple creation modes (p/q vs x), validation
        - Image: Function application with various argument types

        Validates both successful creation and proper error handling
        for invalid inputs.
        """
        # Test creation of Integer
        i = tm.Integer(n=5)
        self.assertEqual(i.n, 5)

        # # Test invalid Integer creation
        # with self.assertRaises(ValidationError):
        #     tm.Integer(n=-1)

        # Test invalid Integer creation
        with self.assertRaises(ValidationError):
            tm.Integer(n=4.5)

        with self.assertRaises(ValidationError):
            tm.Integer(n="not a number")

        # Test creation of Symbol
        s = tm.Symbol(s="x")
        self.assertEqual(s.s, "x")
        self.assertEqual(str(s.sympy_expr), "x")

        # Test creation of Function
        f = tm.Function(name="f")
        self.assertEqual(f.name, "f")
        self.assertEqual(str(f.sympy_expr), "f")

        # Test calling a function with arguments
        x = tm.Symbol(s="x")
        fx = f(x)
        self.assertIsInstance(fx, tm.Image)
        self.assertEqual(str(fx.sympy_expr), "f(x)")

        # Test invalid Symbol creation
        with self.assertRaises(TypeError):
            tm.Symbol(s=123)  # Symbol name should be a string

        with self.assertRaises(ValidationError):
            tm.Symbol(s="")  # Empty string not allowed

        # Test invalid Function creation
        with self.assertRaises(TypeError):
            tm.Function(name=123)  # Function name should be a string

        with self.assertRaises(ValidationError):
            tm.Function(name="")  # Empty string not allowed

        # Test creation of Decimal with p and q
        d1 = tm.Decimal(p=5, q=2)

        # Test creation of Decimal with x
        d2 = tm.Decimal(x=3.75)

        # Test invalid Decimal creation
        with self.assertRaises(ValueError):
            tm.Decimal()  # Missing both p/q and x

        with self.assertRaises(ValueError):
            tm.Decimal(p=1, q=2, x=0.5)  # Providing both p/q and x

        # Test Image class creation
        # With a single argument
        img1 = f(x)
        self.assertEqual(img1.f, f)
        self.assertEqual(img1.pre, x)

        # With multiple arguments (collection)
        y = tm.Symbol(s="y")
        img2 = f(tm.MathsCollection(elements=[x, y]))
        self.assertIsInstance(img2, tm.Image)
        self.assertEqual(str(img2.sympy_expr), "f(x, y)")

        # With an Integer argument
        n = tm.Integer(n=42)
        img3 = f(n)
        self.assertIsInstance(img3, tm.Image)
        self.assertEqual(img3.pre, n)
        self.assertEqual(str(img3.sympy_expr), "f(42)")

    def test_neg(self):
        """
        Test the negation operator (__neg__) for various mathematical objects.

        Validates:
        - Integer negation: positive ↔ negative conversion
        - Special handling of -1 and 1
        - Proper creation of Mul objects for complex negations

        Ensures that mathematical negation follows expected rules.
        """
        a = tm.Integer(n=13)
        self.assertEqual(-a, tm.Integer(n=-13))

        a = tm.Integer(n=1)
        self.assertEqual(-a, tm.Integer(n=-1))

        a = tm.Integer(n=-1)
        self.assertEqual(-a, tm.Integer(n=1))

    def test_simplification_atoms(self):
        """
        Test simplification behavior for atomic mathematical objects.

        Validates that:
        - Atomic objects (Integer, Symbol) remain unchanged when simplified
        - Negative integers maintain their value during simplification
        - Symbol negation creates proper Mul(-1, Symbol) structures
        - Double negation returns to original form

        Ensures basic mathematical identities are preserved.
        """
        a = tm.Integer(n=13)
        self.assertEqual(a.simplified(), a)

        a = tm.Integer(n=1)
        self.assertEqual(a.simplified(), a)

        a = tm.Integer(n=-1)
        self.assertEqual(a.simplified(), a)

        a = tm.Integer(n=-100)
        # self.assertEqual(a.simplified, tm.Mul(l=tm.Integer(n=-1), r=tm.Integer(n=100)))
        self.assertEqual(a.simplified(), tm.Integer(n=-100))
        self.assertEqual(-a.simplified(), tm.Integer(n=100))

        a = tm.Symbol(s="a")
        self.assertEqual(a.simplified(), a)
        self.assertEqual(-a.simplified(), tm.Mul(l=tm.Integer(n=-1), r=tm.Symbol(s="a")))
        self.assertEqual(-(-a.simplified()), tm.Symbol(s="a"))

    def test_simplification_addition(self):
        """
        Test simplification rules for addition operations.

        Validates:
        - Integer + Integer → Integer (arithmetic)
        - Proper handling of algebraic simplification rules

        Currently tests basic integer addition.
        TODO: Expand to cover more complex addition scenarios.
        """
        # Test simplification of Integer + Integer
        a = tm.Add(l=tm.Integer(n=3), r=tm.Integer(n=4))
        self.assertEqual(a.simplified(), tm.Integer(n=7))

    def test_simplification_fraction(self):
        """
        Test fraction simplification and reduction rules.

        Validates:
        - Fractions with denominator 1 → Integer
        - GCD reduction (10/5 → 2)
        - Negative fraction handling (sign normalization)
        - Various combinations of positive/negative numerator/denominator

        Ensures fractions are always in their simplest form.
        """
        # Test with denominator 1
        f = tm.Fraction(p=7, q=1)
        self.assertEqual(f.simplified(), tm.Integer(n=7))

        # Test simplification of a fraction
        f = tm.Fraction(p=10, q=5)
        self.assertEqual(f.simplified(), tm.Integer(n=2))

        # Test negative fractions
        f = tm.Fraction(p=-6, q=9)
        self.assertEqual(f.simplified(), tm.Fraction(p=-2, q=3))

        # Test negative fractions
        f = tm.Fraction(p=6, q=-9)
        self.assertEqual(f.simplified(), tm.Fraction(p=-2, q=3))

        # Test negative fractions
        f = tm.Fraction(p=-6, q=-9)
        self.assertEqual(f.simplified(), tm.Fraction(p=2, q=3))

        # Test double negative fractions
        f = tm.Fraction(p=-10, q=-5)
        self.assertEqual(f.simplified(), tm.Integer(n=2))

    def test_basic_operations(self):
        """
        Test all operator overloads and their mathematical correctness.

        Comprehensive test covering:
        - Addition (+): Integer, Symbol, Fraction combinations
        - Subtraction (-): Implemented as Add(l, -r)
        - Multiplication (*): Various type combinations
        - Division (/): Creates Fraction objects
        - Exponentiation (**): Creates Pow objects
        - Comparisons (>, <): Creates relation objects
        - Negation (-): Unary minus operator
        - Complex nested expressions
        - Mixed type operations

        Validates that Python operators create the correct mathematical
        object representations.
        """

        # Setup some basic objects
        a = tm.Integer(n=5)
        b = tm.Integer(n=3)
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        f1 = tm.Fraction(p=1, q=2)
        f2 = tm.Fraction(p=2, q=3)

        # Test addition
        add1 = a + b
        self.assertIsInstance(add1, tm.Add)
        self.assertEqual(add1.simplified(), tm.Integer(n=8))

        add2 = a + x
        self.assertIsInstance(add2, tm.Add)
        self.assertEqual(add2.l, a)
        self.assertEqual(add2.r, x)

        add3 = f1 + f2
        self.assertIsInstance(add3, tm.Add)
        self.assertEqual(add3.simplified(), tm.Fraction(p=7, q=6))

        # Test subtraction
        sub1 = a - b
        self.assertIsInstance(sub1, tm.Add)  # Subtraction is implemented as Add(l, -r)
        self.assertEqual(sub1.simplified(), tm.Integer(n=2))

        sub2 = x - y
        self.assertIsInstance(sub2, tm.Add)
        self.assertEqual(sub2.l, x)
        self.assertEqual(sub2.r, tm.Mul(l=tm.Integer(n=-1), r=y))

        # Test multiplication
        mul1 = a * b
        self.assertIsInstance(mul1, tm.Mul)
        self.assertEqual(mul1.simplified(), tm.Integer(n=15))

        mul2 = a * x
        self.assertIsInstance(mul2, tm.Mul)
        self.assertEqual(mul2.l, a)
        self.assertEqual(mul2.r, x)

        mul3 = f1 * f2
        self.assertIsInstance(mul3, tm.Mul)
        self.assertEqual(mul3.simplified(), tm.Fraction(p=1, q=3))

        # Test division (creating fractions)
        div1 = a / b
        self.assertIsInstance(div1, tm.Fraction)
        self.assertEqual(div1.simplified(), tm.Fraction(p=5, q=3))

        div2 = x / y
        self.assertIsInstance(div2, tm.Fraction)
        self.assertEqual(div2.p, x)
        self.assertEqual(div2.q, y)

        # Test power
        pow1 = a**b
        self.assertIsInstance(pow1, tm.Pow)
        self.assertEqual(pow1.simplified(), tm.Integer(n=125))

        pow2 = x**b
        self.assertIsInstance(pow2, tm.Pow)
        self.assertEqual(pow2.base, x)
        self.assertEqual(pow2.exp, b)

        # Test comparison operators
        gt1 = a > b
        self.assertIsInstance(gt1, tm.StrictGreaterThan)
        self.assertEqual(gt1.l, a)
        self.assertEqual(gt1.r, b)

        lt1 = a < b
        self.assertIsInstance(lt1, tm.StrictGreaterThan)
        self.assertEqual(lt1.l, b)
        self.assertEqual(lt1.r, a)

        # Test negation
        neg1 = -a
        self.assertIsInstance(neg1, tm.Integer)
        self.assertEqual(neg1.n, -5)

        neg2 = -x
        self.assertIsInstance(neg2, tm.Mul)
        self.assertEqual(neg2.l, tm.Integer(n=-1))
        self.assertEqual(neg2.r, x)

        # Test complex expressions
        expr1 = a + b * x
        self.assertIsInstance(expr1, tm.Add)
        self.assertEqual(expr1.l, a)
        self.assertIsInstance(expr1.r, tm.Mul)

        expr2 = (a + b) * x
        self.assertIsInstance(expr2, tm.Mul)
        self.assertIsInstance(expr2.l, tm.Add)
        self.assertEqual(expr2.r, x)

        # Test with Decimal
        d = tm.Decimal(x=2.5)
        expr3 = a + d
        self.assertIsInstance(expr3, tm.Add)
        self.assertEqual(expr3.l, a)
        self.assertEqual(expr3.r, d)

        # Test with functions and images
        f = tm.Function(name="f")
        fx = f(x)
        expr4 = a + fx
        self.assertIsInstance(expr4, tm.Add)
        self.assertEqual(expr4.l, a)
        self.assertEqual(expr4.r, fx)

    def test_maths_collection(self):
        """
        Test MathsCollection container functionality.

        Validates:
        - Element storage and retrieval (__getitem__)
        - String representation (__repr__, __str__)
        - Simplification propagation to all elements
        - Integration with Function calls (multi-argument functions)

        Ensures collections properly manage multiple mathematical objects.
        """
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # Test creation
        coll = tm.MathsCollection(elements=[x, y, z])

        # Test __getitem__
        self.assertEqual(coll[0], x)
        self.assertEqual(coll[1], y)
        self.assertEqual(coll[2], z)

        # Test __repr__ and __str__
        self.assertEqual(repr(coll), "(Symbol(s='x'), Symbol(s='y'), Symbol(s='z'))")
        self.assertEqual(str(coll), "(Symbol(s='x'), Symbol(s='y'), Symbol(s='z'))")

        # Test simplified
        simplified_coll = coll.simplified()
        self.assertIsInstance(simplified_coll, tm.MathsCollection)
        self.assertEqual(len(simplified_coll.elements), 3)

        # Test with Function
        f = tm.Function(name="f")
        f_xyz = f(coll)
        self.assertIsInstance(f_xyz, tm.Image)
        self.assertEqual(f_xyz.f, f)
        self.assertEqual(f_xyz.pre, coll)

    def test_fraction_properties(self):
        """
        Test Fraction class additional properties and conversions.

        Validates:
        - as_decimal property: Fraction → Decimal conversion
        - as_percent property: Fraction → percentage (Integer or Decimal)
        - Proper handling of integer vs non-integer percentages

        Ensures fractions can be converted to different representations
        for display and calculation purposes.
        """
        f = tm.Fraction(p=3, q=4)

        # Test as_decimal property
        decimal = f.as_decimal
        self.assertIsInstance(decimal, tm.Decimal)
        self.assertEqual(decimal.eval(), 0.75)

        # Test as_percent property
        percent = f.as_percent
        self.assertIsInstance(percent, tm.Integer)
        self.assertEqual(percent.n, 75)

        # Test with non-integer percentage
        f2 = tm.Fraction(p=1, q=3)
        percent2 = f2.as_percent
        self.assertIsInstance(percent2, tm.Decimal)

    def test_relations(self):
        """
        Test relational operators and mathematical comparisons.

        Validates:
        - Equality: Direct creation and simplification
        - StrictGreaterThan: Direct creation and operator syntax
        - Operator overload behavior (>, <)
        - Simplification of relations with complex expressions
        - Proper handling of symbolic vs numeric comparisons

        Ensures mathematical relations are correctly represented
        and can be manipulated algebraically.
        """

        # Create basic objects for testing
        a = tm.Integer(n=5)
        b = tm.Integer(n=3)
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # ========== Test Equality ==========

        # Test direct creation of Equality
        eq1 = tm.Equality(l=a, r=b)
        self.assertIsInstance(eq1, tm.Equality)
        self.assertEqual(eq1.l, a)
        self.assertEqual(eq1.r, b)

        # Test with symbols
        eq2 = tm.Equality(l=x, r=y)
        self.assertIsInstance(eq2, tm.Equality)
        self.assertEqual(eq2.l, x)
        self.assertEqual(eq2.r, y)

        # Test simplified method
        eq_complex = tm.Equality(l=tm.Add(l=a, r=b), r=tm.Integer(n=8))
        eq_simplified = eq_complex.simplified()
        self.assertIsInstance(eq_simplified, tm.Equality)
        self.assertEqual(eq_simplified.l, tm.Integer(n=8))
        self.assertEqual(eq_simplified.r, tm.Integer(n=8))

        # Test with complex expressions
        eq3 = tm.Equality(l=tm.Add(l=x, r=y), r=tm.Integer(n=10))

        # ========== Test StrictGreaterThan ==========

        # Create StrictGreaterThan directly (avoid using > operator for now)
        gt1 = tm.StrictGreaterThan(l=a, r=b)
        self.assertIsInstance(gt1, tm.StrictGreaterThan)
        self.assertEqual(gt1.l, a)
        self.assertEqual(gt1.r, b)

        # Test with symbols
        gt2 = tm.StrictGreaterThan(l=x, r=y)
        self.assertIsInstance(gt2, tm.StrictGreaterThan)
        self.assertEqual(gt2.l, x)
        self.assertEqual(gt2.r, y)

        # Test simplified method
        gt_complex = tm.StrictGreaterThan(l=tm.Add(l=a, r=b), r=tm.Integer(n=7))
        gt_simplified = gt_complex.simplified()
        self.assertIsInstance(gt_simplified, tm.StrictGreaterThan)
        self.assertEqual(gt_simplified.l, tm.Integer(n=8))
        self.assertEqual(gt_simplified.r, tm.Integer(n=7))

        # Test with complex expressions
        gt3 = tm.StrictGreaterThan(l=tm.Add(l=x, r=y), r=tm.Integer(n=10))

        # Now test the operator syntax
        gt_op1 = a > b  # This should work now
        self.assertIsInstance(gt_op1, tm.StrictGreaterThan)
        self.assertEqual(gt_op1.l, a)
        self.assertEqual(gt_op1.r, b)

        lt_op1 = a < b  # This should work now
        self.assertIsInstance(lt_op1, tm.StrictGreaterThan)
        self.assertEqual(lt_op1.l, b)
        self.assertEqual(lt_op1.r, a)


if __name__ == "__main__":
    unittest.main()
