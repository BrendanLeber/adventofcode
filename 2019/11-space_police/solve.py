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


class Color(IntEnum):
    BLACK = 0
    WHITE = 1


class Turn(IntEnum):
    LEFT = -1
    RIGHT = 1

    @classmethod
    def from_integer(cls, turn: int):
        return Turn.LEFT if turn == 0 else Turn.RIGHT


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


@dataclass
class Bot:
    column: int = 0
    row: int = 0
    direction: Direction = Direction.NORTH

    def turn_and_move(self, turn: Turn) -> None:
        self.direction = Direction((self.direction + turn) % len(Direction))
        if self.direction == Direction.NORTH:
            self.row -= 1
        elif self.direction == Direction.EAST:
            self.column += 1
        elif self.direction == Direction.SOUTH:
            self.row += 1
        else:
            self.column -= 1

    @property
    def position(self) -> Tuple[int, int]:
        return (self.column, self.row)


def paint_canvas(
    program: List[int], initial_color: Color, trace: bool
) -> Dict[Tuple[int, int], Color]:
    if trace:
        steps: List[Tuple[Tuple[int, int], int]] = []
    vm: Intcode = Intcode(program, True)
    bot = Bot()
    canvas: Dict[Tuple[int, int], Union[str, bytes, SupportsInt]] = dict()
    if trace:
        steps.append(((0, 0), initial_color.value))
    vm.add_inputs([initial_color])
    while True:
        if not vm.execute():
            break
        canvas[bot.position] = Color(vm.last_output)  # type: ignore
        if trace:
            steps.append((bot.position, vm.last_output))  # type: ignore
        if not vm.execute():
            break
        bot.turn_and_move(Turn.from_integer(vm.last_output))  # type: ignore
        vm.add_inputs([canvas.get(bot.position, Color.BLACK).value])  # type: ignore
    if trace:
        print("** trace:")
        for pos, color in steps:
            print(f"{pos} {color}")
    return canvas  # type: ignore


def print_canvas(canvas: Dict[Tuple[int, int], Color]) -> None:
    area: Rectangle = Rectangle(
        left=min([k[0] for k in canvas.keys()]),
        top=min([k[1] for k in canvas.keys()]),
        right=max([k[0] for k in canvas.keys()]),
        bottom=max([k[1] for k in canvas.keys()]),
    )

    offset: Point = Point(x=area.left * -1, y=area.top * -1)

    printable: List[List[str]] = [[" "] * (area.width() + 1) for _ in range(area.height() + 1)]
    for (column, row), color in canvas.items():
        printable[row + offset.y][column + offset.x] = (" ", "#")[color]

    for line in printable:
        print("".join(line))


def solve(program: List[int], trace: bool, display: bool) -> Tuple[int, int]:
    canvas: Dict[Tuple[int, int], Color] = paint_canvas(program, Color.BLACK, trace)
    if display:
        print("\n** one:")
        print_canvas(canvas)
    one: int = len(canvas)

    canvas = paint_canvas(program, Color.WHITE, trace)
    if display:
        print("\n*  if display:* two:")
        print_canvas(canvas)
    two: int = -1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 11 - Space Police.")
    parser.add_argument(
        "input",
        type=str,
        default="input.int",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--trace", action="store_true", default=False, help="Display a trace of the painting bot."
    )
    parser.add_argument(
        "--display", action="store_true", default=False, help="Display the final painting."
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
