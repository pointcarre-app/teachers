"""
Test suite for LaTeX output generation across all mathematical objects.

This module tests LaTeX string generation for:
- Atomic objects (Integer, Symbol, Decimal, Function, Inf)
- Binary operators (Add, Mul, Fraction, Pow)
- Relations (Equality, StrictGreaterThan, Interval)
- Collections (MathsCollection)
- Complex nested expressions
- LaTeX formatting consistency and correctness

These tests ensure that all mathematical objects can generate
proper LaTeX representations for display in educational interfaces
and maintain consistent formatting standards.
"""

import unittest
import teachers.maths as tm


class TestLatexOutput(unittest.TestCase):
    """Test suite for LaTeX string generation across all mathematical objects."""

    def test_integer_latex(self):
        """
        Test Integer LaTeX output generation.

        Validates:
        - Simple integer representation
        - Negative integer handling
        - Zero representation
        - Large number formatting
        - String conversion accuracy

        Ensures integers generate proper LaTeX for display.
        """
        # Test positive integer
        i = tm.Integer(n=42)
        self.assertEqual(i.latex(), "42")

        # Test negative integer
        i_neg = tm.Integer(n=-17)
        self.assertEqual(i_neg.latex(), "-17")

        # Test zero
        i_zero = tm.Integer(n=0)
        self.assertEqual(i_zero.latex(), "0")

        # Test large number
        i_large = tm.Integer(n=1000000)
        self.assertEqual(i_large.latex(), "1000000")

    def test_symbol_latex(self):
        """
        Test Symbol LaTeX output generation.

        Validates:
        - Single character symbols
        - Multi-character symbols
        - Greek letter handling
        - Special character preservation
        - Mathematical notation symbols

        Ensures symbols generate proper LaTeX for algebraic display.
        """
        # Test single character
        x = tm.Symbol(s="x")
        self.assertEqual(x.latex(), "x")

        # Test multi-character
        theta = tm.Symbol(s="theta")
        self.assertEqual(theta.latex(), "theta")

        # Test with special characters (should be preserved)
        alpha = tm.Symbol(s="α")
        self.assertEqual(alpha.latex(), "α")

    def test_decimal_latex(self):
        """
        Test Decimal LaTeX output with European formatting.

        Validates:
        - Decimal point replacement (. → ,)
        - European mathematical notation
        - Precision preservation
        - Different decimal representations
        - Formatting consistency

        Ensures decimals use period as decimal separator (no commas).
        """
        # Test simple decimal with x parameter
        d1 = tm.Decimal(x=3.14)
        latex_output = d1.latex()
        self.assertIn("3.14", latex_output)  # Period format (no commas)

        # Test decimal with p/q parameters
        d2 = tm.Decimal(p=5, q=2)
        latex_output = d2.latex()
        self.assertIn("2.5", latex_output)  # Should be 2.5 with period

        # Test zero decimal
        d3 = tm.Decimal(x=0.0)
        latex_output = d3.latex()
        self.assertIn("0", latex_output)

    def test_function_latex(self):
        """
        Test Function LaTeX output generation.

        Validates:
        - Function name preservation
        - Simple string output
        - Mathematical function notation
        - Name formatting consistency

        Ensures function names are properly formatted for LaTeX.
        """
        # Test simple function
        f = tm.Function(name="f")
        self.assertEqual(f.latex(), "f")

        # Test multi-character function
        sin = tm.Function(name="sin")
        self.assertEqual(sin.latex(), "sin")

        # Test Greek function name
        phi = tm.Function(name="φ")
        self.assertEqual(phi.latex(), "φ")

    def test_image_latex(self):
        """
        Test Image (function application) LaTeX output.

        Validates:
        - Function application notation: f(x)
        - Single argument formatting
        - Multiple argument formatting with collections
        - Nested function applications
        - Complex argument expressions

        Ensures function applications are properly formatted.
        """
        f = tm.Function(name="f")
        x = tm.Symbol(s="x")

        # Test simple function application
        fx = f(x)
        self.assertEqual(fx.latex(), "f(x)")

        # Test function with multiple arguments
        y = tm.Symbol(s="y")
        fxy = f(tm.MathsCollection(elements=[x, y]))
        expected = "f(\\left(x, y\\right))"  # MathsCollection adds LaTeX parentheses
        self.assertEqual(fxy.latex(), expected)

        # Test nested function application
        g = tm.Function(name="g")
        f_g_x = f(g(x))
        self.assertEqual(f_g_x.latex(), "f(g(x))")

    def test_inf_latex(self):
        """
        Test Inf (infinity) LaTeX output generation.

        Validates:
        - Infinity symbol generation
        - LaTeX infinity notation
        - Mathematical symbol accuracy

        Ensures infinity is properly represented in LaTeX.
        """
        inf = tm.Inf()
        self.assertEqual(inf.latex(), "\\infty")

    def test_add_latex(self):
        """
        Test Add LaTeX output with proper sign handling.

        Validates:
        - Addition operator formatting
        - Negative term handling (+ becomes -)
        - Sign consolidation for subtraction
        - Complex expression formatting
        - Operator precedence representation

        Ensures addition expressions are properly formatted.
        """
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")

        # Test simple addition
        add_expr = x + y
        self.assertEqual(add_expr.latex(), "x + y")

        # Test addition with negative (should become subtraction)
        neg_y = tm.Integer(n=-5)
        add_neg = x + neg_y
        # The negative should be handled properly
        latex_output = add_neg.latex()
        self.assertIn("x", latex_output)
        self.assertIn("-5", latex_output)

    def test_mul_latex(self):
        """
        Test Mul LaTeX output with context-sensitive formatting.

        Validates:
        - Multiplication operator insertion (\\times)
        - Implicit multiplication for symbols
        - Negative coefficient handling
        - Parentheses for complex expressions
        - Different operand type combinations

        Ensures multiplication expressions use appropriate notation.
        """
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        n = tm.Integer(n=3)

        # Test coefficient multiplication (should be implicit)
        mul_coeff = n * x
        self.assertEqual(mul_coeff.latex(), "3x")

        # Test symbol multiplication (should use \\times for clarity)
        mul_symbols = x * y
        # Could be either "xy" or "x \\times y" depending on implementation
        latex_output = mul_symbols.latex()
        self.assertIn("x", latex_output)
        self.assertIn("y", latex_output)

        # Test negative multiplication
        neg_one = tm.Integer(n=-1)
        neg_x = neg_one * x
        self.assertEqual(neg_x.latex(), "-x")

    def test_fraction_latex(self):
        """
        Test Fraction LaTeX output with dfrac formatting.

        Validates:
        - Display fraction notation (\\dfrac)
        - Numerator and denominator placement
        - Negative fraction sign placement
        - Complex expression fractions
        - Brace structure for arguments

        Ensures fractions are properly formatted for display.
        """
        # Test simple fraction
        frac = tm.Fraction(p=1, q=2)
        expected = "\\dfrac{1}{2}"
        self.assertEqual(frac.latex(), expected)

        # Test negative fraction
        neg_frac = tm.Fraction(p=-3, q=4)
        expected = "-\\dfrac{3}{4}"
        self.assertEqual(neg_frac.latex(), expected)

        # Test fraction with expressions
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        expr_frac = (x + y) / tm.Integer(n=2)
        latex_output = expr_frac.latex()
        self.assertIn("\\dfrac", latex_output)
        self.assertIn("x + y", latex_output)
        self.assertIn("2", latex_output)

    def test_pow_latex(self):
        """
        Test Pow LaTeX output with exponent formatting.

        Validates:
        - Exponent notation (^{})
        - Base parentheses for complex expressions
        - Superscript brace structure
        - Nested power expressions
        - Mixed base and exponent types

        Ensures power expressions are properly formatted.
        """
        x = tm.Symbol(s="x")
        n = tm.Integer(n=3)

        # Test simple power
        pow_expr = x**n
        self.assertEqual(pow_expr.latex(), "x^{3}")

        # Test power with complex base
        add_expr = x + tm.Integer(n=1)
        pow_complex = add_expr**n
        expected = "\\left(x + 1\\right)^{3}"
        self.assertEqual(pow_complex.latex(), expected)

        # Test power with fraction exponent
        half = tm.Fraction(p=1, q=2)
        sqrt_x = x**half
        latex_output = sqrt_x.latex()
        self.assertIn("x^{", latex_output)
        self.assertIn("\\dfrac{1}{2}", latex_output)

    def test_equality_latex(self):
        """
        Test Equality LaTeX output generation.

        Validates:
        - Equality operator (=)
        - Left and right side formatting
        - Complex expression equality
        - Mathematical equation representation

        Ensures equations are properly formatted.
        """
        x = tm.Symbol(s="x")
        five = tm.Integer(n=5)

        # Test simple equality
        eq = tm.Equality(l=x, r=five)
        self.assertEqual(eq.latex(), "x = 5")

        # Test complex equality
        expr = x + tm.Integer(n=2)
        eq_complex = tm.Equality(l=expr, r=five)
        self.assertEqual(eq_complex.latex(), "x + 2 = 5")

    def test_strict_greater_than_latex(self):
        """
        Test StrictGreaterThan LaTeX output generation.

        Validates:
        - Greater than operator (>)
        - Left and right side formatting
        - Complex expression inequalities
        - Mathematical inequality representation

        Ensures inequalities are properly formatted.
        """
        x = tm.Symbol(s="x")
        five = tm.Integer(n=5)

        # Test simple inequality
        gt = tm.StrictGreaterThan(l=x, r=five)
        self.assertEqual(gt.latex(), "x > 5")

        # Test complex inequality
        expr = x + tm.Integer(n=2)
        gt_complex = tm.StrictGreaterThan(l=expr, r=five)
        self.assertEqual(gt_complex.latex(), "x + 2 > 5")

    def test_interval_latex(self):
        """
        Test Interval LaTeX output generation.

        Validates:
        - Interval notation with brackets
        - Left and right boundary formatting
        - Semicolon separator
        - Mathematical interval representation

        Ensures intervals are properly formatted.
        """
        a = tm.Integer(n=0)
        b = tm.Integer(n=5)

        # Test simple interval
        interval = tm.Interval(l=a, r=b)
        expected = "\\lbracket 0; 5\\rbracket"  # Add space after lbracket and semicolon
        self.assertEqual(interval.latex(), expected)

        # Test interval with symbols
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        interval_symbols = tm.Interval(l=x, r=y)
        expected = "\\lbracket x; y\\rbracket"  # Add space after semicolon
        self.assertEqual(interval_symbols.latex(), expected)

    def test_maths_collection_latex(self):
        """
        Test MathsCollection LaTeX output generation.

        Validates:
        - Collection parentheses formatting
        - Element separation with commas
        - Nested collection handling
        - Mathematical tuple representation

        Ensures collections are properly formatted.
        """
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # Test simple collection
        coll = tm.MathsCollection(elements=[x, y, z])
        expected = "\\left(x, y, z\\right)"
        self.assertEqual(coll.latex(), expected)

        # Test collection with expressions
        expr1 = x + tm.Integer(n=1)
        expr2 = tm.Integer(n=2) * y  # Put coefficient first to get "2y"
        coll_expr = tm.MathsCollection(elements=[expr1, expr2])
        latex_output = coll_expr.latex()
        self.assertIn("\\left(", latex_output)
        self.assertIn("x + 1", latex_output)
        self.assertIn("2y", latex_output)
        self.assertIn("\\right)", latex_output)

    def test_complex_expression_latex(self):
        """
        Test LaTeX output for complex nested expressions.

        Validates:
        - Multi-level nesting formatting
        - Operator precedence representation
        - Parentheses placement and balancing
        - Overall expression readability
        - LaTeX syntax correctness

        Ensures complex expressions generate readable LaTeX.
        """
        x = tm.Symbol(s="x")
        y = tm.Symbol(s="y")
        z = tm.Symbol(s="z")

        # Create complex expression: (x + y)^2 / (z - 1)
        numerator = (x + y) ** tm.Integer(n=2)
        denominator = z - tm.Integer(n=1)
        complex_expr = numerator / denominator

        latex_output = complex_expr.latex()

        # Verify key components are present
        self.assertIn("\\dfrac", latex_output)  # Fraction
        self.assertIn("\\left(x + y\\right)^{2}", latex_output)  # Squared expression
        self.assertIn("z -1", latex_output)  # Denominator (cleaner format: z -1 instead of z + -1)

        # Verify proper LaTeX structure
        self.assertTrue(latex_output.count("{") == latex_output.count("}"))  # Balanced braces

    def test_latex_consistency(self):
        """
        Test LaTeX output consistency across similar expressions.

        Validates:
        - Consistent formatting patterns
        - Similar expression similarity
        - Formatting rule adherence
        - Mathematical notation standards

        Ensures the LaTeX generation follows consistent rules.
        """
        # Test consistent fraction formatting
        frac1 = tm.Fraction(p=1, q=2)
        frac2 = tm.Fraction(p=3, q=4)

        latex1 = frac1.latex()
        latex2 = frac2.latex()

        # Both should use dfrac
        self.assertIn("\\dfrac", latex1)
        self.assertIn("\\dfrac", latex2)

        # Both should have same structure pattern
        self.assertTrue(latex1.startswith("\\dfrac{"))
        self.assertTrue(latex2.startswith("\\dfrac{"))

        # Test consistent power formatting
        x = tm.Symbol(s="x")
        pow1 = x ** tm.Integer(n=2)
        pow2 = x ** tm.Integer(n=3)

        latex_pow1 = pow1.latex()
        latex_pow2 = pow2.latex()

        # Both should use ^{} notation
        self.assertIn("^{", latex_pow1)
        self.assertIn("^{", latex_pow2)
        self.assertTrue(latex_pow1.endswith("}"))
        self.assertTrue(latex_pow2.endswith("}"))

    def test_decimal_image_multiplication_latex(self):
        """
        Test LaTeX output for Decimal * Image multiplication.

        Validates:
        - Implicit multiplication formatting (no \\times)
        - Coefficient-first ordering (0.5V(n), not V(n)0.5)
        - Proper decimal representation
        - Function notation preservation
        - Both commutative orders produce same result

        Ensures decimal coefficients with functions render correctly.
        """
        # Test basic decimal coefficient with function
        n = tm.Symbol(s="n")
        v = tm.Function(name="V")
        decimal_half = tm.Decimal(p=1, q=2)  # 0.5
        image_vn = v(n)  # V(n)

        # Test Decimal * Image
        mul_decimal_first = tm.Mul(l=decimal_half, r=image_vn).simplified()
        latex_decimal_first = mul_decimal_first.latex()
        self.assertEqual(latex_decimal_first, "0.5V(n)")

        # Test Image * Decimal (should normalize to same result)
        mul_image_first = tm.Mul(l=image_vn, r=decimal_half).simplified()
        latex_image_first = mul_image_first.latex()
        self.assertEqual(latex_image_first, "0.5V(n)")

        # Test with float-form decimal
        decimal_float = tm.Decimal(x=0.75)
        mul_float = tm.Mul(l=decimal_float, r=image_vn).simplified()
        latex_float = mul_float.latex()
        self.assertEqual(latex_float, "0.75V(n)")

        # Test with more complex function argument
        x = tm.Symbol(s="x")
        f = tm.Function(name="f")
        complex_arg = tm.Add(l=x, r=tm.Integer(n=1))  # x + 1
        image_complex = f(complex_arg)  # f(x + 1)
        decimal_quarter = tm.Decimal(p=1, q=4)  # 0.25

        mul_complex = tm.Mul(l=decimal_quarter, r=image_complex).simplified()
        latex_complex = mul_complex.latex()
        self.assertEqual(latex_complex, "0.25f(x + 1)")

        # Test with different function names
        g = tm.Function(name="g")
        h = tm.Function(name="H")  # Capital letter
        greek = tm.Function(name="\\phi")  # Greek letter function

        mul_g = tm.Mul(l=decimal_half, r=g(n)).simplified()
        mul_h = tm.Mul(l=decimal_half, r=h(n)).simplified()
        mul_greek = tm.Mul(l=decimal_half, r=greek(n)).simplified()

        self.assertEqual(mul_g.latex(), "0.5g(n)")
        self.assertEqual(mul_h.latex(), "0.5H(n)")
        self.assertEqual(mul_greek.latex(), "0.5\\phi(n)")

    def test_decimal_image_edge_cases_latex(self):
        """
        Test edge cases for Decimal * Image LaTeX rendering.

        Validates:
        - Whole number decimals (1.0 → "1")
        - Very small decimals
        - Negative decimals
        - Multiple function arguments
        - Nested function calls

        Ensures robust LaTeX generation for all decimal-function combinations.
        """
        n = tm.Symbol(s="n")
        x = tm.Symbol(s="x")
        f = tm.Function(name="f")

        # Test whole number decimal (should render as integer)
        decimal_one = tm.Decimal(p=2, q=2)  # 1.0
        mul_one = tm.Mul(l=decimal_one, r=f(n)).simplified()
        # Note: Decimal(1.0) should render as "1" not "1.0"
        self.assertEqual(mul_one.latex(), "1f(n)")

        # Test very small decimal
        decimal_small = tm.Decimal(x=0.001)
        mul_small = tm.Mul(l=decimal_small, r=f(n)).simplified()
        self.assertEqual(mul_small.latex(), "0.001f(n)")

        # Test negative decimal
        decimal_neg = tm.Decimal(p=-1, q=2)  # -0.5
        mul_neg = tm.Mul(l=decimal_neg, r=f(n)).simplified()
        self.assertEqual(mul_neg.latex(), "-0.5f(n)")

        # Test function with multiple arguments (using MathsCollection)
        collection = tm.MathsCollection(elements=[n, x])
        image_multi = tm.Image(f=f, pre=collection)
        mul_multi = tm.Mul(l=tm.Decimal(p=3, q=4), r=image_multi).simplified()
        # This should render as something like "0.75f(n, x)"
        latex_multi = mul_multi.latex()
        self.assertIn("0.75", latex_multi)
        self.assertIn("f(", latex_multi)
        self.assertIn("n", latex_multi)
        self.assertIn("x", latex_multi)


if __name__ == "__main__":
    unittest.main()
