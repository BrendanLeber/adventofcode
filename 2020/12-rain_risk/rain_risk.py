# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 12 - Rain Risk."""

import argparse
import pdb
import traceback
from copy import deepcopy
from dataclasses import dataclass
from math import cos, radians, sin
from typing import List, NamedTuple


class Instruction(NamedTuple):
    cmd: str
    value: int

    def __str__(self):
        return f"{self.cmd}{self.value}"


@dataclass
class Position:
    x: int = 0
    y: int = 0


@dataclass
class Ship:
    pos: Position = Position()
    waypoint: Position = Position(10, 1)
    facing: int = 0

    def __str__(self) -> str:
        ew = "east" if self.pos.x >= 0 else "west"
        ns = "north" if self.pos.y >= 0 else "south"
        wew = "east" if self.waypoint.x >= 0 else "west"
        wns = "north" if self.waypoint.y >= 0 else "south"
        return (
            f"{ew} {abs(self.pos.x)}, {ns} {abs(self.pos.y)}"
            f"; {self.facing}"
            f"; {wew} {abs(self.waypoint.x)}, {wns} {abs(self.waypoint.y)}"
        )

    def execute(self, cmd: Instruction) -> None:
        if cmd.cmd == "N":
            self.waypoint.y += cmd.value
        elif cmd.cmd == "S":
            self.waypoint.y -= cmd.value
        elif cmd.cmd == "E":
            self.waypoint.x += cmd.value
        elif cmd.cmd == "W":
            self.waypoint.x -= cmd.value
        elif cmd.cmd in ["R", "L"]:
            theta = radians(cmd.value)
            if cmd.cmd == "R":
                theta *= -1.0
            cx = self.waypoint.x * cos(theta) - self.waypoint.y * sin(theta)
            cy = self.waypoint.x * sin(theta) + self.waypoint.y * cos(theta)
            self.waypoint.x = int(round(cx))
            self.waypoint.y = int(round(cy))
        elif cmd.cmd == "F":
            self.pos.x += cmd.value * self.waypoint.x
            self.pos.y += cmd.value * self.waypoint.y

    def move(self, cmd: Instruction) -> None:
        if cmd.cmd == "N":
            self.pos.y += cmd.value
        elif cmd.cmd == "S":
            self.pos.y -= cmd.value
        elif cmd.cmd == "E":
            self.pos.x += cmd.value
        elif cmd.cmd == "W":
            self.pos.x -= cmd.value
        elif cmd.cmd == "R":
            self.facing += cmd.value
            self.facing %= 360
        elif cmd.cmd == "L":
            self.facing -= cmd.value
            self.facing %= 360
        elif cmd.cmd == "F":
            if self.facing == 0:
                self.pos.x += cmd.value
            elif self.facing == 90:
                self.pos.y -= cmd.value
            elif self.facing == 180:
                self.pos.x -= cmd.value
            elif self.facing == 270:
                self.pos.y += cmd.value


def from_file(fname: str):
    data: List[Instruction] = []
    with open(fname, "rt") as inf:
        for line in inf:
            line = line.strip()
            data.append(Instruction(line[0], int(line[1:])))
    return data


def manhattan_distance(a: Position, b: Position = Position()) -> int:
    """Return the Manhattan distance between two positions."""
    return abs(a.x - b.x) + abs(a.y - b.y)


def solve(commands: List[Instruction]):
    one = Ship()
    two = deepcopy(one)
    for cmd in commands:
        one.move(cmd)
        two.execute(cmd)

    return (manhattan_distance(one.pos), manhattan_distance(two.pos))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 12 - Rain Risk.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        puzzle = from_file(args.input)
        print(solve(puzzle))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
