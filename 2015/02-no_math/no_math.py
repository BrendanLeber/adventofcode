#!/usr/bin/env python3
"""
Solve the Advent of Code Day 02 problem:
'I Was Told There Was No Math'.
"""


import fileinput
import re


def solve(data):
    """Solve parts one and two."""

    total_paper = 0
    total_ribbon = 0

    for package in data:
        length, width, height = package
        faces = [width * height, length * height, width * length]
        extra = min(faces)

        paper = 0
        for face in faces:
            paper = paper + 2 * face

        total_paper = total_paper + paper + extra

        perimiters = [2 * (width + height), 2 * (length + height), 2 * (width + length)]
        wrap = min(perimiters)
        bow = width * length * height
        total_ribbon = total_ribbon + wrap + bow

    return (total_paper, total_ribbon)


if __name__ == "__main__":
    # input line is LLLxWWWxHHH where L, W & H are digits
    p = re.compile(r"(\d+)x(\d+)x(\d+)")

    # read problem input from file or stdin
    puzzle_data = []
    for line in fileinput.input():
        m = p.match(line)
        if not m:
            raise ValueError("line '{0}' does not match pattern!".format(line))
        puzzle_data.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))

    print(solve(puzzle_data))
