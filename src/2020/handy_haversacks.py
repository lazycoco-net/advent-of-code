import re
import time
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GraphNode:
    color: str
    quantity: int


@dataclass
class Graph:
    dictionary: Dict[str, List[GraphNode]]

    def count_bags_that_can_contain(self, bag_color: str) -> int:
        bags_cache = {}
        for color in self.dictionary.keys():
            bags_cache[color] = self._can_contain(bag_color, color, bags_cache)
        return len([t for t in bags_cache.values() if t is True])

    def _can_contain(self, bag_color_to_contain: str, bag_color_to_check: str, bags_cache: Dict[str, bool]) -> bool:
        if bag_color_to_check in bags_cache:
            return bags_cache[bag_color_to_check]
        for node in self.dictionary[bag_color_to_check]:
            if node.color == bag_color_to_contain:
                bags_cache[bag_color_to_check] = True
                return True
            if self._can_contain(bag_color_to_contain, node.color, bags_cache):
                return True
        bags_cache[bag_color_to_check] = False
        return False

    def count_needed_bags_for(self, bag_color: str) -> int:
        return self._count_bags_for(bag_color, {})

    def _count_bags_for(self, bag_color: str, bags_cache: Dict[str, int]) -> int:
        if bag_color in bags_cache:
            return bags_cache[bag_color]
        count = sum([node.quantity + node.quantity * self._count_bags_for(node.color, bags_cache) for node in self.dictionary[bag_color]])
        bags_cache[bag_color] = count
        return count


if __name__ == '__main__':
    with open('handy_haversacks.txt', 'r') as f:
        start_time = time.time()
        bags_dictionary = {}
        for line in f:
            color_match = re.match(r'(\w+ \w+) bags contain', line)
            color = color_match.group(1)
            sub_bags_iterator = re.finditer(r'(\d) (\w+ \w+) bag[s]?[.,]', line)
            bags_dictionary[color] = [GraphNode(m.group(2), int(m.group(1))) for m in sub_bags_iterator]

        print(f'Got {len(bags_dictionary)} nodes')
        graph = Graph(bags_dictionary)
        count_part_1 = graph.count_bags_that_can_contain('shiny gold')
        print(f'Count Part 1: {count_part_1}')
        count_part_2 = graph.count_needed_bags_for('shiny gold')
        print(f'Count Part 2: {count_part_2}')
        print(f'Took {time.time() - start_time} seconds')
