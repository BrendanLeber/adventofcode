# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Optional, Set, Tuple


class PlanetNode:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.parent = None
        self.children = []  # type: ignore

    def __repr__(self) -> str:
        parent_name = f"'{self.parent.name}'" if self.parent else "None"  # type: ignore
        child_names = ", ".join([f"'{child.name}'" for child in self.children])
        return f"PlanetNode(name='{self.name}', parent={parent_name} children=[{child_names}])"

    def __lt__(self, other) -> bool:
        return self.name < other.name

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def add_child(self, child) -> None:
        self.children.append(child)

    def count_orbits(self, parent_orbits) -> int:
        return parent_orbits + sum([c.count_orbits(parent_orbits + 1) for c in self.children])

    def find(self, name: str):
        if self.name == name:
            return self
        for child in self.children:
            found = child.find(name)
            if found:
                return found
        return None

    def get_path(self, name: str, path) -> bool:
        if self.name == name:
            path.append(self)
            return True
        elif not self.children:
            return False
        founds = []
        for child in self.children:
            found = child.get_path(name, path)
            founds.append(found)
        if any(founds):
            path.append(self)
            return True
        return False


def binary_contains(sequence: List[PlanetNode], key: str) -> bool:
    """Return True if the key exists in the sequence, False otherwise.  (Binary Search)"""
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid].name < key:
            low = mid + 1
        elif sequence[mid].name > key:
            high = mid - 1
        else:
            return True
    return False


def binary_index(sequence: List[PlanetNode], key: str) -> Optional[int]:
    """Return the index of the key node or None if it doesn't exist.  (Binary Search)"""
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sequence[mid].name < key:
            low = mid + 1
        elif sequence[mid].name > key:
            high = mid - 1
        else:
            return mid
    return None


def find_first_common_node(
    lh_path: List[PlanetNode], rh_path: List[PlanetNode]
) -> Optional[PlanetNode]:
    """Find the first node in common between two paths."""
    for lh_node in lh_path:
        for rh_node in rh_path:
            if lh_node == rh_node:
                return lh_node
    return None


def unique_planets(orbits: List[Tuple[str, str]]) -> Set[str]:
    """Get the unique list of planets from all of the orbits."""
    planets: Set[str] = set()
    planets.update([x[0] for x in orbits])
    planets.update([x[1] for x in orbits])
    return planets


def solve(orbits: List[Tuple[str, str]]) -> Tuple[Optional[int], Optional[int]]:
    # create nodes for every possible planet
    planets: List[PlanetNode] = []
    for planet in unique_planets(orbits):
        planets.append(PlanetNode(planet))
    planets.sort()

    # create the root of our orbit tree (s/b COM at the root)
    com_id = binary_index(planets, "COM")
    root: PlanetNode = planets[com_id]  # type: ignore

    # add the rest of the planets to the orbit tree
    for planet, child in orbits:
        pid = binary_index(planets, planet)
        cid = binary_index(planets, child)
        planets[pid].add_child(planets[cid])  # type: ignore
        planets[cid].parent = planets[pid]  # type: ignore

    # count the total number of direct and indirect orbits
    one: Optional[int] = root.count_orbits(0)

    # find path from root to 'YOU' node
    you_path: List[PlanetNode] = []
    you_found = root.get_path("YOU", you_path)
    if not you_found:
        raise ValueError("no path found to 'YOU' node.")

    # find path from root to 'SAN' node
    san_path: List[PlanetNode] = []
    san_found = root.get_path("SAN", san_path)
    if not san_found:
        raise ValueError("no path found to 'SAN' node.")

    # find the first node in common between 'YOU' and 'SAN'
    common_node = find_first_common_node(you_path, san_path)
    if not common_node:
        raise ValueError("no common node found between 'YOU' and 'SAN'.")

    # calculate the distance between the common node and the 'YOU' node
    you_distance = 0
    for node in you_path[1:]:  # don't count ourself
        if node == common_node:
            break
        you_distance += 1

    # calculate the distance between the common node and the 'SAN' node
    san_distance = 0
    for node in san_path[1:]:  # don't count ourself
        if node == common_node:
            break
        san_distance += 1

    two: Optional[int] = you_distance + san_distance

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 6 - Universal Orbit Map."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    orbits: List[Tuple[str, str]] = []
    with open(args.input) as inf:
        for line in inf:
            orbits.append(tuple(line.strip().split(")")))  # type: ignore

    try:
        print(solve(orbits))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
