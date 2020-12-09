import time
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple


def find_two_that_sums(the_sum: int, input_set: Set[int]) -> Optional[Tuple[int, int]]:
    for value in input_set:
        complement = the_sum - value
        if complement != value and complement in input_set:
            return value, complement

    return None


@dataclass
class XmasDecoder:
    data: List[int]
    preamble_length: int

    def find_first_invalid(self) -> Optional[int]:
        start_index = 0
        preamble_set = set(self.data[:self.preamble_length])
        for index in range(self.preamble_length, len(self.data)):
            result = find_two_that_sums(self.data[index], preamble_set)
            if not result:
                return self.data[index]
            preamble_set.remove(self.data[start_index])
            preamble_set.add(self.data[index])
            start_index += 1
        return None

    def find_contiguous_set_that_sum(self, the_sum: int) -> Set[int]:
        start_index = 0
        end_index = 1
        data_length = len(self.data)
        current_sum = self.data[0] + self.data[1]
        while end_index < data_length:
            if current_sum == the_sum:
                return set(self.data[start_index:end_index+1])
            elif current_sum > the_sum:
                current_sum -= self.data[start_index]
                start_index += 1
            else:
                end_index += 1
                if end_index >= data_length:
                    break
                current_sum += self.data[end_index]
        return set()


if __name__ == '__main__':
    with open('encoding_error.txt', 'r') as f:
        start_time = time.time()
        data = [int(line) for line in f]
        print(f'Got {len(data)} numbers.')
        encoder = XmasDecoder(data, 25)
        value = encoder.find_first_invalid()
        print(f'First invalid: {value}')
        contiguous_set = encoder.find_contiguous_set_that_sum(value)
        encryption_weakness = min(contiguous_set) + max(contiguous_set)
        print(f'Encryption weakness: {encryption_weakness}')
        print(f'Took {time.time() - start_time} seconds.')
