# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from collections import deque
from re import findall
from typing import Dict, List, Tuple

from intcode import Intcode
from point import Point
from rect import Rectangle


def extract_ints(line: str) -> List[int]:
    return [int(x) for x in findall(r"-?\d+", line)]


def sign(x: int) -> int:
    """Return the sign of the argument.  [-1, 0, 1]"""
    return x and (1, -1)[x < 0]


def play_game(program: List[int], trace: bool) -> int:
    vm: Intcode = Intcode(program, True)
    vm.tape[0] = 2
    score: int = -1
    canvas: Dict[Tuple[int, int], int] = dict()
    ball_pos: Tuple[int, int] = (0, 0)
    paddle_pos: Tuple[int, int] = (0, 0)
    while True:
        if not vm.execute():
            break
        x = vm.last_output
        if not vm.execute():
            break
        y = vm.last_output
        if not vm.execute():
            break
        block = vm.last_output

        if block == 3:
            paddle_pos = (x, y)  # type: ignore
            vm.inputs = deque([sign(ball_pos[0] - paddle_pos[0])])
        elif block == 4:
            ball_pos = (x, y)  # type: ignore
            vm.inputs = deque([sign(ball_pos[0] - paddle_pos[0])])

        if x == -1 and y == 0:
            score = block  # type: ignore
        else:
            canvas[(x, y)] = block  # type: ignore

        if trace:
            print_canvas(canvas, score)

    if trace:
        print("\nfinal state:")
        print_canvas(canvas, score)

    return score


def print_canvas(canvas: Dict[Tuple[int, int], int], score: int) -> None:
    area: Rectangle = Rectangle(
        left=min([k[0] for k in canvas.keys()]),
        top=min([k[1] for k in canvas.keys()]),
        right=max([k[0] for k in canvas.keys()]),
        bottom=max([k[1] for k in canvas.keys()]),
    )

    offset: Point = Point(x=area.left * -1, y=area.top * -1)

    printable: List[List[str]] = [[" "] * (area.width() + 1) for _ in range(area.height() + 1)]
    for (column, row), block in canvas.items():
        printable[row + offset.y][column + offset.x] = (" ", "#", "*", "=", ".")[block]

    print(f"\nscore: {score}")
    for line in printable:
        print("".join(line))


def solve(program: List[int], trace: bool) -> int:
    return play_game(program, trace)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 13 - Care Package (Part Two)."
    )
    parser.add_argument(
        "input",
        type=str,
        default="blocks.int",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--trace", action="store_true", default=False, help="Display a trace of the painting bot."
    )
    args = parser.parse_args()

    program: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            program.extend(extract_ints(line))

    try:
        print(solve(program, args.trace))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
