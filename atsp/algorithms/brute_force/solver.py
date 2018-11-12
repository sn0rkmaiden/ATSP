from atsp.algorithms.base import Solver
from .utils import permutations


class BruteForceSolver(Solver):

    def solve(self):
        super(BruteForceSolver, self).solve()
        elements = list(range(1, self.map.size))
        for permutation in permutations(elements):
            path = [0] + permutation + [0]
            new_cost = self.map.calculate_cost(path)
            if new_cost < self.best_cost:
                self.best_cost = new_cost
                self.best_path = [path]
            elif new_cost == self.best_cost:
                self.best_path.append(path)
        return self.best_path, self.best_cost
