# -*- coding: utf-8 -*-

import argparse
import pdb
import re
import traceback
from typing import List, Tuple

Room = Tuple[str, int, str]


def decrypt_name(encrypted_name: str, sector_id: int) -> str:
    decrypted_name: List[str] = []
    for ch in encrypted_name:
        if ch == "-":
            decrypted_name.append(" ")
        else:
            value: int = ord(ch) - ord("a")
            value = (value + sector_id) % 26
            decrypted_name.append(chr(value + ord("a")))

    return "".join(decrypted_name)


def get_frequencies(encrypted_name: str) -> List[Tuple[str, int]]:
    counts: List[int] = [0] * 26
    for ch in encrypted_name:
        counts[ord(ch) - ord("a")] += 1

    freqs: List[Tuple[str, int]] = []
    for idx in range(26):
        if counts[idx] > 0:
            freqs.append((chr(ord("a") + idx), counts[idx]))

    freqs.sort(key=lambda x: x[0])
    freqs.sort(key=lambda x: x[1], reverse=True)

    return freqs


def is_real_room(room: Room) -> bool:
    encrypted_name, _, checksum = room
    encrypted_name = encrypted_name.replace("-", "")
    freqs: List[Tuple[str, int]] = get_frequencies(encrypted_name)
    for idx, ch in enumerate(checksum):
        if freqs[idx][0] != ch:
            return False
    return True


def solve(rooms: List[Room], verbose=False) -> Tuple[int, int]:
    one: int = 0
    two: int = 0
    for room in rooms:
        if is_real_room(room):
            if verbose:
                print(f"{room} is a real room.")
            one += room[1]
            encrypted_name, sector_id, _ = room
            decrypted_name: str = decrypt_name(encrypted_name[:-1], sector_id)
            if verbose:
                print(f"room: '{decrypted_name}'  sector_id: {sector_id}")
            if decrypted_name == "northpole object storage":
                two = sector_id
        else:
            if verbose:
                print(f"{room} is *not* a real room.")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 4 - Security Through Obscurity."
    )
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

    matcher = re.compile(r"^(?P<name>\D+)(?P<sector>\d+)\[(?P<check>[a-z]+)\]$", re.X)

    rooms: List[Room] = []
    with open(args.input) as inf:
        for line in inf:
            match = matcher.match(line.strip())
            if not match:
                raise ValueError(f"invalid room.  '{line.strip()}'")
            rooms.append((match["name"], int(match["sector"]), match["check"]))

    try:
        print(solve(rooms, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
