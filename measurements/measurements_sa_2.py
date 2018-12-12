from atsp import Map
from atsp.algorithms.simulated_annealing.solver import SimulatedAnnealing
import logging
import time
from pprint import pformat
import math
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
                'total_time': round(self.solver.end_timestamp, 3)
            })
            # logger.info('{cost}\t{error}\t{best_time}\t{total_time}'.format(**values[-1]))
            # logger.debug(time_taken)
        values = {k: [dic[k] for dic in values] for k in values[0]}
        return {
                'cost': round(sum(values['cost'])/len(values['cost'])),
                'error': round(sum(values['error'])/len(values['error']), 5),
                'best_time': round(sum(values['best_time'])/len(values['best_time']), 3),
                'total_time': round(sum(values['total_time'])/len(values['total_time']), 3),
            }


logger.info('Cooling factor\tCost\tError\tFound at\tTotal time')
for i in range(10):
    cooling_factor = 0.99 + i/1000
    measurement = Measurement('../atsp/tests/test_data/ftv47.atsp', known_best_value=1776,
                              cooling_factor=cooling_factor, timeout=9000)  # 20 seconds
    result = measurement.measure()
    logger.info('{cooling_factor}\t{cost}\t{error}\t{best_time}\t{total_time}'.format(cooling_factor=cooling_factor,
                                                                                      **result))
