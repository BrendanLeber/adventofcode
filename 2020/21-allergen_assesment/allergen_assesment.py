# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 21 - Allergen Assesment."""

import argparse
import pdb
import traceback
from re import match


def parse_puzzle(lines: list[str]):
    puzzle: list[tuple[list[str], list[str]]] = []
    for line in lines:
        m = match(r"^([^(]+)\(contains ([^)]+)\)$", line)
        ingredients = m[1].strip().split()
        allergens = m[2].strip().split(", ")
        puzzle.append((ingredients, allergens))
    return puzzle


def part_one(puzzle):
    all_ingredients: set[str] = set()
    all_allergens: set[str] = set()
    allergen_ingredient_map: dict[str, set[str]] = {}
    for ingredients, allergens in puzzle:
        all_ingredients.update(ingredients)
        all_allergens.update(allergens)
        for allergen in allergens:
            new_ingredients = allergen_ingredient_map.get(allergen, set())
            new_ingredients.update(ingredients)
            allergen_ingredient_map[allergen] = new_ingredients

    remaining_ingredients = all_ingredients.copy()
    for allergen, ingredients in allergen_ingredient_map.items():
        remaining_ingredients.difference_update(ingredients)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 21 - Allergen Assesment."
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
        with open(args.input, "rt") as inf:
            lines = inf.readlines()
        puzzle = parse_puzzle(lines)
        print(part_one(puzzle))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
