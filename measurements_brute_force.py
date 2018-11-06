import logging
import time

from atsp import Atsp, Map
from atsp.branch_and_bound import SolutionExplorer

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def find_first_solution(city_map, timeout):
    return SolutionExplorer(city_map).find_first_solution(timeout=timeout)


def find_best_solutions(city_map, timeout):
    return SolutionExplorer(city_map).find_best_solutions(timeout=timeout)


class Measurement(object):

    def __init__(self, size, repetitions=100, timeout=30):
        self.size = size
        self.repetitions = repetitions
        self.timeout = timeout

    def measure_brute_force(self):
        return self._measure(find_first_solution)

    def measure_best_solutions(self):
        return self._measure(find_best_solutions)

    def _measure(self, action):
        values = []
        timeouts = 0
        for _ in range(self.repetitions):
            city_map = Map.from_random_matrix(size=self.size)
            atsp = Atsp(city_map)
            start = time.time()
            try:
                atsp.brute_force()
            except TimeoutError:
                timeouts += 1
            time_taken = time.time() - start
            values.append(time_taken)
            logger.debug(time_taken)
        return sum(values) / len(values), timeouts


logger.info('Size,First average,First timeouts,Best average,Best timeouts')
for i in range(5, 40, 5):
    measurement = Measurement(i)
    average, timeouts = measurement.measure_brute_force()
    logger.info('{size},{average},{timeouts}'.format(
        size=i, average=average, timeouts=timeouts)
    )
