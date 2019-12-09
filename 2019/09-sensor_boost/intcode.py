# -*- coding: utf-8 -*-

import pdb
import sys
import traceback
from collections import deque
from enum import IntEnum
from typing import Deque, Dict, List, NamedTuple, Optional, Tuple, Union


class ParameterMode(IntEnum):
    POSITIONAL = 0
    IMMEDIATE = 1
    RELATIVE = 2


class ParameterType(IntEnum):
    READ = 0
    WRITE = 1


class InstructionInfo(NamedTuple):
    name: str
    params: Tuple[ParameterType, ...]


INSTRUCTIONS: Dict[int, InstructionInfo] = {
    1: InstructionInfo("add", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    2: InstructionInfo("mul", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    3: InstructionInfo("in", (ParameterType.WRITE,)),
    4: InstructionInfo("out", (ParameterType.READ,)),
    5: InstructionInfo("jnz", (ParameterType.READ, ParameterType.READ)),
    6: InstructionInfo("jz", (ParameterType.READ, ParameterType.READ)),
    7: InstructionInfo("lt", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    8: InstructionInfo("eq", (ParameterType.READ, ParameterType.READ, ParameterType.WRITE)),
    9: InstructionInfo("rbo", (ParameterType.READ,)),
    99: InstructionInfo("halt", tuple()),
}


class Intcode:
    def __init__(self, program: List[int]) -> None:
        self.ip: int = 0
        self.program: List[int] = program[:]
        self.tape: List[int] = program[:]
        # add extra memory space for data buffer
        self.tape += [0] * max(1024, len(self.program) * 3)
        self.relative_base: int = 0
        self.last_output: Optional[int] = None
        self.last_input: Optional[int] = None
        self.chained_mode: bool = False
        self.inputs: Deque = deque()
        # self.execution_trace: Dict[int, str] = {}

    def _disasm(self) -> str:
        addr = f"{self.ip:5}"
        opcode = self.tape[self.ip] % 100
        opname = INSTRUCTIONS[opcode].name
        params = []
        mask = 10
        for pnum, ptype in enumerate(INSTRUCTIONS[opcode].params, 1):
            mask *= 10
            pmode = ParameterMode((self.tape[self.ip] // mask) % 10)
            if ptype == ParameterType.WRITE:
                leader = "$"
            elif pmode == ParameterMode.POSITIONAL:
                leader = "$"
            elif pmode == ParameterMode.RELATIVE:
                leader = "@"
            else:
                leader = ""
            params.append(f"{leader}{self.tape[self.ip + pnum]}")
        return addr + ": " + f"{opname} " + ", ".join(params)

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
                position = self.tape[self.ip + param_num]
                if param_mode == ParameterMode.RELATIVE:
                    position += self.relative_base
                arguments.append(position)
            elif param_mode == ParameterMode.POSITIONAL:
                position = self.tape[self.ip + param_num]
                arguments.append(self.tape[position])
            elif param_mode == ParameterMode.IMMEDIATE:
                arguments.append(self.tape[self.ip + param_num])
            elif param_mode == ParameterMode.RELATIVE:
                position = self.tape[self.ip + param_num] + self.relative_base
                arguments.append(self.tape[position])
            else:
                raise TypeError(f"unknown parameter mode {param_mode}")
        return (opcode, arguments)

    def execute(self) -> Union[Optional[int], bool]:
        """Execute the instructions contained in the VM memory."""
        while self.ip < len(self.program):
            # self.execution_trace[self.ip] = self._disasm()
            opcode, params = self.decode_instruction()
            if opcode == 1:
                self.tape[params[2]] = params[0] + params[1]
                self.ip += 1 + len(params)
            elif opcode == 2:
                self.tape[params[2]] = params[0] * params[1]
                self.ip += 1 + len(params)
            elif opcode == 3:
                if self.chained_mode and self.inputs:
                    value = self.inputs.popleft()
                else:
                    value = int(input("$ "))
                self.last_input = self.tape[params[0]] = value
                self.ip += 1 + len(params)
            elif opcode == 4:
                self.last_output = params[0]
                self.ip += 1 + len(params)
                if self.chained_mode:
                    return True
                else:
                    print(self.last_output)
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
            elif opcode == 9:
                self.relative_base += params[0]
                self.ip += 1 + len(params)
            elif opcode == 99:
                if self.chained_mode:
                    return False
                else:
                    return self.last_output
        raise EOFError("reached end of tape without finding halt instruction.")

    def reset(self) -> None:
        """Reset the VM state before starting a new execution."""
        self.tape = self.program[:]
        # add extra memory space for data buffer
        self.tape += [0] * max(1024, len(self.program) * 3)
        self.ip = 0
        self.relative_base = 0
        # self.execution_trace = {}

    def set_inputs(self, inputs: List[int]) -> None:
        """Set the inputs for the VM to read."""
        self.inputs = deque(inputs)

    def set_noun_and_verb(self, noun: int, verb: int) -> None:
        """Set the noun and verb to initialize the program."""
        self.tape[1] = noun
        self.tape[2] = verb


if __name__ == "__main__":
    program: List[int] = []
    with open(sys.argv[1]) as inf:
        for line in inf:
            program += list(map(int, line.strip().split(",")))
    try:
        vm = Intcode(program)
        vm.execute()

        # addrs = list(vm.execution_trace.keys())
        # addrs.sort()
        # for addr in addrs:
        #     print(f"{vm.execution_trace[addr]}")
        # for ip in range(addrs[-1] + 1, len(vm.program)):
        #     print(f"{ip:5d}: {vm.program[ip]}")
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
