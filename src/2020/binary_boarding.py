import math
import re
import time
from typing import Dict


def binary_to_decimal(number_str: str, zero_char: str, one_char: str) -> int:
    return int(number_str.replace(zero_char, '0').replace(one_char, '1'), 2)


def is_my_seat(seats_taken: Dict[int, bool], seat_id: int) -> bool:
    is_first_row = 0 <= seat_id <= 7
    is_last_row = 1015 <= seat_id <= 1023
    return not is_first_row and not is_last_row and not seats_taken[seat_id] and seats_taken[seat_id-1] and seats_taken[seat_id+1]


if __name__ == '__main__':
    with open('binary_boarding.txt', 'r') as f:
        star_time = time.time()
        maximum = -math.inf
        seats_taken = {i: False for i in range(0, 128 * 8)}
        for line in f:
            match = re.match(r'([B|F]{7})([L|R]{3})', line)
            row = binary_to_decimal(match.group(1), zero_char='F', one_char='B')
            column = binary_to_decimal(match.group(2), zero_char='L', one_char='R')
            seat_id = row * 8 + column
            maximum = max(seat_id, maximum)
            seats_taken[seat_id] = True

        for seat_id in seats_taken.keys():
            if is_my_seat(seats_taken, seat_id):
                print(f'Found my seat id: {seat_id}')

        print(f'Max seat id: {maximum}')
        print(f'Took {time.time() - star_time} seconds')
