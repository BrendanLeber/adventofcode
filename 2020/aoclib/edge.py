# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Edge:
    u: int  # the "from" vertex
    v: int  # the "to" vertex

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)
