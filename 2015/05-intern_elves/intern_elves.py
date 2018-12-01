#!/usr/bin/env python3
"""
Solve the Advent of Code Day 05 problem:
'Doesn't He Have Intern-Elves For This?'
"""

from __future__ import print_function
import fileinput
import re
import sys


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, *kwargs)


def count_vowels(entry):
    """Count the number of vowels (aeiou) in the given string."""
    vowel_count = 0
    for vowel in "aeiou":
        vowel_count += entry.count(vowel)
    return vowel_count


def has_double_chars(entry):
    """Return True if there are double chars (aa, bb,...) in the given string."""
    for idx in range(1, len(entry)):
        if entry[idx] == entry[idx - 1]:
            return True
    return False


def naughty_strings_exist(entry):
    """Return True if any of the naughty strings exist in `xs`."""
    match = re.search(r"(ab|cd|pq|xy)", entry)
    return bool(match)


def solve_part_1(puzzle_data):
    """Solve the first part of the puzzle."""
    answer = 0
    for entry in puzzle_data:
        vowels_p = count_vowels(entry) >= 3
        double_p = has_double_chars(entry)
        not_naughty_p = not naughty_strings_exist(entry)
        if vowels_p and double_p and not_naughty_p:
            answer += 1
    return answer


def find_pairs(entry):
    """
    Return True if the string contains a pair of any two letters that
    appears at least twice in the string without overlapping, like
    xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it
    overlaps).
    """
    for idx in range(1, len(entry)):
        if re.search(entry[idx - 1 : idx + 1], entry[idx + 1 :]):
            return True
    return False


def find_triplet(entry):
    """
    Does the string contain a triplet?
    A letter which repeats with exactly one letter between them.
    """
    for idx in range(2, len(entry)):
        if entry[idx - 2] == entry[idx]:
            return True
    return False


def solve_part_2(puzzle_data):
    """Solve the second part of the puzzle."""
    answer = 0
    pairs_found = 0
    triplets_found = 0
    for entry in puzzle_data:
        pair_found = find_pairs(entry)
        if pair_found:
            pairs_found += 1

        triplet_found = find_triplet(entry)
        if triplet_found:
            triplets_found += 1

        if pair_found and triplet_found:
            answer += 1

    return answer


def solve(puzzle_data):
    """Solve the puzzle."""
    return (solve_part_1(puzzle_data), solve_part_2(puzzle_data))


if __name__ == "__main__":
    # read problem input from file or stdin
    data = []
    for line in fileinput.input():
        data.append(line.strip())

    result = solve(data)
    print(result)
