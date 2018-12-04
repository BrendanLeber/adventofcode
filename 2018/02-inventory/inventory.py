#!/usr/bin/env python


from collections import Counter
import fileinput


def part_one(package_ids: list) -> int:
    match_two = 0
    match_three = 0
    for package_id in package_ids:
        counts = [count for _,count in Counter(package_id).most_common()]
        if 2 in counts:
            match_two += 1
        if 3 in counts:
            match_three += 1
    return match_two * match_three


#def levenshtein_distance(s1: str, s2: str) -> int:
#    if len(s1) > len(s2):
#        s1, s2 = s2, s1
#    distances = range(len(s1) + 1)
#    for i2, c2 in enumerate(s2):
#        distances_ = [i2 + 1]
#        for i1, c1 in enumerate(s1):
#            if c1 == c2:
#                distances_.append(distances[i1])
#            else:
#                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
#        distances = distances_
#    return distances[-1]


#def part_two(package_ids: list) -> str:
#    for first in package_ids:
#        for second in package_ids:
#            if levenshtein_distance(first, second) == 1:
#                for pos in range(len(first)):
#                    if first[pos] != second[pos]:
#                        return first[0:pos] + first[pos + 1:]
#    return None


def part_two(package_ids: list) -> str:
    for first in package_ids:
        for second in package_ids:
            matches = []
            for pos in range(0, len(first)):
                if first[pos] == second[pos]:
                    matches.append(first[pos])
            if len(matches) == len(first) - 1:
                return "".join(matches)
    return None


if __name__ == "__main__":
    package_ids = []
    for line in fileinput.input():
        package_ids.append(line.strip())

    print(part_one(package_ids))
    print(part_two(package_ids))
