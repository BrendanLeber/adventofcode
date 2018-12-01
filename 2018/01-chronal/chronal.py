#!/usr/bin/env python


import fileinput


def part_one(changes: list) -> int:
    frequency = 0
    for change in changes:
        frequency += change
    return frequency


def part_two(changes: list) -> int:
    frequency = 0
    frequencies_found = set()
    frequencies_found.add(frequency)
    while True:
        for change in changes:
            frequency += change
            if frequency in frequencies_found:
                return frequency
            frequencies_found.add(frequency)


if __name__ == "__main__":
    frequency_changes = []
    for line in fileinput.input():
        frequency_changes.append(int(line))
    print(part_one(frequency_changes))
    print(part_two(frequency_changes))
