import re
import time
from typing import List


def mask_character(character: str, mask: str) -> str:
    return character if mask == 'X' else mask


def mask_value(value: int, mask: str) -> int:
    binary_str = '{0:036b}'.format(value)
    masked_list = [mask_character(character, mask_char) for character, mask_char in zip(list(binary_str), list(mask))]
    return int(''.join(masked_list), 2)


def mask_character_part_2(character: str, mask: str) -> str:
    return character if mask == '0' else mask


def mask_value_part_2(value: int, mask: str) -> List[str]:
    binary_str = '{0:036b}'.format(value)
    return [mask_character_part_2(character, mask_char) for character, mask_char in zip(list(binary_str), list(mask))]


def get_combinations(value_list: List[str]) -> List[str]:
    if not value_list:
        return ['']
    result = get_combinations(value_list[1:])
    if value_list[0] == 'X':
        return [f'0{combination}' for combination in result] + [f'1{combination}' for combination in result]
    return [f'{value_list[0]}{combination}' for combination in result]


def memory_combinations(value: int, mask: str) -> List[int]:
    binary_list = mask_value_part_2(value, mask)
    combinations = get_combinations(binary_list)
    return [int(combination, 2) for combination in combinations]


if __name__ == '__main__':
    with open('docking_data.txt') as f:
        start_time = time.time()
        memory = {}
        memory_part_2 = {}
        for line in f:
            m = re.match(r'mask = ([X10]{36})', line)
            if m:
                mask = m.group(1)
                continue
            m = re.match(r'mem\[(\d+)\] = (\d+)', line)
            mem_id = int(m.group(1))
            mem_value = int(m.group(2))
            memory[mem_id] = mask_value(mem_value, mask)
            combinations = memory_combinations(mem_id, mask)
            for combination in combinations:
                memory_part_2[combination] = mem_value

        print(f'Sum part 1: {sum(memory.values())}')
        print(f'Sum part 2: {sum(memory_part_2.values())}')
        print(f'Took {time.time() - start_time} seconds')
