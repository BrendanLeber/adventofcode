# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 20 - Jurassic Jigsaw."""

import argparse
import pdb
import traceback
import re
import math

N = -1
M = -1
TILES = {}


class Tile:
    def __init__(self, data):
        m = re.match(r"^Tile (\d+):$", data[0])
        self.id = int(m[1])

        self.pieces = [data[1 : M + 1]]
        for _ in range(3):
            self.pieces.append(self.rotate(self.pieces[-1]))
        self.pieces.append(self.flip(self.pieces[0]))
        for _ in range(3):
            self.pieces.append(self.rotate(self.pieces[-1]))

        self.pos = []
        for piece in self.pieces:
            x = [0, 0, 0, 0]
            x[0] = self.e2n(piece[0])
            x[1] = self.e2n("".join([i[-1] for i in piece]))
            x[2] = self.e2n(piece[M - 1])
            x[3] = self.e2n("".join([i[0] for i in piece]))
            self.pos.append(x)

    def rotate(self, piece):
        r = []
        for x in range(M):
            row = "".join(piece[y][x] for y in range(M - 1, -1, -1))
            r.append(row)
        return r

    def flip(self, piece):
        result = piece.copy()
        result.reverse()
        return result

    def e2n(self, edge):
        edge = edge.replace("#", "1")
        edge = edge.replace(".", "0")
        return int(edge, 2)

    def fit(self, south=-1, east=-1):
        if east == -1 and south == -1:
            return [(p[2], p[1]) for p in self.pos]
        if south == -1:
            return [(p[2], p[1]) for p in self.pos if east == p[3]]
        if east == -1:
            return [(p[2], p[1]) for p in self.pos if south == p[0]]
        return [(p[2], p[1]) for p in self.pos if east == p[3] and south == p[0]]


def fits(board, tile_ids):
    south, east = -1, -1
    if len(board) > 0:
        east = board[-1][2]
    if len(board) > N:
        south = board[-N][1]
        if len(board) % N == 0:
            east = -1
    return [(tid, nso, nea) for tid in tile_ids for nso, nea in TILES[tid].fit(south, east)]


def load_tiles(fname):
    global TILES, N, M
    with open(fname, "rt") as inf:
        data = inf.read()
    sections = data.strip().split("\n\n")
    TILES = {}
    for section in sections:
        lines = section.strip().split("\n")
        M = len(lines) - 1
        tile = Tile(lines)
        TILES[tile.id] = tile
    N = int(math.sqrt(len(TILES)))


def solve(board, rest):
    if len(rest) == 0:
        return board
    for tid, south, east in fits(board, rest):
        s = solve(board + [(tid, south, east)], rest - {tid})
        if s:
            return s


def part_one():
    tile_ids = set(TILES.keys())
    solution = solve([], tile_ids)
    return solution[0][0] * solution[N - 1][0] * solution[N * N - N][0] * solution[N * N - 1][0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 20 - Jurassic Jigsaw."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        load_tiles(args.input)
        print(part_one())
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
