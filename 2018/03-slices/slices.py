#!/usr/bin/env python


from collections import namedtuple
from dataclasses import dataclass
import fileinput
import re


Claim = namedtuple("Claim", ["claim", "area"])


@dataclass
class Rect:
    """A rectangle in 2-dimensional space."""

    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0


def part_one(claims: list) -> int:
    fabric = [[0] * 1000 for _ in range(1000)]

    for claim in claims:
        for row in range(claim.area.top, claim.area.bottom):
            for col in range(claim.area.left, claim.area.right):
                fabric[row][col] += 1

    overlaps = 0
    for row in fabric:
        for col in row:
            if col > 1:
                overlaps += 1

    return overlaps


def part_two(claims: list) -> int:
    fabric = [[0] * 1000 for _ in range(1000)]

    for claim in claims:
        for row in range(claim.area.top, claim.area.bottom):
            for col in range(claim.area.left, claim.area.right):
                fabric[row][col] += 1

    for claim in claims:
        max_claimed = 0
        for row in range(claim.area.top, claim.area.bottom):
            for col in range(claim.area.left, claim.area.right):
                max_claimed = max(max_claimed, fabric[row][col])
        if max_claimed == 1:
            return claim.claim

    return -1


if __name__ == "__main__":
    pattern = re.compile(
        r"""
        ^\#(?P<claim>[0-9]+) \s+@\s+
        (?P<from_left>[0-9]+) , (?P<from_top>[0-9]+)
        :\s+
        (?P<width>[0-9]+) x (?P<height>[0-9]+)$""",
        re.VERBOSE,
    )

    claims = []
    for line in fileinput.input():
        matches = pattern.search(line.strip())
        if not matches:
            raise TypeError(f"input line does not match expected format: '{line}'")
        area = Rect(
            int(matches.group("from_left")),
            int(matches.group("from_top")),
            int(matches.group("from_left")) + int(matches.group("width")),
            int(matches.group("from_top")) + int(matches.group("height")),
        )
        claims.append(Claim(int(matches.group("claim")), area))

    print(part_one(claims))
    print(part_two(claims))
