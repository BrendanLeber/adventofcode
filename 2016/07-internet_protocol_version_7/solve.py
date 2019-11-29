# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Set, Tuple


class IPAddress:
    def __init__(self, addr: str):
        self.addr: str = addr
        self.supernets: List[str] = []
        self.hypernets: List[str] = []

        while addr:
            if addr[0] == "[":
                # start of a hypernet segment - remove the '['
                addr = addr[1:]

                # find the end of the segment (']')
                pos: int = addr.find("]")
                if pos == -1:
                    raise ValueError("malformed hypernet segment")

                # save this hypernet segment to the current address
                segment = addr[:pos]
                self.hypernets.append(segment)

                # remove this hypernet segment from the temp string
                addr = addr[pos + 1:]
            else:
                # find the next hypernet segment (or the end)
                pos = addr.find("[")
                if pos == -1:
                    self.supernets.append(addr)
                    addr = addr[:pos + 1]
                else:
                    segment = addr[0:pos]
                    self.supernets.append(segment)
                    addr = addr[pos:]

    def __repr__(self) -> str:
        return (
            f"IPAddress(addr={self.addr}, supernets={self.supernets}, hypernets={self.hypernets})"
        )

    def abas_to_babs(self, abas: List[str]) -> List[str]:
        babs: List[str] = []
        for aba in abas:
            babs.append(aba[1] + aba[0] + aba[1])
        return babs

    def get_abas(self) -> List[str]:
        abas: Set[str] = set()
        for segment in self.supernets:
            end = len(segment) - 2
            for pos in range(end):
                if segment[pos] != segment[pos + 2]:
                    continue

                if segment[pos] != segment[pos + 1]:
                    abas.add(segment[pos:pos + 3])

        return list(abas)

    def has_abba(self, segment: str) -> bool:
        for pos in range(0, len(segment) - 3):
            if segment[pos] != segment[pos + 3]:
                continue
            if segment[pos + 1] == segment[pos + 2] and segment[pos] != segment[pos + 1]:
                return True

        return False

    def supports_ssl(self) -> bool:
        abas: List[str] = self.get_abas()
        babs: List[str] = self.abas_to_babs(abas)
        for hypernet in self.hypernets:
            for bab in babs:
                if hypernet.find(bab) != -1:
                    return True
        return False

    def supports_tls(self) -> bool:
        in_super: bool = False
        for supernet in self.supernets:
            if self.has_abba(supernet):
                in_super = True
                break

        in_hyper: bool = False
        for hypernet in self.hypernets:
            if self.has_abba(hypernet):
                in_hyper = True
                break

        return in_super and not in_hyper


def solve(addrs: List[IPAddress], verbose=False) -> Tuple[int, int]:
    one: int = 0
    two: int = 0
    for addr in addrs:
        if addr.supports_tls():
            one += 1
        if addr.supports_ssl():
            two += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 7 - Internet Protocol Version 7."
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

    addrs: List[IPAddress] = []
    with open(args.input) as inf:
        for line in inf:
            addrs.append(IPAddress(line.strip()))

    try:
        print(solve(addrs, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
