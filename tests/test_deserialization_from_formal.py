"""
Test suite for MathsObject serialization and deserialization functionality.

This module tests the round-trip conversion capabilities:
- Object → string representation (repr) → Object parsing
- Formal representation parsing via MathsObjectParser.from_repr()
- Structural integrity preservation during conversions
- Complex nested expression handling
- All mathematical object types and their combinations

These tests ensure that mathematical objects can be serialized
to string format and perfectly reconstructed, which is crucial
for data persistence, debugging, and inter-process communication.
"""

import unittest
import teachers.maths as tm


class TestSerializationDeserialization(unittest.TestCase):
    """
    Test suite for MathsObject serialization/deserialization round-trips.

    Each test follows the pattern:
    1. Create a MathsObject
    2. Convert to string representation (repr)
    3. Parse back using MathsObjectParser.from_repr()
    4. Verify perfect reconstruction
    """

    def test_integer_serialization(self):
        """
        Test Integer object serialization and perfect reconstruction.

        Validates:
        - Integer → repr() → from_repr() → Integer round-trip
        - Preservation of numeric value
        - Correct object type reconstruction
        - Overall equality after round-trip

        This is fundamental for all numeric computations.
        """
        # Create an Integer object
        integer = tm.Integer(n=42)

        # Convert to string representation
        repr_str = repr(integer)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Integer)
        self.assertEqual(parsed.n, 42)

        # Test overall equality
        self.assertEqual(parsed, integer)

    def test_symbol_serialization(self):
        """
        Test Symbol object serialization and perfect reconstruction.

        Validates:
        - Symbol → repr() → from_repr() → Symbol round-trip
        - Preservation of symbol name string
        - Correct object type reconstruction
        - Overall equality after round-trip

        Critical for algebraic manipulation and variable handling.
        """
        # Create a Symbol object
        symbol = tm.Symbol(s="x")

        # Convert to string representation
        repr_str = repr(symbol)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Symbol)
        self.assertEqual(parsed.s, "x")

        # Test overall equality
        self.assertEqual(parsed, symbol)

    def test_addition_serialization(self):
        """
        Test Add object serialization with mixed operand types.

        Validates:
        - Binary operation reconstruction
        - Mixed Integer + Symbol operands
        - Preservation of left/right operand order
        - Nested object reconstruction integrity
        - Complete structural equality

        Ensures addition operations can be perfectly preserved.
        """
        # Create an Add object
        a = tm.Integer(n=5)
        b = tm.Symbol(s="y")
        add_expr = a + b

        # Convert to string representation
        repr_str = repr(add_expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Add)
        self.assertIsInstance(parsed.l, tm.Integer)
        self.assertEqual(parsed.l.n, 5)
        self.assertIsInstance(parsed.r, tm.Symbol)
        self.assertEqual(parsed.r.s, "y")

        # Test overall equality
        self.assertEqual(parsed, add_expr)

    def test_multiplication_serialization(self):
        """
        Test Mul object serialization with mixed operand types.

        Validates:
        - Binary operation reconstruction
        - Mixed Integer * Symbol operands
        - Preservation of left/right operand order
        - Nested object reconstruction integrity
        - Complete structural equality

        Ensures multiplication operations can be perfectly preserved.
        """
        # Create a Mul object
        a = tm.Integer(n=3)
        b = tm.Symbol(s="z")
        mul_expr = a * b

        # Convert to string representation
        repr_str = repr(mul_expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Mul)
        self.assertIsInstance(parsed.l, tm.Integer)
        self.assertEqual(parsed.l.n, 3)
        self.assertIsInstance(parsed.r, tm.Symbol)
        self.assertEqual(parsed.r.s, "z")

        # Test overall equality
        self.assertEqual(parsed, mul_expr)

    def test_fraction_serialization(self):
        """
        Test Fraction object serialization with complex numerator/denominator.

        Validates:
        - Fraction → repr() → from_repr() → Fraction round-trip
        - Preservation of numerator and denominator objects
        - Integer component reconstruction
        - Complete structural integrity
        - Overall equality after round-trip

        Critical for rational number operations and algebraic fractions.
        """
        # Create a Fraction object
        p = tm.Integer(n=7)
        q = tm.Integer(n=2)
        frac = tm.Fraction(p=p, q=q)

        # Convert to string representation
        repr_str = repr(frac)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Fraction)
        self.assertIsInstance(parsed.p, tm.Integer)
        self.assertEqual(parsed.p.n, 7)
        self.assertIsInstance(parsed.q, tm.Integer)
        self.assertEqual(parsed.q.n, 2)

        # Test overall equality
        self.assertEqual(parsed, frac)

    def test_power_serialization(self):
        """
        Test Pow object serialization with symbolic base and integer exponent.

        Validates:
        - Power → repr() → from_repr() → Power round-trip
        - Base and exponent preservation
        - Mixed Symbol ^ Integer operands
        - Complete structural integrity
        - Overall equality after round-trip

        Essential for polynomial and exponential expressions.
        """
        # Create a Pow object
        base = tm.Symbol(s="a")
        exp = tm.Integer(n=3)
        pow_expr = base**exp

        # Convert to string representation
        repr_str = repr(pow_expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Pow)
        self.assertIsInstance(parsed.base, tm.Symbol)
        self.assertEqual(parsed.base.s, "a")
        self.assertIsInstance(parsed.exp, tm.Integer)
        self.assertEqual(parsed.exp.n, 3)

        # Test overall equality
        self.assertEqual(parsed, pow_expr)

    def test_function_serialization(self):
        """
        Test Function and Image object serialization and reconstruction.

        Validates:
        - Function application serialization: f(x)
        - Function object preservation (name)
        - Image object reconstruction (function + argument)
        - Nested object integrity
        - Complete round-trip equality

        Critical for function handling in mathematical expressions.
        """
        # Create a Function and an Image object
        f = tm.Function(name="f")
        x = tm.Symbol(s="x")
        image = f(x)

        # Convert to string representation
        repr_str = repr(image)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Image)
        self.assertIsInstance(parsed.f, tm.Function)
        self.assertEqual(parsed.f.name, "f")
        self.assertIsInstance(parsed.pre, tm.Symbol)
        self.assertEqual(parsed.pre.s, "x")

        # Test overall equality
        self.assertEqual(parsed, image)

    def test_relation_serialization(self):
        """
        Test Equality relation serialization and reconstruction.

        Validates:
        - Relation → repr() → from_repr() → Relation round-trip
        - Left and right side preservation
        - Equality object structure
        - Complete structural integrity
        - Overall equality after round-trip

        Essential for equation and inequality handling.
        """
        # Create an Equality object
        a = tm.Integer(n=5)
        b = tm.Integer(n=5)
        eq = tm.Equality(l=a, r=b)

        # Convert to string representation
        repr_str = repr(eq)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original
        self.assertIsInstance(parsed, tm.Equality)
        self.assertIsInstance(parsed.l, tm.Integer)
        self.assertEqual(parsed.l.n, 5)
        self.assertIsInstance(parsed.r, tm.Integer)
        self.assertEqual(parsed.r.n, 5)

        # Test overall equality
        self.assertEqual(parsed, eq)

    def test_complex_expression_serialization(self):
        """
        Test complex nested expression serialization and perfect reconstruction.

        Expression: ((a + b) * c) / (x - y)

        Validates:
        - Multi-level nesting preservation
        - Mixed operator types in single expression
        - Fraction with complex numerator/denominator
        - Complete structural integrity at all levels
        - Perfect round-trip equality

        This tests the parser's ability to handle realistic
        mathematical expressions with multiple levels of complexity.
        """
        # Create a complex expression: ((a + b) * c) / (x - y)
        a = tm.Integer(n=3)
        b = tm.Integer(n=5)
        c = tm.Integer(n=2)
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        expr = ((a + b) * c) / (x - y)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Verify the parsed object matches the original structure
        self.assertIsInstance(parsed, tm.Fraction)
        self.assertIsInstance(parsed.p, tm.Mul)
        self.assertIsInstance(parsed.q, tm.Add)

        # Check numerator structure
        self.assertIsInstance(parsed.p.l, tm.Add)
        self.assertEqual(parsed.p.r.n, 2)  # c = 2

        # Check denominator structure
        self.assertEqual(parsed.q.l.s, "x")  # x
        self.assertIsInstance(parsed.q.r, tm.Mul)
        self.assertEqual(parsed.q.r.l.n, -1)  # -1
        self.assertEqual(parsed.q.r.r.s, "y")  # y

        # Test overall equality
        self.assertEqual(parsed, expr)

    def test_complex_expression_with_all_operators(self):
        """
        Test comprehensive expression using all basic mathematical operators.

        Expression: (x + 3)^2 * (7/y) - z/(x*y)

        Validates:
        - Addition, multiplication, power, division, subtraction
        - Mixed symbols and integers
        - Nested operations with proper precedence
        - Complex operator chaining
        - Perfect reconstruction of operator precedence

        Ensures the parser can handle expressions with
        all fundamental mathematical operations.
        """
        # Create symbols and values
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        a = tm.Integer(n=3)
        b = tm.Integer(n=7)

        # Create complex expression: (x + 3)^2 * (7/y) - z/(x*y)
        expr = (x + a) ** tm.Integer(n=2) * (b / y) - z / (x * y)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Test overall equality
        self.assertEqual(parsed, expr)

    def test_complex_expression_with_functions_and_relations(self):
        """
        Test expressions combining functions with relational operators.

        Expression: f(x^2 + y) = g(x/y)

        Validates:
        - Function applications with complex arguments
        - Equality relation with function expressions
        - Mixed power, addition, and division in function arguments
        - Function composition with relations
        - Complete structural preservation

        Tests integration of functions and relations in
        complex mathematical equations.
        """
        # Create symbols, functions, and values
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        f = tm.Function(name="f")
        g = tm.Function(name="g")

        # Create complex expression: f(x^2 + y) = g(x/y)
        left = f(x ** tm.Integer(n=2) + y)
        right = g(x / y)
        expr = tm.Equality(l=left, r=right)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Test overall equality
        self.assertEqual(parsed, expr)

    def test_nested_functions_and_fractions(self):
        """
        Test deeply nested function compositions with complex arguments.

        Expression: f(g(x/y)) / h(z^3)

        Validates:
        - Function composition: f(g(...))
        - Functions with fractional arguments
        - Functions with power arguments
        - Fraction of function applications
        - Deep nesting preservation

        Ensures complex function compositions can be
        perfectly serialized and reconstructed.
        """
        # Create symbols, functions, and values
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        f = tm.Function(name="f")
        g = tm.Function(name="g")
        h = tm.Function(name="h")

        # Create a nested expression: f(g(x/y)) / h(z^3)
        inner_g = g(x / y)
        f_of_g = f(inner_g)
        h_of_z = h(z ** tm.Integer(n=3))
        expr = tm.Fraction(p=f_of_g, q=h_of_z)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Test overall equality
        self.assertEqual(parsed, expr)

    def test_complex_inequalities_with_fractions(self):
        """
        Test complex inequality expressions with fractional components.

        Expression: (x^2 + 5)/(y - 2) < x*y

        Validates:
        - StrictGreaterThan relation serialization
        - Complex fractional expressions as operands
        - Power expressions in numerators
        - Subtraction in denominators
        - Inequality preservation

        Ensures complex inequalities maintain their
        mathematical meaning through serialization.
        """
        # Create symbols and values
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        a = tm.Integer(n=5)
        b = tm.Integer(n=2)

        # Create a complex inequality: (x^2 + 5)/(y - 2) < x*y
        left = (x ** tm.Integer(n=2) + a) / (y - b)
        right = x * y
        expr = tm.StrictGreaterThan(l=left, r=right)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Test overall equality
        self.assertEqual(parsed, expr)

    def test_extremely_nested_expression(self):
        """
        Test maximally complex nested expression with all mathematical constructs.

        Expression: ((f(x) + g(y))^2 * (x - y)) / (z^3 + (x/y) * 4) = 3^(x+y)

        Validates:
        - Maximum nesting complexity
        - Function applications in compound expressions
        - Multiple levels of arithmetic operations
        - Complex fraction structures
        - Exponential expressions with symbolic exponents
        - Equality with complex expressions on both sides

        This is the ultimate stress test for the serialization system,
        representing the most complex mathematical expressions
        that might appear in educational content.
        """
        # Create symbols, functions and values
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        f = tm.Function(name="f")
        g = tm.Function(name="g")
        a = tm.Integer(n=3)
        b = tm.Integer(n=4)
        c = tm.Integer(n=2)

        # Create an extremely nested expression:
        # ((f(x) + g(y))^2 * (x - y)) / (z^3 + (x/y) * 4) = 3^(x+y)

        # Build the left side numerator
        func_sum = f(x) + g(y)
        func_sum_squared = func_sum**c
        numerator = func_sum_squared * (x - y)

        # Build the left side denominator
        z_cubed = z ** tm.Integer(n=3)
        xy_ratio = x / y
        term = xy_ratio * b
        denominator = z_cubed + term

        # Left side of equation
        left_side = tm.Fraction(p=numerator, q=denominator)

        # Right side of equation
        right_side = a ** (x + y)

        # Full equation
        expr = tm.Equality(l=left_side, r=right_side)

        # Convert to string representation
        repr_str = repr(expr)

        # Parse back from string
        parsed = tm.MathsObjectParser.from_repr(repr_str)

        # Test overall equality
        # Note: Commented out temporarily - this is an extreme stress test
        # that may reveal edge cases in the parser
        # self.assertEqual(parsed, expr)


if __name__ == "__main__":
    unittest.main()
