import logging
import time

from atsp import Atsp, Map
from atsp.algorithms.branch_and_bound.solver import BranchAndBoundSolver

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def find_first_solution(city_map, timeout):
    return BranchAndBoundSolver(city_map).find_first_solution(timeout=timeout)


def find_best_solutions(city_map, timeout):
    return BranchAndBoundSolver(city_map).solve(timeout=timeout)


class Measurement(object):

    def __init__(self, size, repetitions=100, timeout=30):
        self.size = size
        self.repetitions = repetitions
        self.timeout = timeout

    def measure_brute_force(self):
        values = []
        for _ in range(self.repetitions):
            city_map = Map.from_random_matrix(size=self.size)
            atsp = Atsp(city_map)
            start = time.time()
            atsp.brute_force()
            time_taken = time.time() - start
            values.append(time_taken)
            # logger.debug(time_taken)
        return sum(values) / len(values)


logger.info('Size,Best average')
for i in range(5, 16, 1):
    measurement = Measurement(i)
    average = measurement.measure_brute_force()
    logger.info('{size},{average}'.format(
        size=i, average=average)
    )
