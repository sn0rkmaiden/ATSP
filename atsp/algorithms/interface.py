from .brute_force import BruteForceSolver
from .branch_and_bound import BranchAndBoundSolver


class Atsp(object):

    def __init__(self, city_map):
        self.brute_force_solver = BruteForceSolver(city_map)
        self.branch_and_bound_solver = BranchAndBoundSolver(city_map)

    def brute_force(self):
        return self.brute_force_solver.solve()

    def branch_and_bound(self, timeout=30):
        return self.branch_and_bound_solver.solve(timeout=timeout)

    def first_branch_and_bound_solution(self, timeout=30):
        return self.branch_and_bound_solver.find_first_solution(timeout=timeout)
