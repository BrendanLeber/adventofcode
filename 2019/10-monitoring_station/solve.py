#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from math import atan, degrees, gcd
from typing import List, Tuple

Asteroid = Tuple[int, int]
Asteroids = List[Asteroid]


# def print_asteroids(field: Tuple[int, int], asteroids: Asteroids) -> None:
#     starmap = [["."] * field[0] for _ in range(field[1])]
#     for column, row in asteroids:
#         starmap[row][column] = "#"
#     for row in starmap:
#         print("".join(row))


def calc_angle(v: Tuple[int, int]) -> float:
    if v[1] == 0:
        return 90.0
    return degrees(atan(v[0] / v[1]))


def get_best_station(asteroids: Asteroids):
    in_los = [len(get_directions(s, asteroids)) for s in asteroids]
    sid = in_los.index(max(in_los))
    return asteroids[sid]


def get_directions(station: Asteroid, asteroids: Asteroids):
    directions = set()
    for asteroid in asteroids:
        if asteroid == station:
            continue
        v = (asteroid[0] - station[0], asteroid[1] - station[1])
        d = gcd(v[0], v[1])
        directions.add((v[0] // d, v[1] // d))
    return directions


def shoot(quadrants, station, asteroids, field):
    target_amount = len(asteroids) - 200
    while True:
        for quadrant in quadrants:
            for direction in quadrant:
                multi = 1
                while True:
                    coord = (station[0] + direction[0] * multi, station[1] + direction[1] * multi)
                    if coord[0] < 0 or coord[0] > field[0] or coord[1] < 0 or coord[1] > field[1]:
                        break
                    if coord in asteroids:
                        asteroids.remove(coord)
                        if len(asteroids) == target_amount:
                            return coord
                        break
                    multi += 1


def solve(field: Tuple[int, int], asteroids: Asteroids) -> Tuple[int, int]:
    one: int = -1
    for station in asteroids:
        dirs = get_directions(station, asteroids)
        one = max(len(dirs), one)

    station = get_best_station(asteroids)
    directions = list(get_directions(station, asteroids))
    directions.sort(key=lambda direction: calc_angle(direction), reverse=True)
    quadrants = split_quadrants(directions)
    asteroid_200 = shoot(quadrants, station, asteroids, field)
    two: int = asteroid_200[0] * 100 + asteroid_200[1]

    return (one, two)


def split_quadrants(directions):
    quadrants = []
    quadrants.append([x for x in directions if x[0] >= 0 and x[1] < 0])
    quadrants.append([x for x in directions if x[0] > 0 and x[1] >= 0])
    quadrants.append([x for x in directions if x[0] <= 0 and x[1] > 0])
    quadrants.append([x for x in directions if x[0] < 0 and x[1] <= 0])
    return quadrants


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 10 - Monitoring Station."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    lines: List[str] = []
    with open(args.input) as inf:
        for line in inf:
            lines.append(line.strip())

    try:
        height, width = len(lines), len(lines[0])
        asteroids: Asteroids = [
            (x, y) for y in range(height) for x in range(width) if lines[y][x] == "#"
        ]
        print(solve((width, height), asteroids))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
