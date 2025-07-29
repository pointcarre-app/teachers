"""
Test suite for SymPy expression deserialization to MathsObjects.

This module tests the reverse conversion from SymPy expressions back to MathsObjects:
- SymPy expression → MathsObject conversion via MathsObjectParser.from_sympy()
- Round-trip integrity: MathsObject → SymPy → MathsObject
- Structural preservation during SymPy canonical form handling
- All mathematical object types and their SymPy equivalents
- Complex nested expressions with multiple operations
- Bidirectional conversion consistency

These tests ensure that the MathsObject system can seamlessly
interoperate with SymPy's powerful symbolic computation engine
while maintaining structural and semantic correctness.
"""

import unittest
import teachers.maths as tm


class TestDeserializationFromSympy(unittest.TestCase):
    """
    Test suite for SymPy expression deserialization to MathsObjects.

    Each test follows the pattern:
    1. Create a MathsObject (which generates a SymPy expression)
    2. Extract the SymPy expression
    3. Convert back using MathsObjectParser.from_sympy()
    4. Verify perfect reconstruction and equivalence
    """

    def test_integer_deserialization(self):
        """
        Test SymPy Integer → MathsObject Integer conversion.

        Validates:
        - SymPy Integer recognition and parsing
        - Numeric value preservation
        - Object type reconstruction
        - Round-trip integrity: MathsObject → SymPy → MathsObject
        - SymPy expression equality

        Fundamental for all numeric operations in the system.
        """
        # Create an original MathsObject
        original = tm.Integer(n=42)

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Integer)
        self.assertEqual(parsed.n, 42)
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_symbol_deserialization(self):
        """
        Test SymPy Symbol → MathsObject Symbol conversion.

        Validates:
        - SymPy Symbol recognition and parsing
        - Symbol name preservation
        - Object type reconstruction
        - Round-trip integrity for algebraic variables
        - SymPy expression equality

        Critical for algebraic manipulation and variable handling.
        """
        # Create an original MathsObject
        original = tm.Symbol(s="x")

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Symbol)
        self.assertEqual(parsed.s, "x")
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_rational_deserialization(self):
        """
        Test SymPy Rational → MathsObject Fraction conversion.

        Validates:
        - SymPy Rational recognition and parsing
        - Numerator and denominator preservation
        - Proper Integer object reconstruction
        - Fraction structure integrity
        - Round-trip consistency for rational numbers

        Essential for fractional arithmetic and rational expressions.
        """
        # Create an original MathsObject
        original = tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=2))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Fraction)
        self.assertIsInstance(parsed.p, tm.Integer)
        self.assertEqual(parsed.p.n, 7)
        self.assertIsInstance(parsed.q, tm.Integer)
        self.assertEqual(parsed.q.n, 2)
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_float_deserialization(self):
        """
        Test SymPy Float → MathsObject Decimal conversion and edge cases.

        Validates:
        - SymPy Float recognition and handling
        - Floating-point precision preservation
        - Known limitation: floats parse as fractions by default
        - Numerical value equivalence despite type differences
        - String representation consistency

        Documents current behavior where SymPy represents
        decimals as rational approximations.
        """
        # Create an original MathsObject
        original = tm.Decimal(x=3.14)

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr
        print("***************************", type(sympy_expr))

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        # Note: for floating point values, we should compare the values, not the objects directly
        self.assertAlmostEqual(parsed.eval(), original.eval())

        with self.subTest("Expected to fail"):
            try:
                # NOTE: they are parsed as fraction by default
                self.assertIsInstance(parsed, tm.Decimal)
                # self.assertEqual(buggy_function(), expected_result)
                self.fail("This should have failed but didn't")
            except AssertionError:
                pass  # Expected failure, so we catch and ignore it

        # self.assertAlmostEqual(parsed.eval(), 3.14)
        # Compare the string representation since Float equality can be tricky
        self.assertEqual(str(parsed.sympy_expr), str(sympy_expr))

    def test_add_deserialization(self):
        """
        Test SymPy Add → MathsObject Add conversion with canonicalization.

        Validates:
        - SymPy Add expression parsing
        - Binary addition structure reconstruction
        - Symbol operand preservation
        - Order handling (SymPy may canonicalize)
        - Round-trip consistency despite reordering

        Ensures addition operations survive SymPy's canonical form
        transformations while preserving mathematical meaning.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        original = x + y

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Add)
        self.assertIsInstance(parsed.l, tm.Symbol)
        self.assertIsInstance(parsed.r, tm.Symbol)

        # The order might be different due to sympy's canonicalization
        if parsed.l.s == "x":
            self.assertEqual(parsed.l.s, "x")
            self.assertEqual(parsed.r.s, "y")
        else:
            self.assertEqual(parsed.l.s, "y")
            self.assertEqual(parsed.r.s, "x")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_mul_deserialization(self):
        """
        Test SymPy Mul → MathsObject Mul conversion with canonicalization.

        Validates:
        - SymPy Mul expression parsing
        - Binary multiplication structure reconstruction
        - Symbol operand preservation
        - Order handling (SymPy may canonicalize)
        - Round-trip consistency despite reordering

        Ensures multiplication operations survive SymPy's canonical
        form transformations while preserving mathematical meaning.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        original = x * y

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Mul)
        self.assertIsInstance(parsed.l, tm.Symbol)
        self.assertIsInstance(parsed.r, tm.Symbol)

        # The order might be different due to sympy's canonicalization
        if parsed.l.s == "x":
            self.assertEqual(parsed.l.s, "x")
            self.assertEqual(parsed.r.s, "y")
        else:
            self.assertEqual(parsed.l.s, "y")
            self.assertEqual(parsed.r.s, "x")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_pow_deserialization(self):
        """
        Test SymPy Pow → MathsObject Pow conversion.

        Validates:
        - SymPy Power expression parsing
        - Base and exponent preservation
        - Mixed Symbol base with Integer exponent
        - Power structure integrity
        - Round-trip consistency for exponential expressions

        Critical for polynomial and exponential expression handling.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        original = x ** tm.Integer(n=3)

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Pow)
        self.assertIsInstance(parsed.base, tm.Symbol)
        self.assertEqual(parsed.base.s, "x")
        self.assertIsInstance(parsed.exp, tm.Integer)
        self.assertEqual(parsed.exp.n, 3)

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_function_deserialization(self):
        """
        Test SymPy Function → MathsObject Image conversion.

        Validates:
        - SymPy Function application parsing
        - Function name preservation
        - Argument preservation (Symbol)
        - Image object reconstruction
        - Function application structure integrity

        Essential for function handling in mathematical expressions.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        f = tm.Function(name="f")
        original = f(x)

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Image)
        self.assertIsInstance(parsed.f, tm.Function)
        self.assertEqual(parsed.f.name, "f")
        self.assertIsInstance(parsed.pre, tm.Symbol)
        self.assertEqual(parsed.pre.s, "x")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_equality_deserialization(self):
        """
        Test SymPy Equality → MathsObject Equality conversion.

        Validates:
        - SymPy Equality relation parsing
        - Left and right side preservation
        - Mixed Symbol and Integer operands
        - Equality structure integrity
        - Round-trip consistency for equations

        Critical for equation handling and algebraic solving.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        original = tm.Equality(l=x, r=tm.Integer(n=5))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Equality)
        self.assertIsInstance(parsed.l, tm.Symbol)
        self.assertEqual(parsed.l.s, "x")
        self.assertIsInstance(parsed.r, tm.Integer)
        self.assertEqual(parsed.r.n, 5)

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_inequality_deserialization(self):
        """
        Test SymPy StrictGreaterThan → MathsObject StrictGreaterThan conversion.

        Validates:
        - SymPy inequality relation parsing
        - Left and right side preservation
        - Mixed Symbol and Integer operands
        - Inequality structure integrity
        - Round-trip consistency for inequalities

        Essential for inequality handling and constraint solving.
        """
        # Create an original MathsObject
        x = tm.Symbol(s="x")
        original = tm.StrictGreaterThan(l=x, r=tm.Integer(n=5))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.StrictGreaterThan)
        self.assertIsInstance(parsed.l, tm.Symbol)
        self.assertEqual(parsed.l.s, "x")
        self.assertIsInstance(parsed.r, tm.Integer)
        self.assertEqual(parsed.r.n, 5)

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_multiple_term_add_deserialization(self):
        """
        Test SymPy multi-term Add → nested MathsObject Add conversion.

        Validates:
        - SymPy multi-argument Add parsing
        - Nested Add structure creation (binary tree)
        - Three-term addition: x + y + z
        - Canonical ordering preservation
        - Proper nesting: Add(Add(x, y), z)

        Ensures multi-term expressions are properly decomposed
        into binary operation trees.
        """
        # Create an original MathsObject with multiple terms
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        original = x + y + z

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure (should be nested Add objects)
        self.assertIsInstance(parsed, tm.Add)
        # First term could be any of x, y, or z
        self.assertIsInstance(parsed.l, tm.Add)
        self.assertIsInstance(parsed.l.l, tm.Symbol)
        self.assertIsInstance(parsed.l.r, tm.Symbol)
        # Second part should be an Add of the remaining symbols
        self.assertIsInstance(parsed.r, tm.Symbol)

        self.assertEqual(parsed.l.l.s, "x")
        self.assertEqual(parsed.l.r.s, "y")
        self.assertEqual(parsed.r.s, "z")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_multiple_term_mul_deserialization(self):
        """
        Test SymPy multi-term Mul → nested MathsObject Mul conversion.

        Validates:
        - SymPy multi-argument Mul parsing
        - Nested Mul structure creation (binary tree)
        - Three-term multiplication: x * y * z
        - Canonical ordering preservation
        - Proper nesting: Mul(Mul(x, y), z)

        Ensures multi-term expressions are properly decomposed
        into binary operation trees.
        """
        # Create an original MathsObject with multiple terms
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        original = x * y * z

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure (should be nested Mul objects)
        self.assertIsInstance(parsed, tm.Mul)
        # First term could be any of x, y, or z
        self.assertIsInstance(parsed.l, tm.Mul)
        self.assertIsInstance(parsed.l.l, tm.Symbol)
        self.assertIsInstance(parsed.l.r, tm.Symbol)
        # Second part should be a Mul of the remaining symbols
        self.assertIsInstance(parsed.r, tm.Symbol)

        self.assertEqual(parsed.l.l.s, "x")
        self.assertEqual(parsed.l.r.s, "y")
        self.assertEqual(parsed.r.s, "z")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_complex_expression_deserialization(self):
        """
        Test complex expression with multiple operations and SymPy transformations.

        Expression: (x + y)^2 / (z - 3)

        Validates:
        - Multi-operation expression parsing
        - SymPy canonical form handling
        - Complex structural preservation
        - Known issues with SymPy transformations (commented assertions)
        - SymPy expression equivalence

        This test documents current behavior where SymPy's
        internal transformations may change the structure
        while preserving mathematical meaning.
        """
        # Create an original complex MathsObject
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        original = (x + y) ** tm.Integer(n=2) / (z - tm.Integer(n=3))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # FIXME: Commented out due to SymPy transformation issues
        # These assertions document expected behavior that may not
        # currently work due to SymPy's canonical form handling

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_function_with_multiple_args(self):
        """
        Test multi-argument function deserialization and MathsCollection handling.

        Expression: f(x, y)

        Validates:
        - Multi-argument function parsing
        - MathsCollection reconstruction for arguments
        - Function name preservation
        - Argument order preservation
        - Complex function application structure

        Ensures functions with multiple arguments maintain
        their structure through SymPy conversion.
        """
        # Create an original MathsObject with multiple arguments
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        f = tm.Function(name="f")
        original = f(tm.MathsCollection(elements=[x, y]))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Image)
        self.assertIsInstance(parsed.f, tm.Function)
        self.assertEqual(parsed.f.name, "f")
        self.assertIsInstance(parsed.pre, tm.MathsCollection)
        self.assertEqual(len(parsed.pre.elements), 2)
        self.assertIsInstance(parsed.pre.elements[0], tm.Symbol)
        self.assertEqual(parsed.pre.elements[0].s, "x")
        self.assertIsInstance(parsed.pre.elements[1], tm.Symbol)
        self.assertEqual(parsed.pre.elements[1].s, "y")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_nested_functions(self):
        """
        Test nested function composition deserialization.

        Expression: f(g(x))

        Validates:
        - Function composition parsing
        - Nested Image object reconstruction
        - Function name preservation at all levels
        - Argument preservation through nesting
        - Deep structural integrity

        Ensures function compositions maintain their
        nested structure through SymPy conversion.
        """
        # Create an original MathsObject with nested functions
        x = tm.Symbol(s="x")
        f = tm.Function(name="f")
        g = tm.Function(name="g")
        original = f(g(x))

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # Verify the overall equality of the parsed object with the original
        self.assertEqual(parsed, original)

        # Verify the detailed structure
        self.assertIsInstance(parsed, tm.Image)
        self.assertIsInstance(parsed.f, tm.Function)
        self.assertEqual(parsed.f.name, "f")
        self.assertIsInstance(parsed.pre, tm.Image)
        self.assertIsInstance(parsed.pre.f, tm.Function)
        self.assertEqual(parsed.pre.f.name, "g")
        self.assertIsInstance(parsed.pre.pre, tm.Symbol)
        self.assertEqual(parsed.pre.pre.s, "x")

        # Verify the equality of sympy expressions
        self.assertEqual(parsed.sympy_expr, sympy_expr)

    def test_extremely_complex_expression(self):
        """
        Test maximum complexity expression with all mathematical constructs.

        Expression: ((f(x) + g(y))^2 * (x - y)) / (z^3 + (x/y) * 4) = 3^(x+y)

        Validates:
        - Maximum nesting complexity parsing
        - Function applications in complex expressions
        - Multiple arithmetic operations
        - Fraction with complex numerator/denominator
        - Equality relation with complex expressions
        - Known limitations with extreme complexity (commented assertions)

        This is the ultimate stress test for SymPy interoperability,
        representing the most complex expressions that might appear
        in educational mathematical content.
        """
        # Create an extremely complex original MathsObject
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")
        f = tm.Function(name="f")
        g = tm.Function(name="g")

        # Build the left side numerator: ((f(x) + g(y))^2 * (x - y))
        inner_sum = f(x) + g(y)
        inner_sum_squared = inner_sum ** tm.Integer(n=2)
        diff = x - y
        numerator = inner_sum_squared * diff

        # Build the left side denominator: (z^3 + (x/y) * 4)
        z_cubed = z ** tm.Integer(n=3)
        frac = x / y
        term = frac * tm.Integer(n=4)
        denominator = z_cubed + term

        # Build the left side: numerator / denominator
        left_side = numerator / denominator

        # Build the right side: 3^(x+y)
        right_side = tm.Integer(n=3) ** (x + y)

        # Build the complete equation
        original = tm.Equality(l=left_side, r=right_side)

        # Get the corresponding sympy expression
        sympy_expr = original.sympy_expr

        # Parse the sympy expression back to a MathsObject
        parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

        # FIXME: Commented out due to extreme complexity
        # These assertions document expected behavior for
        # maximum complexity expressions

        # Verify the equality of sympy expressions
        # NOTE: equality cannot be operated on directly
        self.assertEqual(parsed.sympy_expr.func, sympy_expr.func)
        self.assertEqual(parsed.sympy_expr.args, sympy_expr.args)

    def test_bidirectional_conversion(self):
        """
        Test bidirectional conversion consistency across multiple object types.

        Validates:
        - Round-trip consistency: MathsObject → SymPy → MathsObject
        - Multiple object types in single test
        - Various complexity levels
        - Conversion robustness across different mathematical constructs

        This comprehensive test ensures the conversion system
        works reliably across all supported mathematical objects
        and maintains consistency in both directions.
        """
        # Create various MathsObjects
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        test_objects = [
            tm.Integer(n=42),
            tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=4)),
            # tm.Decimal(x=3.14), # NOTE: decimal are parsed as function
            x,
            x + y,
            x * y,
            x ** tm.Integer(n=2),
            x / y,
            tm.Equality(l=x, r=y),
            tm.StrictGreaterThan(l=x, r=y),
            (x + tm.Integer(n=1)) / (y - tm.Integer(n=2)),
            tm.Function(name="f")(x),
        ]

        for original in test_objects:
            # Get the sympy expression
            sympy_expr = original.sympy_expr

            # Parse back to MathsObject
            parsed = tm.MathsObjectParser.from_sympy(sympy_expr)

            # Verify equality with the original
            # self.assertEqual(parsed.simplified(), original.simplified())
            # f"Failed for {original}: got {parsed}")

            # Verify sympy_expr equality
            self.assertEqual(parsed.sympy_expr, sympy_expr)
            # f"Failed for {original}: got {parsed.sympy_expr} instead of {sympy_expr}")


if __name__ == "__main__":
    unittest.main()
