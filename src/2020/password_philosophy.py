import re
import time


def is_password_valid_part_one(password: str, character: str, minimum: int, maximum: int) -> bool:
    occurrences = password.count(character)
    return minimum <= occurrences <= maximum


def is_password_valid_part_two(password: str, character: str, first_position: int, second_position: int) -> bool:
    first_index = first_position - 1
    second_index = second_position - 1
    return (password[first_index] == character and password[second_index] != character) or \
           (password[first_index] != character and password[second_index] == character)


if __name__ == '__main__':
    with open('password_philosophy.txt', 'r') as f:
        start_time = time.time()
        pattern = r'(\d+)-(\d+) (\w): (\w+)'
        count_part_1 = 0
        count_part_2 = 0
        for line in f:
            match = re.match(pattern, line)
            if match:
                minimum = int(match.group(1))
                maximum = int(match.group(2))
                character = match.group(3)
                password = match.group(4)
                if is_password_valid_part_one(password, character, minimum, maximum):
                    count_part_1 += 1
                if is_password_valid_part_two(password, character, minimum, maximum):
                    count_part_2 += 1

        end_time = time.time()
        print(f'Count part one: {count_part_1}')
        print(f'Count part two: {count_part_2}')
        print(f'Took: {end_time - start_time} seconds')
