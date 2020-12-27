#!/usr/bin/env python3
# pylint: disable=no-name-in-module
import re
from collections import defaultdict


with open("test.txt", "rt") as inf:
    data = inf.read()
tiles = data.split("\n\n")

M = 10


class Tile:
    def __init__(self, dat):
        td = dat.split("\n")
        self.id = int(re.sub(r"Tile (\d+):", r"\1", td[0]))
        self.pieces = [td[1 : M + 1]]
        for _ in range(3):
            self.pieces.append(self.rot(self.pieces[-1]))
        self.pieces.append(self.flip(self.pieces[0]))
        for _ in range(3):
            self.pieces.append(self.rot(self.pieces[-1]))

        self.pos = []
        for piece in self.pieces:
            x = [0, 0, 0, 0]
            x[0] = self.e2n(piece[0])
            x[1] = self.e2n("".join([i[-1] for i in piece]))
            x[2] = self.e2n(piece[M - 1])
            x[3] = self.e2n("".join([i[0] for i in piece]))
            self.pos.append(x)

    def rot(self, dat):
        r = []
        for x in range(M):
            row = "".join(dat[y][x] for y in range(M - 1, -1, -1))
            r.append(row)
        return r

    def flip(self, dat):
        fl = dat.copy()
        fl.reverse()
        return fl

    def e2n(self, edge):
        edge = edge.replace("#", "1")
        edge = edge.replace(".", "0")
        return int(edge, 2)

    def fit(self, so=-1, ea=-1):
        if ea == -1 and so == -1:
            return [(p[2], p[1]) for p in self.pos]
        if so == -1:
            return [(p[2], p[1]) for p in self.pos if ea == p[3]]
        if ea == -1:
            return [(p[2], p[1]) for p in self.pos if so == p[0]]
        return [(p[2], p[1]) for p in self.pos if ea == p[3] and so == p[0]]

    def getimage(self, so, ea):
        for i, p in enumerate(self.pos):
            if ea == p[1] and so == p[2]:
                return [r[1 : M - 1] for r in self.pieces[i][1 : M - 1]]


def fits(brd, ts):
    bl = len(brd)
    so, ea = -1, -1
    if bl > 0:
        ea = brd[-1][2]
    if bl >= N:
        so = brd[-N][1]
        if bl % N == 0:
            ea = -1
    return [(t, nso, nea) for t in ts for nso, nea in TD[t].fit(so, ea)]


def solve(brd, rest):
    if len(rest) == 0:
        return brd
    for t, so, ea in fits(brd, rest):
        s = solve(brd + [(t, so, ea)], rest - {t})
        if s:
            return s


N = 12
TD = defaultdict(Tile)
ts = set()
for d in tiles:
    t = Tile(d)
    TD[t.id] = t
    ts.add(t.id)
b = solve([], ts)
print(b[0][0] * b[N - 1][0] * b[N * N - N][0] * b[N * N - 1][0])
pieces = [TD[p[0]].getimage(p[1], p[2]) for p in b]
t = 0
im = []
for m in range(0, len(pieces), N):
    for i in range(M - 2):
        row = "".join(p[i] for p in pieces[m : m + N])
        im.append(row)
        t += row.count("#")
print("#=", t)

im.reverse()
mon = 0
m1 = r"..................#."
m2 = r"#....##....##....###"
m3 = r"(?=.#..#..#..#..#..#)"
for i, r in enumerate(im):
    ns1 = [m.start(0) for m in re.finditer(m2, r)]
    if len(ns1) > 1:
        print(f"Maybe {len(ns1)} Monsters", ns1)
    for n1 in ns1:
        if n1 and i > 0:
            print(i, n1)
            ns2 = [m.start(0) for m in re.finditer(m3, im[i + 1])]
            if n1 in ns2:
                print("n2!", ns2)
                if im[i - 1][n1 + 18] == "#":
                    mon += 1
                    print(f"Monster {mon}!")
                else:
                    print("Missing head")
print(f"{mon} sea monsters")
print(f"Roughness: {t-mon*15}")
