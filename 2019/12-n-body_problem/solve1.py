# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from itertools import permutations
from typing import List


@dataclass
class Vector:
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self) -> str:
        return f"<x={self.x}, y={self.y}, z={self.z}>"

    @classmethod
    def parse(cls, text: str):
        # <x=-1, y=0, z=2>
        parts: List[str] = text[1:-1].split()
        x = int(parts[0][2:-1])
        y = int(parts[1][2:-1])
        z = int(parts[2][2:])
        return Vector(x=x, y=y, z=z)

    def energy(self) -> int:
        return sum([abs(self.x), abs(self.y), abs(self.z)])


@dataclass
class Moon:
    pos: Vector = Vector()
    vel: Vector = Vector()

    def __str__(self) -> str:
        return f"pos={self.pos}, vel={self.vel}"

    @classmethod
    def parse(cls, text: str):
        return Moon(pos=Vector.parse(text), vel=Vector())

    def apply_gravity(self, other) -> None:
        if other.pos.x > self.pos.x:
            self.vel.x += 1
        elif self.pos.x != other.pos.x:
            self.vel.x -= 1

        if other.pos.y > self.pos.y:
            self.vel.y += 1
        elif self.pos.y != other.pos.y:
            self.vel.y -= 1

        if other.pos.z > self.pos.z:
            self.vel.z += 1
        elif self.pos.z != other.pos.z:
            self.vel.z -= 1

    def apply_velocity(self) -> None:
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def kinetic_energy(self) -> int:
        return self.vel.energy()

    def potential_energy(self) -> int:
        return self.pos.energy()

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()


def apply_gravity(moons: List[Moon]) -> None:
    for left, right in permutations(moons, 2):
        left.apply_gravity(right)


def apply_velocity(moons: List[Moon]) -> None:
    for moon in moons:
        moon.apply_velocity()


def print_step(step: int, moons: List[Moon]) -> None:
    print(f"After {step} steps:")
    for moon in moons:
        print(moon)
    print("")


def print_system_energy(step: int, moons: List[Moon]) -> None:
    print(f"Energy after {step} steps:")
    energy: List[int] = []
    total_energy: int = 0
    for moon in moons:
        energy.append(moon.total_energy())
        total_energy += moon.total_energy()
        print(
            (
                f"pot: {abs(moon.pos.x)} + {abs(moon.pos.y)} + {abs(moon.pos.z)} = "
                f"{moon.potential_energy()};   "
                f"kin: {abs(moon.vel.x)} + {abs(moon.vel.y)} + {abs(moon.vel.z)} = "
                f"{moon.kinetic_energy()};   "
                f"total: {moon.potential_energy()} * {moon.kinetic_energy()} = "
                f"{moon.total_energy()}"
            )
        )
    sums: str = " + ".join(map(str, energy))
    print(f"Sum of total energy: {sums} = {total_energy}")


def system_energy(moons: List[Moon]) -> int:
    total_energy: int = 0
    for moon in moons:
        total_energy += moon.total_energy()
    return total_energy


def solve(moons: List[Moon], steps: int, trace: int) -> int:
    for step in range(steps):
        if trace and not (step % trace):
            print_step(step, moons)
        apply_gravity(moons)
        apply_velocity(moons)
    if trace:
        print_step(steps, moons)
        print_system_energy(steps, moons)

    return system_energy(moons)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 12 - The N-Body Problem (Part 1)."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "steps",
        type=int,
        default=1000,
        nargs="?",
        help="The number of simulation steps to run.  (Default %(default)s)",
    )
    parser.add_argument(
        "trace",
        type=int,
        default=0,
        nargs="?",
        help="Number of steps between traces.  0=No Trace  (Default %(default)s)",
    )
    args = parser.parse_args()

    moons: List[Moon] = []
    with open(args.input) as inf:
        for line in inf:
            moons.append(Moon.parse(line.strip()))

    try:
        print(solve(moons, args.steps, args.trace))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
