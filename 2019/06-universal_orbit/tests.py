# -*- coding: utf-8 -*-


import unittest
from typing import List, Set, Tuple

from solve import unique_planets


class BasicTestCases(unittest.TestCase):
    def test_unique_planets(self):
        orbits: List[Tuple[str, str]] = [
            ("COM", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E"),
            ("E", "F"),
            ("B", "G"),
            ("G", "H"),
            ("D", "I"),
            ("E", "J"),
            ("J", "K"),
            ("K", "L"),
        ]

        expected: Set[str] = {"COM", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"}

        self.assertEqual(unique_planets(orbits), expected)


if __name__ == "__main__":
    unittest.main()
