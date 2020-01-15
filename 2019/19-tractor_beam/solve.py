# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List

from geometry import Size
from intcode import Intcode
from utility import extract_ints


def get_field(program: List[int], size: Size) -> List[List[int]]:
    vm: Intcode = Intcode(program, True)
    field: List[List[int]] = [[-1] * size.cx for _ in range(size.cy)]
    for row in range(size.cy):
        for col in range(size.cx):
            vm.reset()
            vm.add_inputs([col, row])
            if not vm.execute():
                raise RuntimeError("vm unexpectedly finished executing.")
            field[row][col] = vm.last_output
            if vm.execute():
                raise RuntimeError("vm did not finish executing.")
    return field


def check(vm: Intcode, x: int, y: int) -> int:
    vm.reset()
    vm.add_inputs([x, y])
    return vm.execute()


def print_field(canvas: List[List[int]]) -> None:
    for row in canvas:
        print("".join(map(lambda x: "#" if x == 1 else ".", row)))


def solve(program: List[int], size: Size, display: bool):
    field: List[List[int]] = get_field(program, size)
    if display:
        print_field(field)

    # part one: how many points are affected by the tractor beam?
    one = 0
    for row in field:
        one += sum(row)

    # part two: what coordinate starts a box of 100x100 that fits inside the beam?
    vm = Intcode(program)
    vm.silent_mode = True
    x = y = 0
    while not check(vm, x + 99, y):
        y += 1
        while not check(vm, x, y + 99):
            x += 1
    if display:
        print(f"({x}, {y})")
    two = x * 10000 + y

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 19 - Tractor Beam.")
    parser.add_argument(
        "input",
        type=str,
        default="drone.int",
        nargs="?",
        help="The puzzle input.  (Default '%(default)s')",
    )
    parser.add_argument(
        "width",
        type=int,
        default=50,
        nargs="?",
        help="The width of the field to scan.  (Default %(default)s)",
    )
    parser.add_argument(
        "height",
        type=int,
        default=50,
        nargs="?",
        help="The height of the field to scan.  (Default %(default)s)",
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
        print(solve(program, Size(args.width, args.height), args.display))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
