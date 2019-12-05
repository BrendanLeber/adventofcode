# -*- coding: utf-8 -*-


import unittest

from intcode import Intcode


class BasicTestCases(unittest.TestCase):
    def test_decode(self):
        cpu: Intcode = Intcode([])
        self.assertEqual(cpu.decode(1002), (2, 0, 1, 0))


if __name__ == "__main__":
    unittest.main()
