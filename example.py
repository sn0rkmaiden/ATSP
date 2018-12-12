import logging

from atsp import Map, Atsp

logging.basicConfig(level=logging.INFO)
import time


start = time.time()
city_map = Map.from_atsp('atsp/tests/test_data/rbg403.atsp')
# print(city_map.original_matrix)
# path, cost = Atsp(city_map).simulated_annealing()
print(Atsp(city_map).simulated_annealing(cooling_factor=0.99993, timeout=900))
time_taken = time.time() - start
print(time_taken)
# print(Atsp(city_map).first_branch_and_bound_solution())
