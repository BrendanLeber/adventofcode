#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import pdb
import traceback


def mlen(string):
    start = 1
    end = len(string) - 1
    result = 0
    pos = start
    while pos < end:
        if string[pos] != "\\":
            pos += 1
            result += 1
        elif string[pos + 1] in ["\\", '"']:
            pos += 2
            result += 1
        else:
            pos += 4
            result += 1
    return result


def elen(string):
    result = 2
    for ch in string:
        if ch not in ["\\", '"']:
            result += 1
        else:
            result += 2
    return result


def solve(strings):
    totals = list(map(len, strings))
    mtotals = list(map(mlen, strings))
    etotals = list(map(elen, strings))
    return (sum(totals) - sum(mtotals), sum(etotals) - sum(totals))


if __name__ == "__main__":
    try:
        lines = []
        for line in fileinput.input():
            lines.append(line.strip())
        print(solve(lines))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
