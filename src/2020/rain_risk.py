import math
import re
import time
from dataclasses import dataclass
from enum import Enum
from typing import List, NoReturn


class Direction(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'

    @staticmethod
    def is_direction(value: str) -> bool:
        return value in {e.value for e in set(Direction)}


class Axis(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'

    def rotate(self, direction: Direction, degrees: int) -> 'Axis':
        direction_order = list(Axis)
        if direction == Direction.LEFT:
            direction_order.reverse()
        shift = degrees / 90
        index = int((direction_order.index(self) + shift) % 4)
        return direction_order[index]

    @staticmethod
    def values() -> List['Axis']:
        return [Axis.NORTH, Axis.EAST, Axis.SOUTH, Axis.WEST]

    @staticmethod
    def is_axis(value: str) -> bool:
        return value in {e.value for e in set(Axis)}


@dataclass
class Instruction:
    action: str
    value: int


class NavigationSystem:
    def __init__(self, start_axis: Axis):
        self.x = 0
        self.y = 0
        self.axis = start_axis

    def process_instructions(self, instructions: List[Instruction]) -> NoReturn:
        for instruction in instructions:
            if Axis.is_axis(instruction.action):
                self.move(Axis(instruction.action), instruction.value)
            elif Direction.is_direction(instruction.action):
                direction = Direction(instruction.action)
                if direction == Direction.FORWARD:
                    self.move(self.axis, instruction.value)
                else:
                    self.rotate(Direction(instruction.action), instruction.value)

    def move(self, axis: Axis, value: int) -> NoReturn:
        if axis is Axis.NORTH:
            self.y += value
        elif axis is Axis.SOUTH:
            self.y -= value
        elif axis is Axis.EAST:
            self.x += value
        elif axis is Axis.WEST:
            self.x -= value

    def rotate(self, direction: Direction, value: int) -> NoReturn:
        self.axis = self.axis.rotate(direction, value)

    def manhattan_distance(self) -> float:
        return math.fabs(self.x) + math.fabs(self.y)


if __name__ == '__main__':
    with open('rain_risk.txt') as f:
        start_time = time.time()
        all_file = f.read()
        instructions = [Instruction(m.group(1), int(m.group(2))) for m in re.finditer(r'(\w)(\d+)', all_file)]
        navigation = NavigationSystem(Axis.EAST)
        navigation.process_instructions(instructions)
        manhattan_distance = navigation.manhattan_distance()
        print(f'Manhattan distance: {manhattan_distance}')
        print(f'Took {time.time() - start_time} seconds')
