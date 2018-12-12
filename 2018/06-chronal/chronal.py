#!/usr/bin/env python


from dataclasses import dataclass
from operator import attrgetter, itemgetter
import fileinput


@dataclass
class Point:
    """A point in 2-dimensional space."""

    x: int = 0
    y: int = 0

    def offset(self, x_offset, y_offset):
        """Offset the point by the given values."""
        self.x += x_offset
        self.y += y_offset

    def manhattan_distance(self, other):
        """Return the Manhattan distance between this point an another."""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __sub__(self, rhs):
        """Return the difference of two points."""
        return Point(self.x - rhs.x, self.y - rhs.y)

    def __add__(self, rhs):
        """Return the sum of two points."""
        return Point(self.x + rhs.x, self.y + rhs.y)


def closest_point(loc: Point, points: list) -> int:
    distances = [loc.manhattan_distance(pt) for pt in points]
    min_distance = min(distances)
    min_distances = []
    for i, dist in enumerate(distances):
        if dist == min_distance:
            min_distances.append(i)
    if len(min_distances) == 1:
        return min_distances[0]
    return -1


def part_one(coords: list) -> int:
    max_x = max(coords, key=attrgetter("x")).x + 2
    max_y = max(coords, key=attrgetter("y")).y + 2

    infinites = set()
    grid = [[-1 for _ in range(max_x)] for _ in range(max_y)]
    for row in range(max_y):
        for col in range(max_x):
            grid[row][col] = closest_point(Point(row, col), coords)
            if row == 0 or col == 0 or row == (max_y - 1) or col == (max_x - 1):
                infinites.add(grid[row][col])

    areas = {}
    for pos, _ in enumerate(coords):
        if pos not in infinites:
            area_sum = 0
            for row in grid:
                for col in row:
                    if col == pos:
                        area_sum += 1
            areas[pos] = area_sum

    return max(areas.items(), key=itemgetter(1))[1]


def sum_distances(loc: Point, points: list) -> int:
    dsum = 0
    for pt in points:
        dsum += loc.manhattan_distance(pt)
    return dsum


def part_two(coords: list) -> int:
    max_x = max(coords, key=attrgetter("x")).x + 2
    max_y = max(coords, key=attrgetter("y")).y + 2

    grid = [[0 for _ in range(max_x)] for _ in range(max_y)]
    for row in range(max_y):
        for col in range(max_x):
            grid[row][col] = sum_distances(Point(row, col), coords)

    region_size = 0
    for row in grid:
        for col in row:
            if col < 10000:
                region_size += 1

    return region_size


if __name__ == "__main__":
    coordinates = []
    for line in fileinput.input():
        line = line.strip().replace(",", "").split()
        coordinates.append(Point(int(line[1]), int(line[0])))

    print(part_one(coordinates))
    print(part_two(coordinates))
