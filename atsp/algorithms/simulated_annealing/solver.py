from atsp.algorithms.base import Solver
import random
import math


class SimulatedAnnealing(Solver):

    def __init__(self, city_map, start_temperature=10*40, end_temperature=0.1, cooling_factor=0.999):
        self.start_temperature = start_temperature
        self.end_temperature = end_temperature
        self.cooling_factor = cooling_factor
        super(SimulatedAnnealing, self).__init__(city_map)

    def solve(self):
        temperature = self.start_temperature
        current_path = list(range(self.map.size)) + [0]
        current_cost = self.map.calculate_cost(current_path)
        best_path = current_path
        best_cost = current_cost
        while temperature > self.end_temperature:
            new_path = self.swap_random_elements(list(current_path))
            new_cost = self.map.calculate_cost(new_path)
            if new_cost < current_cost:
                if new_cost < best_cost:
                    best_path = new_path
                    best_cost = new_cost
                current_path = new_path
                current_cost = new_cost
            else:
                probability = self.transition_probability(new_cost - current_cost, temperature)
                if self.make_transition(probability):
                    current_path = new_path
                    current_cost = new_cost
            temperature *= self.cooling_factor
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
