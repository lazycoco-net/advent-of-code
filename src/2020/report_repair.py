import time
from typing import Set, Tuple, Optional


def find_two_that_sums(sum: int, input_set: Set[int], excluded: Optional[int] = None) -> Optional[Tuple[int, int]]:
    for value in input_set:
        if value == excluded:
            continue
        complement = sum - value
        if complement in input_set:
            return value, complement

    return None


def find_three_that_sums(sum: int, input_set: Set[int]) -> Optional[Tuple[int, int, int]]:
    for value in input_set:
        complement = sum - value
        result = find_two_that_sums(complement, input_set, excluded=value)
        if result:
            second, third = result
            return value, second, third

    return None


if __name__ == '__main__':
    with open('report_repair_input.txt', 'r') as f:
        input_set = {int(line.replace('\n', '')) for line in f}

    # Part one: Using hashing implementation. I'll put all numbers in a set. Then for each number I'll calculate the number it
    # needs for adding up to 2020 and check if the number is in that set. If found, then calculate the multiplication.
    # value in input_set takes O(1).
    print('### Part one ###')
    start_time = time.time()
    result = find_two_that_sums(2020, input_set)
    if not result:
        print('No pair of values found that add to 2020')
    else:
        first, second = result
        print(f'Values found: {first} and {second}')
        print(f'Multiplication: {first * second}')
    part_one_end_time = time.time()
    print(f'Took {part_one_end_time - start_time} seconds')

    # Part two: Using the previous implementation. For each value, I'll calculate the number it needs for adding up to 2020,
    # then I try to find two numbers that add up to this new number. If found, then calculate the multiplication.
    print('\n### Part two ###')
    result = find_three_that_sums(2020, input_set)
    if not result:
        print('No three values found that add to 2020')
    else:
        first, second, third = result
        print(f'Values found: {first}, {second} and {third}')
        print(f'Multiplication: {first * second * third}')
    part_two_end_time = time.time()
    print(f'Took {part_two_end_time - part_one_end_time} seconds')
