#!/usr/bin/env python


import fileinput


def part_one(changes: list) -> int:
    frequency: int = 0
    for freq in changes:
        frequency += freq
    return frequency


if __name__ == "__main__":
    frequency_changes = []
    for line in fileinput.input():
        frequency_changes.append(int(line))
    print(part_one(frequency_changes))
