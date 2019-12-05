# -*- coding: utf-8 -*-

from enum import IntEnum
from typing import Dict, List, NamedTuple, Optional, Tuple


class ParameterMode(IntEnum):
    POSITIONAL = 0
    IMMEDIATE = 1


class ParameterType(IntEnum):
    READ = 0
    WRITE = 1


class InstructionInfo(NamedTuple):
    name: str
    params: Tuple[ParameterType, ...]


INSTRUCTIONS: Dict[int, InstructionInfo] = {
    1: InstructionInfo("add", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    2: InstructionInfo("multiply", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    3: InstructionInfo("input", (ParameterType.WRITE,)),
    4: InstructionInfo("output", (ParameterType.READ,)),
    5: InstructionInfo("jump-if-true", (ParameterType.READ, ParameterType.READ)),
    6: InstructionInfo("jump-if-false", (ParameterType.READ, ParameterType.READ)),
    7: InstructionInfo("less-than", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    8: InstructionInfo("equals", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    99: InstructionInfo("halt", tuple()),
}


class Intcode:
    def __init__(self, program: List[int]) -> None:
        self.ip: int = 0
        self.program: List[int] = program[:]
        self.tape: List[int] = []
        self.last_output: Optional[int] = None
        self.last_input: Optional[int] = None

    def decode_instruction(self) -> Tuple[int, List[int]]:
        """Decode the opcode and the arguments for this instruction."""
        opcode: int = self.tape[self.ip] % 100
        arguments: List[int] = []
        mask: int = 10
        # start at 1 to skip the opcode in the instruction
        for param_num, param_type in enumerate(INSTRUCTIONS[opcode].params, 1):
            mask *= 10
            param_mode: ParameterMode = ParameterMode((self.tape[self.ip] // mask) % 10)
            if param_type == ParameterType.WRITE:
                arguments.append(self.tape[self.ip + param_num])
            elif param_mode == ParameterMode.POSITIONAL:
                position = self.tape[self.ip + param_num]
                arguments.append(self.tape[position])
            elif param_mode == ParameterMode.IMMEDIATE:
                arguments.append(self.tape[self.ip + param_num])
            else:
                raise TypeError(f"unknown parameter mode {param_mode}")
        return (opcode, arguments)

    def execute(self) -> int:
        """Execute the instructions contained in the VM memory."""
        while self.ip < len(self.tape):
            opcode, params = self.decode_instruction()
            if opcode == 1:
                self.tape[params[2]] = params[0] + params[1]
                self.ip += 1 + len(params)
            elif opcode == 2:
                self.tape[params[2]] = params[0] * params[1]
                self.ip += 1 + len(params)
            elif opcode == 3:
                self.tape[params[0]] = int(input("input: "))
                self.last_input = self.tape[params[0]]
                self.ip += 1 + len(params)
            elif opcode == 4:
                self.last_output = params[0]
                print(self.last_output)
                self.ip += 1 + len(params)
            elif opcode == 5:
                self.ip = params[1] if params[0] else self.ip + 1 + len(params)
            elif opcode == 6:
                self.ip = params[1] if not params[0] else self.ip + 1 + len(params)
            elif opcode == 7:
                self.tape[params[2]] = 1 if params[0] < params[1] else 0
                self.ip += 1 + len(params)
            elif opcode == 8:
                self.tape[params[2]] = 1 if params[0] == params[1] else 0
                self.ip += 1 + len(params)
            elif opcode == 99:
                return self.tape[0]
        raise EOFError("reached end of tape without finding halt instruction.")

    def reset(self) -> None:
        """Reset the VM state before starting a new execution."""
        self.tape = self.program[:]
        self.ip = 0

    def set_noun_and_verb(self, noun: int, verb: int) -> None:
        """Set the noun and verb to initialize the program."""
        self.tape[1] = noun
        self.tape[2] = verb
