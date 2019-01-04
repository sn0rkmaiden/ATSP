from .brute_force import BruteForceSolver
from .branch_and_bound import BranchAndBoundSolver
from .simulated_annealing import SimulatedAnnealing
from .genetic_algorithm import GeneticSolver


class Atsp(object):

    def __init__(self, city_map):
        self.city_map = city_map

    def brute_force(self):
        return BruteForceSolver(self.city_map).solve()

    def simulated_annealing(self, end_temperature=0, cooling_factor=0.999, timeout=30):
        return SimulatedAnnealing(self.city_map, cooling_factor, end_temperature)\
            .solve(timeout=timeout)

    def genetic_algorithm(self, population_size, crossover_coefficient=0.8, mutation_coefficient=0.1, timeout=30):
        return GeneticSolver(self.city_map, population_size, crossover_coefficient=crossover_coefficient,
                             mutation_coefficient=mutation_coefficient).solve(timeout=timeout)

    def branch_and_bound(self, timeout=30):
        return BranchAndBoundSolver(self.city_map).solve(timeout=timeout)

    def first_branch_and_bound_solution(self, timeout=30):
        return BranchAndBoundSolver(self.city_map).find_first_solution(timeout=timeout)
