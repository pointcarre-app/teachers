"""
Test suite for the MathsGenerator class functionality.

This module tests the mathematical object generation capabilities:
- Random integer generation with configurable bounds
- Seed-based reproducibility for testing
- Integration with the MathsObject system

The generator is crucial for creating mathematical exercises and
ensuring reproducible test scenarios.
"""

import unittest

import teachers.maths as tm
import teachers.generator as tg


class TestMathsGenerator(unittest.TestCase):
    """Test suite for MathsGenerator random mathematical object creation."""

    def test_random_integer(self):
        """
        Test random integer generation with seed reproducibility.

        Validates:
        - Deterministic behavior with fixed seed (seed=0)
        - Correct return type (tm.Integer)
        - Expected value for known seed
        - Default parameter behavior (min_val=0, max_val=100)

        This test ensures that the generator produces consistent,
        reproducible results for testing scenarios.
        """
        g = tg.MathsGenerator(0)
        n = g.random_integer()
        self.assertEqual(n, tm.Integer(n=49))


if __name__ == "__main__":
    unittest.main()
