import functools
import time
from dataclasses import dataclass


@dataclass
class Group:
    answers: str

    def count_unique(self):
        answers = self.answers.replace('\n', '')
        return len(set(answers))

    def count_intersection(self):
        answer_sets = [set(answer) for answer in self.answers.split('\n')]
        reduced_set = functools.reduce(lambda a, b: a.intersection(b), answer_sets)
        return len(reduced_set)


if __name__ == '__main__':
    with open('custom_customs.txt') as f:
        start_time = time.time()
        all_file = f.read()
        groups = [Group(answers) for answers in all_file.split('\n\n')]
        print(f'Got {len(groups)} groups')
        answers_unique_sum = sum(group.count_unique() for group in groups)
        answers_intersection_sum = sum(group.count_intersection() for group in groups)
        print(f'Unique sum: {answers_unique_sum}')
        print(f'Intersection sum: {answers_intersection_sum}')
        print(f'Took: {time.time() - start_time} seconds')
