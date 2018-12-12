#!/usr/bin/env python


import fileinput
import sys


def part_one(polymer: str) -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    while True:
        old_len = len(polymer)
        for unit in alphabet:
            polymer = polymer.replace(unit + unit.upper(), "")
            polymer = polymer.replace(unit.upper() + unit, "")

        if len(polymer) == old_len:
            break

    return len(polymer)


def part_two(polymer: str) -> int:
    best_length = sys.maxsize
    unit_types = set(polymer.casefold())
    for unit_type in unit_types:
        temp_polymer = polymer
        temp_polymer = temp_polymer.replace(unit_type, "")
        temp_polymer = temp_polymer.replace(unit_type.upper(), "")
        best_length = min(best_length, part_one(temp_polymer))
    return best_length


if __name__ == "__main__":
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part_one(lines[0]))
    print(part_two(lines[0]))
