# -*- coding: utf-8 -*-

import functools
import operator


def factorial(n: int) -> int:
    """Calculate the Factorial of N."""
    if n < 1:
        return 1
    return functools.reduce(operator.mul, range(1, n + 1))


def fibonacci(n: int, f0: int = 0, f1: int = 1) -> int:
    """Calculate the Nth Fibonacci Number."""
    for _ in range(n):
        f0, f1 = f1, f0 + f1
    return f0


def sign(x) -> int:
    """Return the sign of the argument.  [-1, 0, 1]"""
    return x and (1, -1)[x < 0]


if __name__ == "__main__":
    import unittest

    class MathematicsUnitTests(unittest.TestCase):
        def test_factorial(self):
            self.assertEqual(factorial(0), 1)
            self.assertEqual(factorial(1), 1)
            self.assertEqual(factorial(2), 2)
            self.assertEqual(factorial(3), 6)
            self.assertEqual(factorial(4), 24)
            self.assertEqual(factorial(13), 6227020800)

        def test_fibonacci(self):
            self.assertEqual(fibonacci(0), 0)
            self.assertEqual(fibonacci(1), 1)
            self.assertEqual(fibonacci(2), 1)
            self.assertEqual(fibonacci(3), 2)
            self.assertEqual(fibonacci(4), 3)
            self.assertEqual(fibonacci(40), 102334155)

    unittest.main()
