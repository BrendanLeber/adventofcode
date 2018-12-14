#!/usr/bin/env python


from dataclasses import dataclass
import fileinput
import re

import numpy as np


@dataclass
class Particle:
    """A particle in 2-dimensional space."""

    x: int = 0
    y: int = 0
    delta_x: int = 0
    delta_y: int = 0

    def update(self):
        """Update the location of the partical by its vector."""
        self.x += self.delta_x
        self.y += self.delta_y

    def inverse_update(self):
        """Update the location of the partical by its reversed vector."""
        self.x -= self.delta_x
        self.y -= self.delta_y


@dataclass
class Rect:
    """A rectangle in 2-dimensional space."""

    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def width(self):
        return abs(self.right - self.left)

    def height(self):
        return abs(self.bottom - self.top)

    @classmethod
    def enclose_all(cls, particles):
        rc = Rect()
        for particle in particles:
            rc.left = min(rc.left, particle.x)
            rc.right = max(rc.right, particle.x)
            rc.top = min(rc.top, particle.y)
            rc.bottom = max(rc.bottom, particle.y)
        return rc


def display_world(iteration, particles):
    area = Rect.enclose_all(particles)
    offset_x = -area.left
    offset_y = -area.top

    grid = np.zeros([area.height() + 1, area.width() + 1], dtype=int)
    for particle in particles:
        grid[particle.y + offset_y, particle.x + offset_x] = 1

    with open(f"stars_{iteration:05d}.pbm", "w") as of:
        of.write(f"P1\n{area.width() + 1} {area.height() + 1}\n")
        for row in grid:
            of.write(" ".join(map(str, row)))
            of.write("\n")
            of.flush()


def part_one(particles):
    # area = Rect.enclose_all(particles)
    # print(f"{len(particles)}  {area.width()} x {area.height()}")

    iteration = 0
    while True:
        iteration += 1

        old_area = Rect.enclose_all(particles)
        for particle in particles:
            particle.update()
        new_area = Rect.enclose_all(particles)

        if old_area.width() * old_area.height() <= new_area.width() * new_area.height():
            # print(f"{iteration}: {old_area.width()} x {old_area.height()} -> {new_area.width()} x {new_area.height()}")
            for particle in particles:
                particle.inverse_update()
            display_world(iteration - 1, particles)
            break

    return iteration - 1


if __name__ == "__main__":
    EXTRACT = re.compile(
        r"^position=<\s*(?P<x>[-0-9]+),\s*(?P<y>[-0-9]+)>\s*velocity=<\s*(?P<dx>[-0-9]+),\s*(?P<dy>[-0-9]+)>$"
    )

    particles = []
    for line in fileinput.input():
        m = EXTRACT.search(line.strip())
        if not m:
            raise TypeError(f"input line does not match expected format: '{line}'")
        particles.append(
            Particle(int(m.group("x")), int(m.group("y")), int(m.group("dx")), int(m.group("dy")))
        )

    print(part_one(particles))
