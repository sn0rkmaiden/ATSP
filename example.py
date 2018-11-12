import logging
import time

from atsp import Map, Atsp

logging.basicConfig(level=logging.INFO)

start = time.time()
city_map = Map.from_file('atsp/tests/test_data/tsp_3_2.txt')
path, cost = Atsp(city_map).branch_and_bound()
print(path, cost)
end = time.time()
print(end - start)
