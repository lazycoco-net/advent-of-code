import functools
import re
import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class PassportField:
    name: str
    required: bool = True

    def validate(self, dictionary: Dict[str, str]) -> bool:
        return self.name in dictionary if self.required else True


FIELDS = [
    PassportField('byr'),
    PassportField('iyr'),
    PassportField('eyr'),
    PassportField('hgt'),
    PassportField('hcl'),
    PassportField('ecl'),
    PassportField('pid'),
    PassportField('cid', required=False)
]


def to_dictionary(input_str: str) -> Dict[str, str]:
    return {s.split(':')[0]: s.split(':')[1] for s in re.split(r'\s', input_str)}


def is_password_valid(passport_info: Dict[str, str]) -> bool:
    validation = [field.validate(passport_info) for field in FIELDS]
    return functools.reduce(lambda a, b: a and b, validation)


if __name__ == '__main__':
    with open('passport_processing.txt') as f:
        start_time = time.time()
        all_file = f.read()
        passports = all_file.split('\n\n')
        count = 0
        for passport_str in passports:
            passport_info = to_dictionary(passport_str)
            if is_password_valid(passport_info):
                count += 1

        print(f'Valid passports: {count}')
        print(f'Took {time.time() - start_time} seconds')
