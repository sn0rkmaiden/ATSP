import logging

from atsp import Map
from atsp.algorithms.simulated_annealing import SimulatedAnnealing

logging.basicConfig(level=logging.INFO, format='')


def small():
    city_map = Map.from_atsp('atsp/tests/test_data/ftv47.atsp')
    solver = SimulatedAnnealing(city_map, cooling_factor=0.99997)
    for _ in range(10):
        solver.solve(timeout=31, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


def medium():
    city_map = Map.from_atsp('atsp/tests/test_data/ftv170.atsp')
    solver = SimulatedAnnealing(city_map, cooling_factor=0.999)
    for _ in range(10):
        solver.solve(timeout=61, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


def large():
    city_map = Map.from_atsp('atsp/tests/test_data/rbg403.atsp')
    solver = SimulatedAnnealing(city_map, cooling_factor=0.999)
    for _ in range(10):
        solver.solve(timeout=121, print_timeout=5)

    print(solver.log.time_summary())
    print(solver.log.best_summary())


if __name__ == '__main__':
    large()
