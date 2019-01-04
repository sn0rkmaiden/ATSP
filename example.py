import logging

from atsp import Map
from atsp.algorithms.genetic_algorithm import GeneticSolver

logging.basicConfig(level=logging.INFO, format='')
logger = logging.getLogger(__name__)
#
city_map = Map.from_atsp('atsp/tests/test_data/ftv47.atsp')
# city_map = Map.from_file('atsp/tests/test_data/tsp_17.txt')
solver = GeneticSolver(city_map, population_size=50, crossover_coefficient=1, mutation_coefficient=0.2)
# path, cost = solver.solve(timeout=31, print_timeout=5)
#
# print(solver.log.time_summary())
# print(solver.log.best_summary())
path, cost = solver.solve(timeout=15)
logger.info(f'Path {path}\nCost {cost}')
