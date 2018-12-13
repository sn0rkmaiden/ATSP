import logging

from atsp import Map, Atsp
from atsp.algorithms.simulated_annealing import SimulatedAnnealing

logging.basicConfig(level=logging.INFO, format='')
import time


start = time.time()
city_map = Map.from_atsp('atsp/tests/test_data/ftv47.atsp')
# print(city_map.original_matrix)
# path, cost = Atsp(city_map).simulated_annealing()
solver = SimulatedAnnealing(city_map, cooling_factor=0.99997)
for _ in range(10):
    solver.solve(timeout=31, print_timeout=5)

print(solver.log.time_summary())
print(solver.log.best_summary())
# print(Atsp(city_map).first_branch_and_bound_solution())
