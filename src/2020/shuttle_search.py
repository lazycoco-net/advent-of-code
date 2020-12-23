import math
import re
import time
from typing import List


class BusService:
    def __init__(self, bus_id: str, arrival_time: int):
        self.bus_id = int(bus_id) if bus_id != 'x' else 0
        self.arrival_time = arrival_time

    def in_service(self) -> bool:
        return self.bus_id != 0

    def next_departure(self) -> int:
        return self.bus_id * math.ceil(self.arrival_time / self.bus_id)


def find_earliest_bus(services: List[BusService]) -> BusService:
    available_buses = [bus for bus in services if bus.in_service()]
    return min(available_buses, key=lambda b: b.next_departure())


if __name__ == '__main__':
    with open('shuttle_search.txt', 'r') as f:
        start_time = time.time()
        arrival = int(f.readline())
        services = [BusService(b, arrival) for b in f.readline().split(',')]
        bus = find_earliest_bus(services)
        result = bus.bus_id * (bus.next_departure() - bus.arrival_time)
        print(f'Result: {result}')
        print(f'Took {time.time() - start_time} seconds')
