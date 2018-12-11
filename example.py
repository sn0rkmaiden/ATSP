import logging

from atsp import Map, Atsp

# logging.basicConfig(level=logging.INFO)

city_map = Map.from_file('atsp/tests/test_data/tsp_17_2.txt')
# path, cost = Atsp(city_map).simulated_annealing()
print(Atsp(city_map).simulated_annealing())
print(Atsp(city_map).first_branch_and_bound_solution())
