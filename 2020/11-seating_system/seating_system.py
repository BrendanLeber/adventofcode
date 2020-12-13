# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 11 - Seating System."""

import argparse
import pdb
import traceback
from enum import Enum
from typing import Dict, List, Tuple

import numpy as np


class Seat_Value(int, Enum):
    WALL = -2
    FLOOR = -1
    EMPTY = 0
    OCCUPIED = 1


INPUT_TO_ENUM: Dict[str, Seat_Value] = {
    "*": Seat_Value.WALL,
    "L": Seat_Value.EMPTY,
    "#": Seat_Value.OCCUPIED,
    ".": Seat_Value.FLOOR,
}


ENUM_TO_INPUT: Dict[Seat_Value, str] = {
    Seat_Value.WALL: "*",
    Seat_Value.EMPTY: "L",
    Seat_Value.OCCUPIED: "#",
    Seat_Value.FLOOR: ".",
}


OFFSETS: List[Tuple[int, int]] = []
for xoff in [-1, 0, 1]:
    for yoff in [-1, 0, 1]:
        if yoff or xoff:
            OFFSETS.append((xoff, yoff))


def from_file(fname: str):
    field: List[List[Seat_Value]] = []
    with open(fname, "rt") as inf:
        for line in inf:
            line = line.strip()
            field.append([Seat_Value.WALL] + list(map(INPUT_TO_ENUM.get, line)) + [Seat_Value.WALL])
    field.insert(0, [Seat_Value.WALL] * len(field[0]))
    field.append([Seat_Value.WALL] * len(field[0]))
    return np.array(field)


def seats_to_str(seats):
    text = []
    for row in seats.tolist()[1 : seats.shape[0] - 1]:
        text.append("".join(map(ENUM_TO_INPUT.get, row[1 : len(row) - 1])))
    return "\n".join(text)


def fill_occupied(seats, occupied):
    occupied[:] = -1
    for row in range(1, seats.shape[0] - 1):
        for col in range(1, seats.shape[1] - 1):
            counter: int = 0
            for xoff, yoff in OFFSETS:
                if seats[row + yoff, col + xoff] == Seat_Value.OCCUPIED:
                    counter += 1
            occupied[row, col] = counter


def fill_occupied_2(seats, occupied):
    occupied[:] = -1
    for row in range(1, seats.shape[0] - 1):
        for col in range(1, seats.shape[1] - 1):
            counter: int = 0
            for xoff, yoff in OFFSETS:
                r = row
                c = col
                while True:
                    r += yoff
                    c += xoff
                    if seats[r, c] == Seat_Value.FLOOR:
                        continue
                    if seats[r, c] in [Seat_Value.WALL, Seat_Value.EMPTY]:
                        break
                    counter += 1
                    break
            occupied[row, col] = counter


def next_generation(seats, occupied, target):
    for row in range(1, seats.shape[0] - 1):
        for col in range(1, seats.shape[1] - 1):
            if seats[row, col] == Seat_Value.EMPTY and occupied[row, col] == 0:
                seats[row, col] = Seat_Value.OCCUPIED
            if seats[row, col] == Seat_Value.OCCUPIED and occupied[row, col] >= target:
                seats[row, col] = Seat_Value.EMPTY


def solve(world):
    seats = world.copy()
    occupied = np.zeros(seats.shape, dtype=int)
    one = (seats == Seat_Value.OCCUPIED).sum()
    while True:
        fill_occupied(seats, occupied)
        next_generation(seats, occupied, 4)
        count_occupied = (seats == Seat_Value.OCCUPIED).sum()
        if one == count_occupied:
            break
        one = count_occupied

    seats = world.copy()
    occupied = np.zeros(seats.shape, dtype=int)
    two = (seats == Seat_Value.OCCUPIED).sum()
    while True:
        fill_occupied_2(seats, occupied)
        next_generation(seats, occupied, 5)
        count_occupied = (seats == Seat_Value.OCCUPIED).sum()
        if two == count_occupied:
            break
        two = count_occupied

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 11 - Seating System.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        seats = from_file(args.input)
        print(solve(seats))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
