import copy
import time
from typing import List, NoReturn


class SeatingMap:
    def __init__(self, rows: List[List[str]]):
        self.current_rows = rows
        self.next_rows = None
        self.width = len(rows[0])
        self.height = len(rows)

    def stabilize_chaos(self) -> NoReturn:
        keep_looping = True
        while keep_looping:
            self.calculate_next_rows()
            keep_looping = self.next_has_changed()
            self.current_rows = self.next_rows

    def next_has_changed(self) -> bool:
        return self.current_rows != self.next_rows

    def calculate_next_rows(self) -> NoReturn:
        self.next_rows = copy.deepcopy(self.current_rows)
        for i in range(self.width):
            for j in range(self.height):
                if self.should_occupy_seat(j, i):
                    self.next_rows[j][i] = '#'
                elif self.should_empty_seat(j, i):
                    self.next_rows[j][i] = 'L'

    def should_occupy_seat(self, x: int, y: int) -> bool:
        return not self.get_adjacent_occupied_seats(x, y) if self.is_empty_seat(x, y) else False

    def should_empty_seat(self, x: int, y: int) -> bool:
        return len(self.get_adjacent_occupied_seats(x, y)) >= 4 if self.is_occupied_seat(x, y) else False

    def is_empty_seat(self, x: int, y: int) -> bool:
        return self.current_rows[x][y] == 'L'

    def is_occupied_seat(self, x: int, y: int) -> bool:
        return self.current_rows[x][y] == '#'

    def get_adjacent_seats(self, x: int, y: int) -> List[str]:
        return [self.current_rows[i][j]
                for i in range(x-1, x+2)
                for j in range(y-1, y+2)
                if self.is_valid_position(i, j) and not (i == x and j == y)]

    def get_adjacent_occupied_seats(self, x: int, y: int) -> List[str]:
        return [s for s in self.get_adjacent_seats(x, y) if s == '#']

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def count_occupied_seats(self) -> int:
        return len([self.current_rows[i][j] for i in range(self.height) for j in range(self.width) if self.is_occupied_seat(i, j)])

    @staticmethod
    def from_file(file_name: str) -> 'SeatingMap':
        with open(file_name, 'r') as f:
            rows = [list(line.replace('\n', '')) for line in f]
            return SeatingMap(rows)


if __name__ == '__main__':
    start_time = time.time()
    seating_map = SeatingMap.from_file('seating_system.txt')
    seating_map.stabilize_chaos()
    occupied_seats = seating_map.count_occupied_seats()
    print(f'Occupied seats: {occupied_seats}')
    print(f'Took {time.time() - start_time} seconds')
