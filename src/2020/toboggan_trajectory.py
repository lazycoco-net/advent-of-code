import functools
import time
from dataclasses import dataclass
from typing import List, NoReturn


@dataclass
class MovePattern:
    right: int
    down: int


class TobogganMap:
    def __init__(self, rows: List[str]):
        self.rows = rows
        self.width = len(rows[0])
        self.height = len(rows)
        self.x = 0
        self.y = 0

    def count_trees(self, move_pattern: MovePattern) -> int:
        self.x = 0
        self.y = 0
        count = 0
        while not self.is_end():
            if self.is_tree():
                count += 1
            self.next_move(move_pattern)
        return count

    def next_move(self, move_pattern: MovePattern) -> NoReturn:
        self.x = (self.x + move_pattern.right) % self.width
        self.y = self.y + move_pattern.down

    def is_end(self) -> bool:
        return self.y >= self.height

    def is_tree(self) -> bool:
        try:
            return self.rows[self.y][self.x] == '#'
        except IndexError as e:
            print(f'Error at ({self.y}, {self.x})')
            raise e

    @staticmethod
    def from_file(file_name: str) -> 'TobogganMap':
        with open(file_name, 'r') as f:
            rows = [line.replace('\n', '') for line in f]
            return TobogganMap(rows)


if __name__ == '__main__':
    start_time = time.time()
    toboggan_map = TobogganMap.from_file('toboggan_trajectory.txt')
    move_patterns = [
        MovePattern(1, 1),
        MovePattern(3, 1),
        MovePattern(5, 1),
        MovePattern(7, 1),
        MovePattern(1, 2)
    ]
    counts = [toboggan_map.count_trees(move_pattern) for move_pattern in move_patterns]
    print(f'All counts: {counts}')
    print(f'Multiplication: {functools.reduce(lambda a, b: a * b, counts)}')
    print(f'Took {time.time() - start_time} seconds')
