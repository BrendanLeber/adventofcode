# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from hashlib import md5
from itertools import compress
from typing import List, Tuple


Position = Tuple[int, int]
Queue_Entry = Tuple[Position, List[Position], List[str]]


def doors(passcode: str, path: List[str]) -> List[bool]:
    paths: str = f"{passcode}{''.join(path)}"
    hashed: str = md5(paths.encode("utf-8")).hexdigest()[:4]
    return list((int(x, 16) > 10 for x in hashed))


def bfs(passcode: str, start: Tuple[int, int], goal: Tuple[int, int]):
    MOVES = {
        "U": lambda x, y: (x, y - 1),
        "D": lambda x, y: (x, y + 1),
        "L": lambda x, y: (x - 1, y),
        "R": lambda x, y: (x + 1, y),
    }
    queue: List[Queue_Entry] = [(start, [start], [])]
    while queue:
        (x, y), path, directions = queue.pop(0)
        for direction in compress("UDLR", doors(passcode, directions)):
            next_step = MOVES[direction](x, y)
            if not (0 <= next_step[0] < 4 and 0 <= next_step[1] < 4):
                continue
            elif next_step == goal:
                yield directions + [direction]
            else:
                queue.append((next_step, path + [next_step], directions + [direction]))


def solve(passcode: str) -> Tuple[str, int]:
    paths = list(bfs(passcode, (0, 0), (3, 3)))
    one: str = "".join(paths[0])
    two: int = len(paths[-1])
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 17 - Two Steps Forward."
    )
    parser.add_argument(
        "passcode",
        type=str,
        default="hhhxzeay",
        nargs="?",
        help="The vault passcode.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        print(solve(args.passcode))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
