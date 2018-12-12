from atsp import Map
from atsp.algorithms.simulated_annealing.solver import SimulatedAnnealing
import logging
import time
from pprint import pformat

logging.basicConfig(level=logging.ERROR, format='')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class Measurement(object):

    def __init__(self, file_path, known_best_value, cooling_factor, repetitions=10, timeout=30):
        city_map = Map.from_atsp(file_path)
        self.known_best_value = known_best_value
        self.solver = SimulatedAnnealing(city_map, 9000, 0.1, cooling_factor=cooling_factor)
        self.repetitions = repetitions
        self.timeout = timeout

    def measure(self):
        values = []
        for _ in range(self.repetitions):
            path, cost = self.solver.solve(self.timeout)
            values.append({
                'cost': cost,
                'error': round((cost - self.known_best_value) / self.known_best_value, 5),
                'best_time': round(self.solver.best_solution_timestamp, 3),
                'total_time': round(self.solver.end_timestamp, 3),
                'path': path
            })
            logger.info('{cost}\t{error}\t{best_time}\t{total_time}\t{path}'.format(**values[-1]))
            # logger.debug(time_taken)
        return values


logger.info('ftv47.atsp 20 sec')
logger.info('Cost\tError\tFound at\tTotal time\tPath')
measurement = Measurement('../atsp/tests/test_data/ftv47.atsp', known_best_value=1776,
                          cooling_factor=0.99996, timeout=9000)  # 20 seconds
measurement.measure()

logger.info('ftv170.atsp 60 sec')
logger.info('Cost\tError\tFound at\tTotal time\tPath')
measurement = Measurement('../atsp/tests/test_data/ftv170.atsp', known_best_value=2755,
                          cooling_factor=0.99995, timeout=9000)
measurement.measure()

logger.info('rbg403.atsp 40 sec')
logger.info('Cost\tError\tFound at\tTotal time\tPath')
measurement = Measurement('../atsp/tests/test_data/rbg403.atsp', known_best_value=2465,
                          cooling_factor=0.99994, timeout=9000)
measurement.measure()