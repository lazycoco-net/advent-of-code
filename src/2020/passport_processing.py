import functools
import re
import time
from dataclasses import dataclass
from typing import Dict, Set, Optional


class Validator:
    def validate(self, value: str) -> bool:
        raise NotImplementedError('Needs to be implemented in child classes')


@dataclass
class RangeValidator(Validator):
    min_value: int
    max_value: int

    def validate(self, value: str) -> bool:
        return self.min_value <= int(value) <= self.max_value


class HeightValidator(Validator):
    validators: Dict[str, RangeValidator] = {
        'cm': RangeValidator(150, 193),
        'in': RangeValidator(59, 76)
    }

    def validate(self, value: str) -> bool:
        match = re.match(r'^(\d+)(cm|in)$', value)
        if match:
            height = match.group(1)
            unit = match.group(2)
            return self.validators[unit].validate(height) if unit in self.validators else False
        return False


class HairColorValidator(Validator):
    def validate(self, value: str) -> bool:
        return re.match(r'^#[0-9a-f]{6}$', value) is not None


class EyeColorValidator(Validator):
    valid_colors: Set[str] = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    def validate(self, value: str) -> bool:
        return value in self.valid_colors


class PassportIdValidator(Validator):

    def validate(self, value: str) -> bool:
        return re.match(r'^\d{9}$', value) is not None


@dataclass
class PassportField:
    name: str
    required: bool = True
    validator: Optional[Validator] = None

    def validate(self, dictionary: Dict[str, str]) -> bool:
        if self.required:
            if self.name in dictionary:
                return self.validator.validate(dictionary[self.name]) if self.validator else True
            return False
        return True


FIELDS = [
    PassportField('byr', validator=RangeValidator(1920, 2002)),
    PassportField('iyr', validator=RangeValidator(2010, 2020)),
    PassportField('eyr', validator=RangeValidator(2020, 2030)),
    PassportField('hgt', validator=HeightValidator()),
    PassportField('hcl', validator=HairColorValidator()),
    PassportField('ecl', validator=EyeColorValidator()),
    PassportField('pid', validator=PassportIdValidator()),
    PassportField('cid', required=False)
]


def to_dictionary(input_str: str) -> Dict[str, str]:
    return {s.split(':')[0]: s.split(':')[1] for s in re.split(r'\s', input_str)}


def is_passport_valid(passport_info: Dict[str, str]) -> bool:
    validation = [field.validate(passport_info) for field in FIELDS]
    return functools.reduce(lambda a, b: a and b, validation)


if __name__ == '__main__':
    with open('passport_processing.txt') as f:
        start_time = time.time()
        all_file = f.read()
        passports = all_file.split('\n\n')
        print(f'Got {len(passports)} passports')
        count = 0
        for passport_str in passports:
            passport_info = to_dictionary(passport_str)
            if is_passport_valid(passport_info):
                count += 1

        print(f'Valid passports: {count}')
        print(f'Took {time.time() - start_time} seconds')
