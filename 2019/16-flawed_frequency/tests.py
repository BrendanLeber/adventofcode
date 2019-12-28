# -*- coding: utf-8 -*-


import unittest

from solve import get_message_1, get_message_2, get_pattern, phase


class SolveUnitTests(unittest.TestCase):
    def test_get_pattern(self):
        self.assertEqual(get_pattern(1, 8), [1, 0, -1, 0, 1, 0, -1, 0])
        self.assertEqual(get_pattern(2, 8), [0, 1, 1, 0, 0, -1, -1, 0])
        self.assertEqual(get_pattern(3, 8), [0, 0, 1, 1, 1, 0, 0, 0])
        self.assertEqual(get_pattern(4, 8), [0, 0, 0, 1, 1, 1, 1, 0])
        self.assertEqual(get_pattern(5, 8), [0, 0, 0, 0, 1, 1, 1, 1])
        self.assertEqual(get_pattern(6, 8), [0, 0, 0, 0, 0, 1, 1, 1])
        self.assertEqual(get_pattern(7, 8), [0, 0, 0, 0, 0, 0, 1, 1])
        self.assertEqual(get_pattern(8, 8), [0, 0, 0, 0, 0, 0, 0, 1])

    def test_phase(self):
        self.assertEqual(phase([1, 2, 3, 4, 5, 6, 7, 8]), [4, 8, 2, 2, 6, 1, 5, 8])
        self.assertEqual(phase([4, 8, 2, 2, 6, 1, 5, 8]), [3, 4, 0, 4, 0, 4, 3, 8])
        self.assertEqual(phase([3, 4, 0, 4, 0, 4, 3, 8]), [0, 3, 4, 1, 5, 5, 1, 8])
        self.assertEqual(phase([0, 3, 4, 1, 5, 5, 1, 8]), [0, 1, 0, 2, 9, 4, 9, 8])

    def test_full_part_one_1(self):
        signal = list(map(int, list("80871224585914546619083218645595")))
        self.assertEqual(get_message_1(signal, 100), "24176176")

    def test_full_part_one_2(self):
        signal = list(map(int, list("19617804207202209144916044189917")))
        self.assertEqual(get_message_1(signal, 100), "73745418")

    def test_full_part_one_3(self):
        signal = list(map(int, list("69317163492948606335995924319873")))
        self.assertEqual(get_message_1(signal, 100), "52432133")

    def test_full_part_two_1(self):
        signal = list(map(int, list("03036732577212944063491565474664")))
        self.assertEqual(get_message_2(signal, 100), "84462026")

    def test_full_part_two_2(self):
        signal = list(map(int, list("02935109699940807407585447034323")))
        self.assertEqual(get_message_2(signal, 100), "78725270")

    def test_full_part_two_3(self):
        signal = list(map(int, list("03081770884921959731165446850517")))
        self.assertEqual(get_message_2(signal, 100), "53553731")


if __name__ == "__main__":
    unittest.main()
