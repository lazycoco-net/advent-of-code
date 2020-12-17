import copy
import time
from typing import List, NoReturn, Tuple, Optional


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
        return not self.get_occupied_seats_for(x, y) if self.is_empty_seat(x, y) else False

    def should_empty_seat(self, x: int, y: int) -> bool:
        return len(self.get_occupied_seats_for(x, y)) >= self.tolerance() if self.is_occupied_seat(x, y) else False

    def get_occupied_seats_for(self, x: int, y: int) -> List[str]:
        return [s for s in self.get_visible_seats_for(x, y) if s == '#']

    def get_visible_seats_for(self, x: int, y: int) -> List[str]:
        raise NotImplementedError('Needs to be implemented in child classes')

    def tolerance(self) -> int:
        raise NotImplementedError('Needs to be implemented in child classes')

    def is_empty_seat(self, x: int, y: int) -> bool:
        return self.current_rows[x][y] == 'L'

    def is_occupied_seat(self, x: int, y: int) -> bool:
        return self.current_rows[x][y] == '#'

    def is_floor(self, x: int, y: int) -> bool:
        return self.current_rows[x][y] == '.'

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def count_occupied_seats(self) -> int:
        return len([self.current_rows[i][j] for i in range(self.height) for j in range(self.width) if self.is_occupied_seat(i, j)])

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'r') as f:
            rows = [list(line.replace('\n', '')) for line in f]
            return cls(rows)


class AdjacentSeatingMap(SeatingMap):
    def get_visible_seats_for(self, x: int, y: int) -> List[str]:
        return [self.current_rows[i][j]
                for i in range(x-1, x+2)
                for j in range(y-1, y+2)
                if self.is_valid_position(i, j) and not (i == x and j == y)]

    def tolerance(self) -> int:
        return 4


class FirstVisibleSeatingMap(SeatingMap):
    def get_visible_seats_for(self, x: int, y: int) -> List[str]:
        directions = [(a, b) for a in range(-1, 2) for b in range(-1, 2) if not (a == 0 and b == 0)]
        seats = (self.find_first_visible_seat_for(x, y, direction) for direction in directions)
        return [seat for seat in seats if seat]

    def find_first_visible_seat_for(self, x: int, y: int, direction: Tuple[int, int]) -> Optional[str]:
        i = x + direction[0]
        j = y + direction[1]
        while self.is_valid_position(i, j):
            if not self.is_floor(i, j):
                return self.current_rows[i][j]
            i += direction[0]
            j += direction[1]
        return None

    def tolerance(self) -> int:
        return 5


if __name__ == '__main__':
    start_time = time.time()
    seating_map = AdjacentSeatingMap.from_file('seating_system.txt')
    seating_map.stabilize_chaos()
    occupied_seats = seating_map.count_occupied_seats()
    print(f'Occupied seats part one: {occupied_seats}')
    first_part_time = time.time()
    print(f'Took {first_part_time - start_time} seconds')
    seating_map = FirstVisibleSeatingMap.from_file('seating_system.txt')
    seating_map.stabilize_chaos()
    occupied_seats = seating_map.count_occupied_seats()
    print(f'Occupied seats part two: {occupied_seats}')
    print(f'Took {time.time() - first_part_time} seconds')
