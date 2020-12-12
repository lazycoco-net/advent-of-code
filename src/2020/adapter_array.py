import time
from typing import List, Dict


def calculate_joltage_diff_distribution(joltages: List[int]) -> Dict[int, int]:
    dictionary = {
        1: 0,
        3: 0
    }
    for index in range(len(joltages) - 1):
        diff = joltages[index+1] - joltages[index]
        dictionary[diff] += 1
    return dictionary


def calculate_arrangements(joltages: List[int]) -> int:
    joltages_dict = {joltage: [adapter for adapter in joltages if 1 <= adapter - joltage <= 3] for joltage in joltages}
    cache = {joltages[-1]: 1}
    return _calculate_arrangements(0, joltages_dict, cache)


def _calculate_arrangements(joltage: int, joltages_dict: Dict[int, List[int]], cache: Dict[int, int]) -> int:
    if joltage in cache:
        return cache[joltage]
    cache[joltage] = sum(_calculate_arrangements(adapter, joltages_dict, cache) for adapter in joltages_dict[joltage])
    return cache[joltage]


if __name__ == '__main__':
    with open('adapter_array.txt', 'r') as f:
        start_time = time.time()
        joltages = [0] + [int(line) for line in f]
        joltages.sort()
        joltages += [joltages[-1] + 3]
        dictionary = calculate_joltage_diff_distribution(joltages)
        result = dictionary[1] * dictionary[3]
        print(f'Result: {result}')
        arrangements = calculate_arrangements(joltages)
        print(f'Arrangements: {arrangements}')
        print(f'Took {time.time() - start_time} seconds')
