# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from enum import IntEnum
from typing import Dict, List, SupportsInt, Tuple, Union

from intcode import Intcode
from point import Point
from rect import Rectangle


class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Status(IntEnum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2


class Field(IntEnum):
    UNEXPLORED = 0
    EMPTY = 1
    WALL = 2
    DROID = 3


def move(pos, direction):
    if direction == Direction.NORTH:
        return (pos[0], pos[1] + 1)
    elif direction == Direction.SOUTH:
        return (pos[0], pos[1] - 1)
    elif direction == Direction.WEST:
        return (pos[0] - 1, pos[1])
    elif direction == Direction.EAST:
        return (pos[0] + 1, pos[1])
    raise ValueError(f"invalid direction {direction}")


def print_field(canvas, bot):
    area: Rectangle = Rectangle(
        left=min([k[0] for k in canvas.keys()]),
        top=min([k[1] for k in canvas.keys()]),
        right=max([k[0] for k in canvas.keys()]),
        bottom=max([k[1] for k in canvas.keys()]),
    )

    offset = Point(x=area.left * -1, y=area.top * -1)

    printable = [[" "] * (area.width() + 1) for _ in range(area.height() + 1)]
    for (column, row), field in canvas.items():
        printable[row + offset.y][column + offset.x] = (" ", ".", "#", "D")[field]
    printable[bot[1] + offset.y][bot[0] + offset.x] = "D"

    for line in printable:
        print("".join(line))


def solve(program, trace, display):
    vm = Intcode(program, True)

    bot = (0, 0)
    canvas = {bot: Field.EMPTY}

    while True:
        if trace:
            print(f"bot {bot}")
            print_field(canvas, bot)

        if not vm.execute():
            break
        direction = Direction(vm.last_input)
        status = Status(vm.last_output)

        if status == Status.WALL:
            # hit a wall so we don't move
            wall = move(bot, direction)
            canvas[wall] = Field.WALL
        elif status == Status.MOVED:
            bot = move(bot, direction)
            canvas[bot] = Field.EMPTY
        elif status == Status.OXYGEN:
            bot = move(bot, direction)
            canvas[bot] = Field.OXYGEN
        else:
            raise ValueError(f"unknown status {status}")

    one = None
    two = None

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 15 - Oxygen Supply.")
    parser.add_argument(
        "input",
        type=str,
        default="input.int",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--trace", action="store_true", default=False, help="Display a trace of the bot."
    )
    parser.add_argument(
        "--display", action="store_true", default=False, help="Display the final field."
    )
    args = parser.parse_args()

    program: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            program += list(map(int, line.strip().split(",")))
    try:
        print(solve(program, args.trace, args.display))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
