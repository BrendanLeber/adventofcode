# -*- coding: utf-8 -*-
"""Advent of Code - Download input.txt for a given day."""

from __future__ import annotations

import argparse
import contextlib
import pdb
import time
import traceback
import urllib.error
import urllib.request
from typing import Generator


@contextlib.contextmanager
def timing(name: str = "") -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = "ms"
        if t < 100:
            t *= 1000
            unit = "μs"
        if name:
            name = f" ({name})"
        print(f"> {int(t)} {unit}{name}")


def get_input(year: int, day: int) -> str:
    with open(".env") as f:
        contents = f.read()

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = urllib.request.Request(url, headers={"Cookie": contents.strip()})
    return urllib.request.urlopen(req).read().decode()


def download_input(year: int, day: int) -> int:
    for i in range(5):
        try:
            s = get_input(year, day)
        except urllib.error.URLError as e:
            print(f"zzz: not ready yet: {e}")
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit("timed out after attempting many times")

    with open("input.txt", "w") as f:
        f.write(s)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - Download input.txt for a given day."
    )
    parser.add_argument(
        "year",
        type=int,
        help="The year to download.",
    )
    parser.add_argument(
        "day",
        type=int,
        help="The day to download.",
    )
    args = parser.parse_args()

    try:
        download_input(args.year, args.day)
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
