# -*- coding: utf-8 -*-

import fileinput
import pdb
import traceback
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Reindeer:
    name: str
    speed: int
    fly: int
    rest: int
    flying: bool = True
    distance: int = 0
    ticks_remaining: int = 0
    points: int = 0

    def start(self) -> None:
        self.flying = True
        self.distance = 0
        self.ticks_remaining = self.fly

    def tick(self) -> None:
        if self.flying:
            self.distance += self.speed
        self.ticks_remaining -= 1
        if self.ticks_remaining == 0:
            if self.flying:
                self.flying = False
                self.ticks_remaining = self.rest
            else:
                self.flying = True
                self.ticks_remaining = self.fly


def decode_line(line: str) -> Reindeer:
    parts = line.strip().split()
    return Reindeer(parts[0], int(parts[3]), int(parts[6]), int(parts[13]))


def solve(contestants: List[Reindeer]) -> Tuple[int, int]:
    for deer in contestants:
        deer.start()

    for _ in range(2503):
        for deer in contestants:
            deer.tick()

        max_distance = -1
        for deer in contestants:
            if deer.distance > max_distance:
                max_distance = deer.distance

        for deer in contestants:
            if deer.distance == max_distance:
                deer.points += 1

    max_distance = 0
    max_points = 0
    for deer in contestants:
        max_distance = max(max_distance, deer.distance)
        max_points = max(max_points, deer.points)

    return (max_distance, max_points)


if __name__ == "__main__":
    try:
        deer = []
        for line in fileinput.input():
            deer.append(decode_line(line))
        print(solve(deer))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
