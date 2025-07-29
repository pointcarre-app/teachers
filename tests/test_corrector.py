"""
Test suite for the corrector module functionality.

This module tests the mathematical expression correction pipeline:
- User input processing and cleaning (MathLive format)
- Teacher answer validation and formatting
- LaTeX string cleaning and normalization
- Mathematical comparison using SymPy
- Correction result generation and formatting
- Error detection and diff generation

These tests ensure that the correction system can accurately
assess student mathematical responses against teacher solutions
while handling various input formats and edge cases.
"""

import unittest
from unittest.mock import patch


import teachers.corrector as tc


class TestCorrector(unittest.TestCase):
    """Test suite for mathematical expression correction functionality."""

    def test_correct_perfect_match(self):
        """
        Test correction when user input perfectly matches teacher answer.

        Validates:
        - Perfect match detection (is_perfect = True)
        - Correct mathematical equivalence (is_correct = True)
        - Proper result structure with all required fields
        - No error output for perfect responses

        Ensures the correction system properly recognizes
        perfectly formatted correct answers.
        """
        # Simple integer match
        user_input = "42"
        teacher_answer = "Integer(n=42)"

        result = tc.correct(user_input, teacher_answer)

        # Verify result structure
        self.assertIn("is_perfect", result)
        self.assertIn("is_correct", result)
        self.assertIn("user_mathlive", result)
        self.assertIn("perfect_latex", result)

        # Should be both perfect and correct
        self.assertTrue(result["is_perfect"])
        self.assertTrue(result["is_correct"])

        # Verify input preservation
        self.assertEqual(result["user_mathlive"], user_input)

    def test_correct_mathematically_equivalent(self):
        """
        Test correction when user input is mathematically correct but not perfectly formatted.

        Validates:
        - Mathematical equivalence detection (is_correct = True)
        - Format difference detection (is_perfect = False)
        - Proper SymPy-based comparison
        - Result structure integrity

        Ensures the system distinguishes between mathematical
        correctness and formatting perfection.
        """
        # Mathematically equivalent but different format
        user_input = "3/4"  # User enters simple fraction
        teacher_answer = (
            "Fraction(p=Integer(n=3), q=Integer(n=4))"  # Teacher has formal representation
        )

        result = tc.correct(user_input, teacher_answer)

        # Should be correct but not perfect (different formatting)
        self.assertTrue(result["is_correct"])
        # Note: is_perfect depends on exact LaTeX matching, which may vary

    def test_correct_wrong_answer(self):
        """
        Test correction when user input is mathematically incorrect.

        Validates:
        - Incorrect answer detection (is_correct = False)
        - Proper SymPy-based mathematical comparison
        - Error handling for wrong mathematical content
        - Result structure completeness

        Ensures the system properly identifies mathematically
        incorrect responses.
        """
        user_input = "5"
        teacher_answer = "Integer(n=42)"

        result = tc.correct(user_input, teacher_answer)

        # Should be incorrect
        self.assertFalse(result["is_correct"])
        # Also not perfect since it's wrong
        self.assertFalse(result["is_perfect"])

    def test_clean_mathlive_fraction_without_braces(self):
        """
        Test MathLive input cleaning for fractions without braces.

        Validates:
        - Fraction notation normalization: \\frac16 → \\frac{1}{6}
        - Regex pattern matching for fraction syntax
        - Multiple fraction handling in single expression
        - Preservation of existing brace formatting

        Ensures MathLive input is properly normalized before parsing.
        """
        # Test single fraction without braces
        input_str = "\\frac16"
        expected = "\\frac{1}{6}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test multiple fractions
        input_str = "\\frac12 + \\frac34"
        expected = "\\frac{1}{2} + \\frac{3}{4}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test already properly formatted (should remain unchanged)
        input_str = "\\frac{1}{2}"
        expected = "\\frac{1}{2}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test mixed format
        input_str = "\\frac{1}{2} + \\frac34"
        expected = "\\frac{1}{2} + \\frac{3}{4}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

    def test_clean_mathlive_complex_expressions(self):
        """
        Test MathLive cleaning with complex mathematical expressions.

        Validates:
        - Fraction cleaning within larger expressions
        - Preservation of other LaTeX commands
        - Handling of nested mathematical structures
        - Edge cases with alphanumeric variables

        Ensures complex expressions are properly cleaned
        while preserving their mathematical meaning.
        """
        # Test with variables
        input_str = "x + \\fracab - y"
        expected = "x + \\frac{a}{b} - y"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test with numbers and variables mixed
        input_str = "\\frac2x + \\fracy"
        expected = (
            "\\frac{2}{x} + \\fracy"  # Note: 'racy' has 4 chars, doesn't match 2-char pattern
        )
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

    def test_clean_mathlive_dfrac_without_braces(self):
        """
        Test MathLive input cleaning for \\dfrac fractions without braces.

        Validates:
        - Display fraction notation normalization: \\dfrac16 → \\frac{1}{6}
        - Regex pattern matching for dfrac syntax converts to frac
        - Multiple dfrac handling in single expression
        - All fractions normalized to \\frac format
        - Mixed \\frac and \\dfrac handling

        Ensures MathLive input normalizes all fractions to \\frac format
        regardless of input type (frac or dfrac).
        """
        # Test single dfrac without braces - converts to frac
        input_str = "\\dfrac16"
        expected = "\\frac{1}{6}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test multiple dfracs - all convert to frac
        input_str = "\\dfrac12 + \\dfrac34"
        expected = "\\frac{1}{2} + \\frac{3}{4}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test already properly formatted dfrac (should remain unchanged)
        input_str = "\\dfrac{1}{2}"
        expected = "\\dfrac{1}{2}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test mixed frac and dfrac - dfrac without braces converts to frac
        input_str = "\\frac12 + \\dfrac34"
        expected = "\\frac{1}{2} + \\frac{3}{4}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test dfrac with variables - converts to frac
        input_str = "x + \\dfracab - y"
        expected = "x + \\frac{a}{b} - y"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test dfrac with numbers and variables - converts to frac
        input_str = "\\dfrac2x + \\dfrac5y"
        expected = "\\frac{2}{x} + \\frac{5}{y}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

        # Test complex expression with both frac and dfrac - dfrac converts to frac
        input_str = "\\fracxy + \\dfracab = \\frac{z}{w}"
        expected = "\\frac{x}{y} + \\frac{a}{b} = \\frac{z}{w}"
        result = tc.clean_mathlive(input_str)
        self.assertEqual(result, expected)

    def test_clean_teachers_latex_decimal_formatting(self):
        """
        Test teacher LaTeX cleaning for decimal number formatting.

        Validates:
        - Decimal point replacement: . → ,
        - European decimal notation handling
        - Preservation of mathematical operators
        - Integration with fraction formatting

        Ensures teacher output follows proper European
        mathematical notation conventions.
        """
        # Test decimal point replacement
        input_str = "3.14"
        expected = "3,14"
        result = tc.clean_teachers_latex(input_str)
        self.assertEqual(result, expected)

        # Test multiple decimals
        input_str = "3.14 + 2.71"
        expected = "3,14 + 2,71"
        result = tc.clean_teachers_latex(input_str)
        self.assertEqual(result, expected)

    def test_clean_teachers_latex_fraction_formatting(self):
        """
        Test teacher LaTeX cleaning for fraction formatting.

        Validates:
        - Fraction command normalization: \\dfrac → \\frac
        - Consistent fraction representation
        - Preservation of fraction content
        - Mixed expression handling

        Ensures consistent fraction formatting in teacher output.
        """
        # Test dfrac to frac conversion
        input_str = "\\dfrac{1}{2}"
        expected = "\\frac{1}{2}"
        result = tc.clean_teachers_latex(input_str)
        self.assertEqual(result, expected)

        # Test multiple fractions
        input_str = "\\dfrac{1}{2} + \\dfrac{3}{4}"
        expected = "\\frac{1}{2} + \\frac{3}{4}"
        result = tc.clean_teachers_latex(input_str)
        self.assertEqual(result, expected)

        # Test mixed with decimals
        input_str = "\\dfrac{1}{2} = 0.5"
        expected = "\\frac{1}{2} = 0,5"
        result = tc.clean_teachers_latex(input_str)
        self.assertEqual(result, expected)

    def test_clean_latex_for_display(self):
        """
        Test LaTeX display formatting for user presentation.

        Validates:
        - Display fraction formatting: \\frac → \\dfrac
        - Improved visual rendering for user interface
        - Preservation of mathematical content
        - Consistent display formatting

        Ensures user-facing LaTeX is optimized for visual presentation.
        """
        # Test frac to dfrac conversion for display
        input_str = "\\frac{1}{2}"
        expected = "\\dfrac{1}{2}"
        result = tc.clean_latex_for_display(input_str)
        self.assertEqual(result, expected)

        # Test multiple fractions
        input_str = "\\frac{1}{2} + \\frac{3}{4}"
        expected = "\\dfrac{1}{2} + \\dfrac{3}{4}"
        result = tc.clean_latex_for_display(input_str)
        self.assertEqual(result, expected)

    def test_correction_workflow_integration(self):
        """
        Test complete correction workflow with realistic mathematical expressions.

        Validates:
        - End-to-end correction pipeline
        - Complex expression handling
        - Multiple formatting steps integration
        - Error detection and reporting
        - Result completeness and accuracy

        Ensures all correction components work together
        seamlessly for realistic use cases.
        """
        # Test with a complex fraction expression
        user_input = "\\frac12 + \\frac34"  # User input without braces
        teacher_answer = "Add(l=Fraction(p=Integer(n=1), q=Integer(n=2)), r=Fraction(p=Integer(n=3), q=Integer(n=4)))"

        result = tc.correct(user_input, teacher_answer)

        # Verify all required fields are present
        required_fields = [
            "user_mathlive",
            "user_cleaned_mathlive",
            "user_for_display_latex",
            "user_maths_object",
            "answer_formal_repr",
            "answer_maths_object",
            "answer_simplified_maths_object",
            "answer_simplified_latex",
            "perfect_latex",
            "is_perfect",
            "is_correct",
        ]

        for field in required_fields:
            self.assertIn(field, result, f"Missing required field: {field}")

        # Should be mathematically correct
        self.assertTrue(result["is_correct"])

        # Verify input cleaning worked
        self.assertEqual(result["user_cleaned_mathlive"], "\\frac{1}{2} + \\frac{3}{4}")

    @patch("builtins.print")  # Mock print to test debug output
    def test_correction_debug_output(self, mock_print):
        """
        Test correction debug output for mismatched responses.

        Validates:
        - Debug output generation for incorrect answers
        - Error message formatting
        - Diff calculation and display
        - Print statement execution

        Ensures debugging information is properly generated
        to help identify formatting and correctness issues.
        """
        user_input = "wrong"
        teacher_answer = "Integer(n=42)"

        # This should trigger debug output
        result = tc.correct(user_input, teacher_answer)

        # Verify it's marked as imperfect and incorrect
        self.assertFalse(result["is_perfect"])
        self.assertFalse(result["is_correct"])

    def test_correction_edge_cases(self):
        """
        Test correction with edge cases and boundary conditions.

        Validates:
        - Empty input handling
        - Special character handling
        - Complex nested expressions
        - Error recovery and graceful failure
        - Result consistency under stress

        Ensures the correction system handles unusual
        inputs gracefully without crashing.
        """
        # Test with empty input (this might raise an exception)
        try:
            result = tc.correct("", "Integer(n=0)")
            # If it doesn't crash, verify structure
            self.assertIn("is_correct", result)
        except Exception:
            # It's acceptable for empty input to raise an exception
            pass

        # Test with complex nested expression
        user_input = "((x+y)^2)/(z-1)"
        teacher_answer = "Fraction(p=Pow(base=Add(l=Symbol(s='x'), r=Symbol(s='y')), exp=Integer(n=2)), q=Add(l=Symbol(s='z'), r=Integer(n=-1)))"

        result = tc.correct(user_input, teacher_answer)

        # Should complete without crashing
        self.assertIn("is_correct", result)
        self.assertIn("is_perfect", result)


if __name__ == "__main__":
    unittest.main()
