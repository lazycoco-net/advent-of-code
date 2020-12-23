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
        if direction is Direction.LEFT:
            direction_order.reverse()
        shift = int(degrees / 90)
        index = (direction_order.index(self) + shift) % 4
        return direction_order[index]

    @staticmethod
    def is_axis(value: str) -> bool:
        return value in {e.value for e in set(Axis)}


@dataclass
class Instruction:
    action: str
    value: int


@dataclass
class Point:
    x: int
    y: int

    def move(self, axis: Axis, value: int) -> NoReturn:
        if axis is Axis.NORTH:
            self.y += value
        elif axis is Axis.SOUTH:
            self.y -= value
        elif axis is Axis.EAST:
            self.x += value
        elif axis is Axis.WEST:
            self.x -= value

    def rotate(self, direction: Direction, degrees: int) -> NoReturn:
        shift = int(degrees / 90)
        for i in range(shift):
            if direction is Direction.RIGHT:
                new_x = self.y
                new_y = -self.x
            else:
                new_x = -self.y
                new_y = self.x
            self.x = new_x
            self.y = new_y


class NavigationSystem:
    def __init__(self, start_axis: Axis):
        self.ship_position = Point(0, 0)
        self.axis = start_axis

    def process_instructions(self, instructions: List[Instruction]) -> NoReturn:
        for instruction in instructions:
            if Axis.is_axis(instruction.action):
                self.move(Axis(instruction.action), instruction.value)
            elif Direction.is_direction(instruction.action):
                direction = Direction(instruction.action)
                if direction is Direction.FORWARD:
                    self.move_forward(instruction.value)
                else:
                    self.rotate(direction, instruction.value)

    def move(self, axis: Axis, value: int) -> NoReturn:
        self.ship_position.move(axis, value)

    def move_forward(self, value: int) -> NoReturn:
        self.move(self.axis, value)

    def rotate(self, direction: Direction, value: int) -> NoReturn:
        self.axis = self.axis.rotate(direction, value)

    def manhattan_distance(self) -> float:
        return math.fabs(self.ship_position.x) + math.fabs(self.ship_position.y)


class WaypointNavigationSystem(NavigationSystem):

    def __init__(self, start_axis: Axis, waypoint_position: Point):
        super().__init__(start_axis)
        self.waypoint_position = waypoint_position

    def move(self, axis: Axis, value: int) -> NoReturn:
        self.waypoint_position.move(axis, value)

    def move_forward(self, value: int) -> NoReturn:
        self.ship_position.x += self.waypoint_position.x * value
        self.ship_position.y += self.waypoint_position.y * value

    def rotate(self, direction: Direction, value: int) -> NoReturn:
        self.waypoint_position.rotate(direction, value)


if __name__ == '__main__':
    with open('rain_risk.txt') as f:
        start_time = time.time()
        all_file = f.read()
        instructions = [Instruction(m.group(1), int(m.group(2))) for m in re.finditer(r'(\w)(\d+)', all_file)]
        navigation = NavigationSystem(Axis.EAST)
        navigation.process_instructions(instructions)
        manhattan_distance = navigation.manhattan_distance()
        print(f'Manhattan distance Part One: {manhattan_distance}')
        waypoint_navigation = WaypointNavigationSystem(Axis.EAST, Point(10, 1))
        waypoint_navigation.process_instructions(instructions)
        manhattan_distance = waypoint_navigation.manhattan_distance()
        print(f'Manhattan distance Part Two: {manhattan_distance}')
        print(f'Took {time.time() - start_time} seconds')
