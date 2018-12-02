#!/usr/bin/env python


import fileinput


def has_exactly_three(value: str) -> bool:
    char_counts = {}
    for char in value:
        count = char_counts.get(char, 0) + 1
        char_counts[char] = count
    for (char, count) in char_counts.items():
        if count == 3:
            return True
    return False


def has_exactly_two(value: str) -> bool:
    char_counts = {}
    for char in value:
        count = char_counts.get(char, 0) + 1
        char_counts[char] = count
    for (char, count) in char_counts.items():
        if count == 2:
            return True
    return False


def part_one(package_ids: list) -> int:
    match_two = 0
    match_three = 0
    for package_id in package_ids:
        if has_exactly_two(package_id):
            match_two += 1
        if has_exactly_three(package_id):
            match_three += 1
    return match_two * match_three


def part_two(package_ids: list) -> str:
    slots = [0 for _ in range(len(package_ids[0]))]
    for first in range(len(package_ids)):
        for second in range(first + 1, len(package_ids)):
            for pos in range(len(package_ids[first])):
                if package_ids[first][pos] != package_ids[second][pos]:
                    slots[pos] = 1
                else:
                    slots[pos] = 0
            if sum(slots) == 1:
                for slot in range(len(slots)):
                    if slots[slot] == 1:
                        result = package_ids[first][0:slot] + package_ids[first][slot + 1 :]
                        return result
    return None


if __name__ == "__main__":
    package_ids = []
    for line in fileinput.input():
        package_ids.append(line.strip())

    print(part_one(package_ids))
    print(part_two(package_ids))
