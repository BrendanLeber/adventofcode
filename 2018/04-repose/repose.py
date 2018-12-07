#!/usr/bin/env python


from collections import defaultdict
import fileinput


def argmax(d, guard_id):
    best = None
    for k, v in d.items():
        if best is None or (k[0] == guard_id and v > d[best]):
            best = k
    return best


def parse_time(line: str) -> int:
    words = line.split()
    date, time = words[0][1:], words[1][:-1]
    return int(time.split(":")[1])


def part_one(records: list) -> int:
    total_asleep = defaultdict(int)
    minutes_asleep = defaultdict(int)
    guard = None
    asleep = None

    for record in records:
        time = parse_time(record)
        if "begins shift" in record:
            guard = int(record.split()[3][1:])
            asleep = None
        elif "falls asleep" in record:
            asleep = time
        elif "wakes up" in record:
            for minute in range(asleep, time):
                minutes_asleep[(guard, minute)] += 1
                total_asleep[guard] += 1

    max_guard = max(total_asleep, key=total_asleep.get)
    guard, minutes = argmax(minutes_asleep, max_guard)
    return guard * minutes


if __name__ == "__main__":
    records = []
    for line in fileinput.input():
        records.append(line.strip())
    records.sort()

    print(part_one(records))
