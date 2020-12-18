# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 17 - Conway Cubes (2)."""

import argparse
import pdb
import sys
import traceback
from typing import Dict, List, NamedTuple


class Extent(NamedTuple):
    lo: int = 0
    hi: int = 0


class Point(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0
    w: int = 0


World = Dict[Point, bool]


NEIGHBORS: List[Point] = []


def count_neighbors(world: World, pt: Point) -> int:
    neighbors: int = 0
    for offset in NEIGHBORS:
        off: Point = Point(pt.x + offset.x, pt.y + offset.y, pt.z + offset.z, pt.w + offset.w)
        if off in world:
            neighbors += 1
    return neighbors


def get_neighbor_offsets():
    offsets = []
    for w in [-1, 0, 1]:
        for z in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if x or y or z or w:
                        offsets.append(Point(x, y, z, w))
    return offsets


def get_world_cube(world: World):
    min_x = min_y = min_z = min_w = sys.maxsize
    max_x = max_y = max_z = max_w = -sys.maxsize
    for cube in world.keys():
        min_x = min(min_x, cube.x)
        max_x = max(max_x, cube.x)
        min_y = min(min_y, cube.y)
        max_y = max(max_y, cube.y)
        min_z = min(min_z, cube.z)
        max_z = max(max_z, cube.z)
        min_w = min(min_w, cube.w)
        max_w = max(max_w, cube.w)
    return (
        Extent(min_x, max_x + 1),
        Extent(min_y, max_y + 1),
        Extent(min_z, max_z + 1),
        Extent(min_w, max_w + 1),
    )


def print_world(world: World):
    cube = get_world_cube(world)
    for w in range(cube[3].lo, cube[3].hi):
        for z in range(cube[2].lo, cube[2].hi):
            print(f"z={z}, w={w}")
            for y in range(cube[1].lo, cube[1].hi):
                row = []
                for x in range(cube[0].lo, cube[0].hi):
                    pt = Point(x, y, z)
                    if pt in world:
                        row.append("#")
                    else:
                        row.append(".")
                print("".join(row))
        print("\n")


def run_cycle(world: World) -> World:
    next_generation: World = {}
    cube = get_world_cube(world)
    for w in range(cube[3].lo - 1, cube[3].hi + 1):
        for z in range(cube[2].lo - 1, cube[2].hi + 1):
            for y in range(cube[1].lo - 1, cube[1].hi + 1):
                for x in range(cube[0].lo - 1, cube[0].hi + 1):
                    pt = Point(x, y, z, w)
                    neighbors = count_neighbors(world, pt)
                    if pt not in world and neighbors == 3:
                        next_generation[pt] = True
                    elif pt in world and 2 <= neighbors <= 3:
                        next_generation[pt] = True
    return next_generation


def solve(world: World, limit: int = 6):
    # print("Before any cycles:")
    # print_world(world)

    for cycle in range(limit):
        world = run_cycle(world)
        # print(f"After {cycle} cycle(s):")
        # print_world(world)

    one = len(world)
    two = None

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 17 - Conway Cubes.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        NEIGHBORS = get_neighbor_offsets()

        world: World = {}
        with open(args.input, "rt") as inf:
            for y, line in enumerate(inf):
                for x, ch in enumerate(line.strip()):
                    if ch == "#":
                        world[Point(x=x, y=y, z=0, w=0)] = True

        print(solve(world))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
