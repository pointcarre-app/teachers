"""
Test micropip installation of antlr4-python3-runtime
"""

import unittest


class TestAntlr4Import(unittest.TestCase):
    """Test that antlr4-python3-runtime can be imported via micropip."""

    def test_antlr4_import(self):
        """Test basic import of antlr4 module."""
        try:
            import antlr4

            self.assertTrue(True, "antlr4 imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import antlr4: {e}")

    def test_antlr4_has_expected_attributes(self):
        """Test that antlr4 module has expected attributes."""
        try:
            import antlr4

            # Check for common antlr4 classes/attributes
            self.assertTrue(hasattr(antlr4, "InputStream"), "antlr4 should have InputStream")
            self.assertTrue(
                hasattr(antlr4, "CommonTokenStream"), "antlr4 should have CommonTokenStream"
            )
        except ImportError:
            self.skipTest("antlr4 not available")


if __name__ == "__main__":
    unittest.main()
