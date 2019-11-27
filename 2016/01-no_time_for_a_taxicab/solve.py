# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

Move = Tuple[str, int]


@dataclass
class Position:
    row: int = 0
    column: int = 0


def solve(moves: List[Move], verbose=False) -> Tuple[int, int]:
    # start at the origin and facing north
    pos: Position = Position(0, 0)
    heading: int = 0

    for turn, steps in moves:
        if verbose:
            print(f"{pos} {heading} - {turn} {steps}", end="")

        # turn left or right
        if turn == "L":
            heading = wrap((0, 3), heading - 1)
        elif turn == "R":
            heading = wrap((0, 3), heading + 1)
        else:
            raise ValueError(f"invalid turn '{turn}'")

        # 0 = North, 1 = East, 2 = South, 3 = West
        if heading == 0:
            pos.row += steps
        elif heading == 1:
            pos.column += steps
        elif heading == 2:
            pos.row -= steps
        elif heading == 3:
            pos.column -= steps
        else:
            raise ValueError(f"invalid heading '{heading}'")

        if verbose:
            print(f" - {pos} {heading}")

    if verbose:
        print(f"Final: {pos} {heading}")

    one = taxicab_distance(Position(0, 0), pos)

    # start at the origin and facing north
    pos = Position(0, 0)
    heading = 0

    # save places we've visited for part two
    past_positions: List[Position] = []

    two = None
    for turn, steps in moves:
        if turn == "L":  # left
            heading = wrap((0, 3), heading - 1)
        elif turn == "R":  # right
            heading = wrap((0, 3), heading + 1)
        else:
            raise ValueError(f"invalid turn '{turn}'")

        for step in range(steps):
            if heading == 0:  # north
                pos.row += 1
            elif heading == 1:  # east
                pos.column += 1
            elif heading == 2:  # south
                pos.row -= 1
            elif heading == 3:  # west
                pos.column -= 1
            else:
                raise ValueError(f"invalid heading '{heading}'")

            # stop if we've visited here before
            if pos in past_positions and not two:
                if verbose:
                    print(f"found {pos} in past positions.")
                two = taxicab_distance(Position(0, 0), pos)
            else:
                past_positions.append(deepcopy(pos))

    if not two:
        raise ValueError("did not find repeated destination")

    return (one, two)


def taxicab_distance(p: Position, q: Position) -> int:
    return abs(p.column - q.column) + abs(p.row - q.row)


def wrap(span: Tuple[int, int], x: int) -> int:
    start: int = span[1] - span[0] + 1
    if x < span[0]:
        x += start * ((span[0] - x) // start + 1)
    return span[0] + (x - span[0]) % start


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 1 - No Time for a Taxicab."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()

    moves: List[Tuple[str, int]] = []
    with open(args.input) as inf:
        for line in inf:
            for fragment in line.strip().split():
                move = (fragment[0], int(fragment[1:].strip(",")))
                moves.append(move)

    try:
        print(solve(moves, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
