# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import deepcopy
from typing import Tuple

VERBOSE: bool = False

START_STATE = [
    [("promethium", "generator"), ("promethium", "microchip")],
    [
        ("cobalt", "generator"),
        ("curium", "generator"),
        ("ruthenium", "generator"),
        ("plutonium", "generator"),
    ],
    [
        ("cobalt", "microchip"),
        ("curium", "microchip"),
        ("ruthenium", "microchip"),
        ("plutonium", "microchip"),
    ],
    [],
]


def check_valid(dest, pt1, pt2, valid_floors, valid_elevator):
    test_dest = list(valid_floors[dest])
    test_dest.append(pt1)
    if pt2:
        test_dest.append(pt2)

    for i in test_dest:
        if i[1] == "microchip":
            for j in test_dest:
                if j[1] == "generator" and (i[0], "generator") not in test_dest:
                    return False

    if pt1 not in valid_floors[valid_elevator]:
        return False
    if pt2 and pt2 not in valid_floors[valid_elevator]:
        return False

    test_floor = list(valid_floors[valid_elevator])
    test_floor.remove(pt1)
    if pt2:
        test_floor.remove(pt2)

    for i in test_floor:
        if i[1] == "microchip" and (i[0], "generator") not in test_floor:
            for j in test_floor:
                if j != i and j[1] == "generator":
                    return False

    return True


def do_move(destination, pt1, pt2, in_floors, in_elevator, steps):
    move_floors = deepcopy(in_floors)
    move_elevator = int(in_elevator)
    valid = check_valid(destination, pt1, pt2, move_floors, move_elevator)
    state = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], destination]
    if not valid:
        return False
    else:
        move_floors[destination].append(pt1)
        if pt2:
            move_floors[destination].append(pt2)
        move_floors[move_elevator].remove(pt1)
        if pt2:
            move_floors[move_elevator].remove(pt2)
        move_floors[destination] = sorted(move_floors[destination])
        move_elevator = destination
        for i in range(4):
            for j in move_floors[i]:
                if j[1] == "microchip":
                    if (j[0], "generator") not in move_floors[i]:
                        state[i][0] += 1
                    else:
                        state[i][2] += 1
                else:
                    if (j[0], "microchip") not in move_floors[i]:
                        state[i][1] += 1

    return [move_floors, move_elevator, state, steps]


def find_path(start_floors, amount):
    steps = 1
    start_elevator = 0
    moves = []
    seen = []
    for i in start_floors[start_elevator]:
        test = do_move(1, i, None, start_floors, start_elevator, steps)
        if test and test[2] not in seen:
            moves.append(test)
            seen.append(test[2])
        for j in start_floors[start_elevator]:
            if i != j:
                test = do_move(1, i, j, start_floors, start_elevator, steps)
                if test and test[2] not in seen:
                    moves.append(test)
                    seen.append(test[2])

    found = False
    while not found:
        steps += 1
        for i in deepcopy(moves):
            moves.remove(i)
            if len(i[0][3]) == amount:
                return i[3]
            floors = i[0]
            elevator = i[1]
            test_floors = deepcopy(floors)
            test_elevator = int(elevator)
            for p1 in test_floors[test_elevator]:
                for p2 in test_floors[test_elevator]:
                    if p1 != p2:
                        if test_elevator < 3:
                            test = do_move(
                                test_elevator + 1, p1, p2, test_floors, test_elevator, steps
                            )
                            if test and test[2] not in seen:
                                moves.append(test)
                                seen.append(test[2])
                if test_elevator < 3:
                    test = do_move(test_elevator + 1, p1, None, test_floors, test_elevator, steps)
                    if test and test[2] not in seen:
                        moves.append(test)
                        seen.append(test[2])
                test_floors = deepcopy(floors)
                if elevator > 1 and all(test_floors[x] == [] for x in range(1, elevator)):
                    continue
                if test_elevator > 0:
                    test = do_move(test_elevator - 1, p1, None, test_floors, test_elevator, steps)
                    if test and test[2] not in seen:
                        moves.append(test)
                        seen.append(test[2])
                if p2 in test_floors[test_elevator]:
                    if p1[0] != p2[0]:
                        if test_elevator > 0:
                            test = do_move(
                                test_elevator - 1, p1, p2, test_floors, test_elevator, steps
                            )
                            if test and test[2] not in seen:
                                moves.append(test)
                                seen.append(test[2])


def solve() -> Tuple[int, int]:
    breakpoint()
    one: int = find_path(START_STATE, 10)
    two: int = None
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 11 - Radioisotope Thermoelectric Generators."
    )
    #    parser.add_argument(
    #        "input",
    #        type=str,
    #        default="input.txt",
    #        nargs="?",
    #        help="The puzzle input.  (Default %(default)s)",
    #    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    try:
        print(solve())
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
