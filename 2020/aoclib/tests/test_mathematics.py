# -*- coding: utf-8 -*-

import unittest
from aoclib.mathematics import factorial, fibonacci, sign, manhattan_distance


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

    def test_manhattan_distance(self):
        self.assertEqual(manhattan_distance((0, 0), (0, 0)), 0)
        self.assertEqual(manhattan_distance((0, 0), (1, 1)), 2)
        self.assertEqual(manhattan_distance((0, 0), (-1, -1)), 2)

    def test_sign(self):
        self.assertEqual(sign(-32), -1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(sign(31), 1)


if __name__ == "__main__":
    unittest.main()
