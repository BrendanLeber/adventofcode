# -*- coding: utf-8 -*-

from re import findall
from typing import List


def extract_ints(line: str) -> List[int]:
    return [int(x) for x in findall(r"-?\d+", line)]
