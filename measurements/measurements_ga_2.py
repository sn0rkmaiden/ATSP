import logging

from atsp import Map
from atsp.algorithms.genetic_algorithm.solver import GeneticSolver

logging.basicConfig(level=logging.ERROR, format='')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class Measurement(object):

    def __init__(self, file_path, known_best_value, population_size, repetitions=10, timeout=30):
        city_map = Map.from_atsp(file_path)
        self.known_best_value = known_best_value
        self.solver = GeneticSolver(city_map, population_size=population_size,
                                    crossover_coefficient=0.8,
                                    mutation_coefficient=0.1)
        self.repetitions = repetitions
        self.timeout = timeout

    def measure(self):
        values = []
        for _ in range(self.repetitions):
            path, cost = self.solver.solve(self.timeout)
            values.append({
                'cost': cost,
                'error': round((cost - self.known_best_value) / self.known_best_value, 5),
            })
        values = {k: [dic[k] for dic in values] for k in values[0]}
        return {
            'cost': round(sum(values['cost']) / len(values['cost'])),
            'error': round(sum(values['error']) / len(values['error']), 5),
        }


logger.info('Population\tCost\tError')
for population_size in range(10, 25, 2):
    measurement = Measurement('../atsp/tests/test_data/ftv47.atsp', known_best_value=1776,
                              population_size=population_size, timeout=10)
    result = measurement.measure()
    logger.info('{population_size}\t{cost}\t{error}'.format(population_size=population_size, **result))
logger.info('Population\tCost\tError')
for population_size in range(5, 101, 5):
    measurement = Measurement('../atsp/tests/test_data/ftv170.atsp', known_best_value=2755,
                              population_size=population_size, timeout=10)
    result = measurement.measure()
    logger.info('{population_size}\t{cost}\t{error}'.format(population_size=population_size, **result))
logger.info('Population\tCost\tError')
for population_size in range(5, 101, 5):
    measurement = Measurement('../atsp/tests/test_data/rbg403.atsp', known_best_value=2465,
                              population_size=population_size, timeout=10)
    result = measurement.measure()
    logger.info('{population_size}\t{cost}\t{error}'.format(population_size=population_size, **result))
