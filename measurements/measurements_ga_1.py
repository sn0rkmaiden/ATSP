import logging

from atsp import Map
from atsp.algorithms.genetic_algorithm import GeneticSolver

logging.basicConfig(level=logging.INFO, format='')


def new_solver(city_map):
    return GeneticSolver(city_map, population_size=50, crossover_coefficient=1, mutation_coefficient=0.2)


def small():
    city_map = Map.from_atsp('../atsp/tests/test_data/ftv47.atsp')
    solver = new_solver(city_map)
    for _ in range(10):
        solver.solve(timeout=32, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


def medium():
    city_map = Map.from_atsp('../atsp/tests/test_data/ftv170.atsp')
    solver = new_solver(city_map)
    for _ in range(10):
        solver.solve(timeout=63, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


def large():
    city_map = Map.from_atsp('../atsp/tests/test_data/rbg403.atsp')
    solver = new_solver(city_map)
    for _ in range(10):
        solver.solve(timeout=125, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


if __name__ == '__main__':
    medium()
