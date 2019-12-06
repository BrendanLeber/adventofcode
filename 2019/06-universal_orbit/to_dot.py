# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import Dict, List, Set, Tuple


def unique_planets(orbits: List[Tuple[str, str]]) -> Set[str]:
    """Get the unique list of planets from all of the orbits."""
    planets: Set[str] = set()
    planets.update([x[0] for x in orbits])
    planets.update([x[1] for x in orbits])
    return planets


def to_dot(orbits: List[Tuple[str, str]]) -> None:
    print("digraph {")

    planets = unique_planets(orbits)
    planet_nodes: Dict[str, str] = {}
    for planet in planets:
        node = f"node_{planet}"
        planet_nodes[planet] = node
        print(f'    {node} [label = "{planet}"];')
    print("")

    for planet, child in orbits:
        print(f"    {planet_nodes[planet]} -> {planet_nodes[child]};")

    print("}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 6 - Universal Orbit Map - To Dot."
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
        to_dot(orbits)
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
