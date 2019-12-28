# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import deepcopy
from typing import List, Optional

from geometry import Point
from intcode import Intcode
from utility import extract_ints
from search import astar, Node, node_to_path


def find_intersections(canvas: List[List[str]]) -> List[Point]:
    intersections: List[Point] = []
    for row in range(1, len(canvas) - 1):
        for col in range(1, len(canvas[0]) - 1):
            if canvas[row][col - 1 : col + 2] != ["#", "#", "#"]:
                continue
            if canvas[row - 1][col - 1 : col + 2] != [".", "#", "."]:
                continue
            if canvas[row + 1][col - 1 : col + 2] != [".", "#", "."]:
                continue
            intersections.append(Point(x=col, y=row))
    return intersections


def get_canvas(program: List[int], trace: bool) -> List[List[str]]:
    vm: Intcode = Intcode(program, True)
    canvas: List[List[str]] = []
    line: List[str] = []
    while True:
        if not vm.execute():
            break
        cell = vm.last_output
        if cell == 10:
            canvas.append(line)
            line = []
        else:
            line.append(chr(cell))  # type: ignore

    return canvas


def print_canvas(canvas: List[List[str]], intersections: Optional[List[Point]] = None) -> None:
    if intersections:
        canvas = deepcopy(canvas)
        for intersection in intersections:
            canvas[intersection.y][intersection.x] = "O"

    for row in canvas:
        print("".join(row))


def solve(program: List[int], trace: bool, display: bool):
    canvas: List[List[str]] = get_canvas(program, trace)
    if display:
        print_canvas(canvas)

    intersections = find_intersections(canvas)
    if display:
        print_canvas(canvas, intersections)
    one = sum([pt.x * pt.y for pt in intersections])

    two = None
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 17 - Set and Forget.")
    parser.add_argument(
        "input",
        type=str,
        default="ascii.int",
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
