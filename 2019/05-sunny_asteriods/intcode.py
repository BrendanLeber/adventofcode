# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Tuple


class Intcode:
    opcodes: Dict[int, Tuple[str, int]] = {
        1: ("add", 3),
        2: ("multiply", 3),
        3: ("input", 1),
        4: ("output", 1),
        5: ("jump-if-true", 2),
        6: ("jump-if-false", 2),
        7: ("less-than", 3),
        8: ("equals", 3),
        99: ("halt", 0),
    }

    def __init__(self, program: List[int]) -> None:
        self.ip: int = 0
        self.program: List[int] = program[:]
        self.tape: List[int] = []
        self.last_output: Optional[int] = None
        self.last_input: Optional[int] = None

    def decode(self, opcode: int) -> Tuple[int, int, int, int]:
        """Decode the opcode and the parameter mode for up to three parameters."""
        op: int = opcode % 100
        pm1: int = (opcode // 100) % 10
        pm2: int = (opcode // 1000) % 10
        pm3: int = (opcode // 10000) % 10
        return (op, pm1, pm2, pm3)

    def execute(self, noun: Optional[int] = None, verb: Optional[int] = None) -> Optional[int]:
        self.tape = self.program[:]
        if noun:
            self.tape[1] = noun
        if verb:
            self.tape[2] = verb
        self.ip = 0

        while self.ip < len(self.tape):
            op, pm1, pm2, pm3 = self.decode(self.tape[self.ip])
            if op not in self.opcodes.keys():
                raise ValueError(f"unknown instruction {op} {self.tape[self.ip]}")
            elif op == 99:
                return self.tape[0]
            elif op == 1:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                c = self.tape[self.ip + 3]
                self.tape[c] = a + b
                self.ip += 1 + self.opcodes[op][1]
            elif op == 2:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                c = self.tape[self.ip + 3]
                self.tape[c] = a * b
                self.ip += 1 + self.opcodes[op][1]
            elif op == 3:
                c = self.tape[self.ip + 1]
                self.tape[c] = int(input("input: "))
                self.last_input = self.tape[c]
                self.ip += 1 + self.opcodes[op][1]
            elif op == 4:
                self.last_output = self.parameter(1, pm1)
                print(self.last_output)
                self.ip += 1 + self.opcodes[op][1]
            elif op == 5:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                self.ip = b if a else self.ip + 1 + self.opcodes[op][1]
            elif op == 6:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                self.ip = b if not a else self.ip + 1 + self.opcodes[op][1]
            elif op == 7:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                c = self.tape[self.ip + 3]
                self.tape[c] = 1 if a < b else 0
                self.ip += 1 + self.opcodes[op][1]
            elif op == 8:
                a = self.parameter(1, pm1)
                b = self.parameter(2, pm2)
                c = self.tape[self.ip + 3]
                self.tape[c] = 1 if a == b else 0
                self.ip += 1 + self.opcodes[op][1]
            else:
                raise ValueError(f"blue moon error for op {op}")
        return None

    def parameter(self, parameter: int, mode: int) -> int:
        """Parse an parameter that is in position (0) or immediate (1) mode."""
        value: int = self.tape[self.ip + parameter]
        if mode == 0:
            return self.tape[value]
        elif mode == 1:
            return value
        else:
            raise ValueError(f"unknown parameter mode {mode}")
