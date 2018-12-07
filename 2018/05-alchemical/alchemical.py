#!/usr/bin/env python


import fileinput


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


if __name__ == "__main__":
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part_one(lines[0]))
