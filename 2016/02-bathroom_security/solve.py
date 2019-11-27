# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Position:
    row: int = 0
    column: int = 0


KEYPAD: List[List[str]] = [
    [None, None, None, None, None, None, None],  # type: ignore
    [None, None, None, "1", None, None, None],  # type: ignore
    [None, None, "2", "3", "4", None, None],  # type: ignore
    [None, "5", "6", "7", "8", "9", None],  # type: ignore
    [None, None, "A", "B", "C", None, None],  # type: ignore
    [None, None, None, "D", None, None, None],  # type: ignore
    [None, None, None, None, None, None, None],  # type: ignore
]


def pos_to_key(pos: Position) -> str:
    return "123456789"[pos.row * 3 + pos.column]


def update_pos(move: str, pos: Position) -> Position:
    new_pos = deepcopy(pos)
    if move == "U":
        new_pos.row -= 1
    elif move == "D":
        new_pos.row += 1
    elif move == "L":
        new_pos.column -= 1
    elif move == "R":
        new_pos.column += 1
    else:
        raise ValueError(f"invalid move {move}")
    return new_pos


def solve(codes: List[List[str]], verbose=False) -> Tuple[str, str]:
    pos: Position = Position(row=1, column=1)  # start at '5'
    keys: List[str] = []
    for code in codes:
        for move in code:
            if move == "U":
                if pos.row > 0:
                    pos.row -= 1
            elif move == "D":
                if pos.row < 2:
                    pos.row += 1
            elif move == "R":
                if pos.column < 2:
                    pos.column += 1
            elif move == "L":
                if pos.column > 0:
                    pos.column -= 1
            else:
                raise ValueError(f"invalid move {move}")
        keys.append(pos_to_key(pos))
    one: str = "".join(keys)

    pos = Position(row=3, column=1)  # start at '5'
    keys = []
    for code in codes:
        for move in code:
            new_pos = update_pos(move, pos)
            key = KEYPAD[new_pos.row][new_pos.column]
            if key:
                pos = new_pos
        keys.append(KEYPAD[pos.row][pos.column])
    two: str = "".join(keys)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 2 - Bathroom Security."
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

    moves: List[List[str]] = []
    with open(args.input) as inf:
        for line in inf:
            moves.append(list(line.strip()))

    try:
        print(solve(moves, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
