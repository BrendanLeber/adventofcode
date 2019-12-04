# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import Dict, List, Optional, Set, Tuple

VERBOSE: bool = False


Vertex = Tuple[str, int]  # direction, distance
Path = List[Vertex]

Point = Tuple[int, int]  # column, row
Segment = Tuple[Point, Point]  # start, end
Line = List[Segment]

PointDistances = Dict[Point, int]


def sign(x) -> int:
    """Return the sign of the argument.  [-1, 0, 1]"""
    return x and (1, -1)[x < 0]


def is_vertical(segment: Segment) -> bool:
    """Return true if the segment represents a vertical segment."""
    return segment[0][0] == segment[1][0]


def is_horizontal(segment: Segment) -> bool:
    """Return true if the semgent represents a horizontal segment."""
    return segment[0][1] == segment[1][1]


def path_to_line(origin: Point, path: Path) -> Line:
    """Convert a path into a line comprised of segments."""
    line: Line = []
    end: Point = origin
    for direction, distance in path:
        start: Point = end
        if direction == "U":
            end = (start[0], start[1] + distance)
        elif direction == "D":
            end = (start[0], start[1] - distance)
        elif direction == "R":
            end = (start[0] + distance, start[1])
        elif direction == "L":
            end = (start[0] - distance, start[1])
        else:
            raise ValueError(f"unknown direction '{direction}'")
        line.append((start, end))
    return line


def path_to_pt_dist(origin: Point, path: Path) -> PointDistances:
    """Convert a path into a dictionary of points and distances."""
    pt: Point = origin
    dx: int = 0
    dy: int = 0
    length: int = 0

    result: PointDistances = {}
    for direction, distance in path:
        if direction == "U":
            dx, dy = 0, 1
        elif direction == "D":
            dx, dy = 0, -1
        elif direction == "R":
            dx, dy = 1, 0
        elif direction == "L":
            dx, dy = -1, 0
        else:
            raise ValueError(f"unknown direction '{direction}'")
        for _ in range(distance):
            pt = (pt[0] + dx, pt[1] + dy)
            length += 1
            if pt not in result:
                result[pt] = length
    return result


def lines_intersect(l12: Segment, l34: Segment) -> Optional[Point]:
    """Return the point where the two lines intersect."""
    ((x1, y1), (x2, y2)) = l12
    ((x3, y3), (x4, y4)) = l34

    # compute a1, b1, c1 where the line joining points 1 and 2 is
    # a1 * x + b1 * y + c1 = 0
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = x2 * y1 - x1 * y2

    # compute r3 and r4
    r3 = a1 * x3 + b1 * y3 + c1
    r4 = a1 * x4 + b1 * y4 + c1

    # check signs of r3 and r4.  if both point 3 and point 4 lie on
    # the same side of line 1, the line segments do not intersect.
    if r3 != 0 and r4 != 0 and (sign(r3) == sign(r4)):
        return None

    # compute a2, b2, c2
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = x4 * y3 - x3 * y4

    # compute r1 and r2
    r1 = a2 * x1 + b2 * y1 + c2
    r2 = a2 * x2 + b2 * y2 + c2

    # check signs of r1 and r2.  if both point 1 and point 2 lie
    # on the same side of the second line segment, the line segments
    # do not intersect.
    if r1 != 0 and r2 != 0 and (sign(r1) == sign(r2)):
        return None

    # line segments intersect.  compute intersection point
    denom = a1 * b2 - a2 * b1
    if denom == 0:
        return None  # collinear
    if denom < 0:
        offset = -denom / 2
    else:
        offset = denom / 2

    num = b1 * c2 - b2 * c1
    if num < 0:
        x = num - offset
    else:
        x = num + offset
    x = x / denom

    num = a2 * c1 - a1 * c2
    if num < 0:
        y = num - offset
    else:
        y = num + offset
    y = y / denom

    return (int(x), int(y))


def manhattan_distance(a: Point, b: Point) -> int:
    """Return the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(paths: List[Path]) -> Tuple[int, int]:
    origin: Point = (0, 0)

    # convert the list of paths into a list of lines
    lines: List[Line] = []
    for path in paths:
        lines.append(path_to_line(origin, path))

    # get the intersections between the first line and the other lines
    intersections: Set[Point] = set()
    for line in lines[1:]:
        for lh in lines[0]:
            for rv in line:
                pt: Optional[Point] = lines_intersect(lh, rv)
                if pt and pt != origin:
                    intersections.add(pt)

    # get the manhattan distance of the point closest to the origin
    one: int = min([manhattan_distance(origin, pt) for pt in intersections])

    # TODO this assumes there are only two paths provided
    # get the point & distance for each point in path A & B
    pts_a = path_to_pt_dist(origin, paths[0])
    pts_b = path_to_pt_dist(origin, paths[1])

    # get the unique points from both paths
    both: Set[Point] = set(pts_a.keys()) & set(pts_b.keys())

    # get the shortest path to the closest intersection
    two: int = min([pts_a[pt] + pts_b[pt] for pt in both])

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 3 - Crossed Wires.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    paths: List[Path] = []
    with open(args.input) as inf:
        for text in inf:
            path: Path = []
            segments = text.strip().split(",")
            for segment in segments:
                path.append((segment[0], int(segment[1:])))
            paths.append(path)
    try:
        print(solve(paths))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
