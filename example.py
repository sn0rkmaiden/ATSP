import logging

from atsp import Map, Atsp

logging.basicConfig(level=logging.INFO)

city_map = Map.from_atsp('atsp/tests/test_data/rbg403.atsp')
# print(city_map.original_matrix)
# path, cost = Atsp(city_map).simulated_annealing()
print(Atsp(city_map).simulated_annealing())
# print(Atsp(city_map).first_branch_and_bound_solution())
