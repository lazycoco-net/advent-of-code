import functools
import math
import time
from typing import List


class BusService:
    def __init__(self, bus_id: str, arrival_time: int, offset: int):
        self.bus_id = int(bus_id) if bus_id != 'x' else 0
        self.arrival_time = arrival_time
        self.offset = offset

    def in_service(self) -> bool:
        return self.bus_id != 0

    def next_departure(self) -> int:
        return self.bus_id * math.ceil(self.arrival_time / self.bus_id)

    def x_i(self, lcm: int) -> int:
        remainder = (lcm / self.bus_id) % self.bus_id
        i = 0
        while True:
            i += 1
            if remainder * i % self.bus_id == 1:
                break
        return int(lcm / self.bus_id) * i


def find_earliest_bus(services: List[BusService]) -> BusService:
    available_buses = [bus for bus in services if bus.in_service()]
    return min(available_buses, key=lambda b: b.next_departure())


def find_earliest_timestamp(services: List[BusService]) -> int:
    available_buses = [bus for bus in services if bus.in_service()]
    lcm = functools.reduce(lambda a, b: a*b, [bus.bus_id for bus in available_buses])
    solution = sum([(bus.bus_id - bus.offset) * bus.x_i(lcm) for bus in available_buses])
    while solution - lcm > 0:
        solution -= lcm
    return solution


if __name__ == '__main__':
    with open('shuttle_search.txt', 'r') as f:
        start_time = time.time()
        arrival = int(f.readline())
        services = [BusService(b, arrival, offset) for offset, b in enumerate(f.readline().split(','))]
        bus = find_earliest_bus(services)
        result = bus.bus_id * (bus.next_departure() - bus.arrival_time)
        print(f'Result: {result}')
        earliest = find_earliest_timestamp(services)
        print(f'Earliest: {earliest}')
        print(f'Took {time.time() - start_time} seconds')
