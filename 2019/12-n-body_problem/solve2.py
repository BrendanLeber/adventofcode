# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from typing import List, Set


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
    for left in moons:
        for right in moons:
            if left is right:
                continue
            left.apply_gravity(right)


def apply_velocity(moons: List[Moon]) -> None:
    for moon in moons:
        moon.apply_velocity()


def lcm(xs: List[int]) -> int:
    primes_per_dimension: List[List[int]] = [prime_factors(x) for x in xs]
    all_primes: Set[int] = set([prime for primes in primes_per_dimension for prime in primes])
    result: int = 1
    for prime in all_primes:
        amount = max(primes_per_dimension[dim].count(prime) for dim in range(len(xs)))
        result *= prime ** amount
    return result


def prime_factors(n: int) -> List[int]:
    factors: List[int] = []
    i: int = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def print_step(step: int, moons: List[Moon]) -> None:
    print(f"After {step} steps:")
    for moon in moons:
        print(moon)
    print("")


def solve(moons: List[Moon], trace: int) -> int:
    step: int = 0
    cycles: List[int] = [None, None, None]  # type: ignore
    while not all(cycles):
        if trace and not (step % trace):
            print_step(step, moons)
        apply_gravity(moons)
        apply_velocity(moons)
        step += 1
        if not cycles[0] and all([m.vel.x == 0 for m in moons]):
            cycles[0] = step
        if not cycles[1] and all([m.vel.y == 0 for m in moons]):
            cycles[1] = step
        if not cycles[2] and all([m.vel.z == 0 for m in moons]):
            cycles[2] = step

    print_step(step, moons)

    return lcm(cycles) * 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 12 - The N-Body Problem (Part Two)."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
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
        print(solve(moons, args.trace))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
