# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from re import findall
from typing import Dict, List, Tuple

from intcode import Intcode
from point import Point
from rect import Rectangle


def extract_ints(line: str) -> List[int]:
    return [int(x) for x in findall(r"-?\d+", line)]


def play_game(program: List[int], trace: bool) -> Dict[Tuple[int, int], int]:
    vm: Intcode = Intcode(program, True)
    canvas: Dict[Tuple[int, int], int] = dict()
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
        canvas[(x, y)] = block  # type: ignore

    return canvas


def print_canvas(canvas: Dict[Tuple[int, int], int]) -> None:
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

    for line in printable:
        print("".join(line))


def solve(program: List[int], trace: bool, display: bool) -> int:
    canvas: Dict[Tuple[int, int], int] = play_game(program, trace)
    if display:
        print_canvas(canvas)

    return sum([1 for b in canvas.values() if b == 2])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 13 - Care Package.")
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
            program.extend(extract_ints(line))
    try:
        print(solve(program, args.trace, args.display))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
