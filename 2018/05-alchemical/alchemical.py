#!/usr/bin/env python


import fileinput
import sys


def part_one(polymer: str) -> int:
    new_polymer = ""
    while True:
        for pos in range(len(polymer) - 1):
            if (
                polymer[pos].casefold() == polymer[pos + 1].casefold()
                and polymer[pos] != polymer[pos + 1]
            ):
                new_polymer = polymer[:pos] + polymer[pos + 2 :]
                break
        if len(new_polymer) == len(polymer):
            break
        polymer = new_polymer

    return len(new_polymer)


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
