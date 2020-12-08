import re
import time
from dataclasses import dataclass
from typing import NoReturn, List


class ProgramState:
    def __init__(self):
        self.accumulator = 0
        self.instruction_index = 0


@dataclass
class Instruction:
    value: int
    executed: bool = False

    def do_action(self, program_state: ProgramState) -> NoReturn:
        self._internal_do_action(program_state)
        self.executed = True

    def _internal_do_action(self, program_state: ProgramState) -> NoReturn:
        raise NotImplementedError('Needs to be implemented by child classes')

    def get_opposite(self) -> 'Instruction':
        raise NotImplementedError('Needs to be implemented by child classes')


class AccumulatorInstruction(Instruction):
    def _internal_do_action(self, program_state: ProgramState) -> NoReturn:
        program_state.accumulator += self.value
        program_state.instruction_index += 1

    def get_opposite(self) -> 'Instruction':
        return self


class JumpInstruction(Instruction):
    def _internal_do_action(self, program_state: ProgramState) -> NoReturn:
        program_state.instruction_index += self.value

    def get_opposite(self) -> 'Instruction':
        return NoOpInstruction(self.value)


class NoOpInstruction(Instruction):
    def _internal_do_action(self, program_state: ProgramState) -> NoReturn:
        program_state.instruction_index += 1

    def get_opposite(self) -> 'Instruction':
        return JumpInstruction(self.value)


INSTRUCTION_CLASS_DICT = {
    'acc': AccumulatorInstruction,
    'jmp': JumpInstruction,
    'nop': NoOpInstruction
}


class InstructionFactory:
    @staticmethod
    def from_string(instruction_str: str, value: int) -> Instruction:
        instruction_class = INSTRUCTION_CLASS_DICT[instruction_str]
        return instruction_class(value)


class Program:
    def __init__(self, instructions: List[Instruction]):
        self.state = ProgramState()
        self.instructions = instructions

    def run_until_loop_found(self) -> NoReturn:
        while not self.finished() and not self.loop_found():
            self.instructions[self.state.instruction_index].do_action(self.state)

    def loop_found(self) -> bool:
        return self.instructions[self.state.instruction_index].executed

    def finished(self) -> bool:
        return self.state.instruction_index >= len(self.instructions)

    def reset(self) -> NoReturn:
        self.state = ProgramState()
        for instruction in self.instructions:
            instruction.executed = False


if __name__ == '__main__':
    with open('handheld_halting.txt', 'r') as f:
        start_time = time.time()
        all_file = f.read()
        instructions = [InstructionFactory.from_string(m.group(1), int(m.group(2))) for m in re.finditer(r'(nop|acc|jmp) ([+-]\d+)', all_file)]
        print(f'Found {len(instructions)} instructions')
        program = Program(instructions)
        program.run_until_loop_found()
        print(f'Accumulator part one: {program.state.accumulator}')

        for i in range(len(instructions)):
            tmp_instruction = instructions[i]
            if isinstance(tmp_instruction, (JumpInstruction, NoOpInstruction)):
                program.instructions[i] = tmp_instruction.get_opposite()
                program.reset()
                program.run_until_loop_found()
                if program.finished():
                    print(f'Accumulator part two: {program.state.accumulator}')
                    break
                instructions[i] = tmp_instruction

        print(f'Took {time.time() - start_time} seconds')
