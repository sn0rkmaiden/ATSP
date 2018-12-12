from atsp.algorithms.base import Solver
import random
import math
import time
import logging

logger = logging.getLogger(__name__)


class SimulatedAnnealing(Solver):

    def __init__(self, city_map, start_temperature, end_temperature, cooling_factor):
        super(SimulatedAnnealing, self).__init__(city_map)
        self.start_temperature = start_temperature * self.map.size
        self.end_temperature = end_temperature
        self.cooling_factor = cooling_factor
        self.best_solution_timestamp = None
        self.end_timestamp = None

    def solve(self, timeout=60):
        start = time.time()
        temperature = self.start_temperature
        _path = list(range(1, self.map.size))
        # random.shuffle(_path)
        current_path = [0] + _path + [0]
        current_cost = self.map.calculate_cost(current_path)
        best_path = current_path
        best_cost = current_cost
        print_timeout = 1
        last_print = start
        while temperature > self.end_temperature and time.time() - start < timeout:
            if time.time() - last_print > print_timeout:
                logger.info('Temperature: {}'.format(temperature))
                last_print = time.time()
            new_path = self.swap_random_elements(list(current_path))
            new_cost = self.map.calculate_cost(new_path)
            if new_cost < current_cost:
                if new_cost < best_cost:
                    best_path = new_path
                    best_cost = new_cost
                    self.best_solution_timestamp = time.time() - start
                current_path = new_path
                current_cost = new_cost
            else:
                probability = self.transition_probability(new_cost - current_cost, temperature)
                if self.make_transition(probability):
                    current_path = new_path
                    current_cost = new_cost
            temperature *= self.cooling_factor
        self.end_timestamp = time.time() - start
        return best_path, best_cost

    @staticmethod
    def transition_probability(delta, temperature):
        return math.exp(-delta / temperature)

    @staticmethod
    def make_transition(probability):
        return random.uniform(0, 1) <= probability

    @classmethod
    def swap_random_elements(cls, path):
        a = cls.random_path_index(path)
        b = cls.random_path_index(path)
        while a == b:
            b = cls.random_path_index(path)
        path[a], path[b] = path[b], path[a]
        return path

    @staticmethod
    def random_path_index(path):
        return random.randint(1, len(path) - 2)
