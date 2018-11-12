import logging
import time

from atsp.algorithms.base import Solver
from atsp.map import SplitPointNotFound
from .solution import Solution

logger = logging.getLogger(__name__)


class ExpansionError(Exception):
    pass


class IncompletePathError(Exception):
    pass


class BacktrackError(Exception):
    pass


class BranchAndBoundSolver(Solver):

    def __init__(self, city_map):
        super(BranchAndBoundSolver, self).__init__(city_map)
        self.start_solution = Solution(self.map)
        self.current_solution = self.start_solution

    def solve(self, timeout=30):
        super(BranchAndBoundSolver, self).solve()
        return self._solve(exit_on_first_solution=False, timeout=timeout)

    def find_first_solution(self, timeout=30):
        self.reset()
        return self._solve(exit_on_first_solution=True, timeout=timeout)

    def _solve(self, exit_on_first_solution, timeout):
        start = time.time()
        solution_found = self.check_current_solution()
        while True:
            if time.time() - start > timeout:
                raise TimeoutError
            if solution_found and exit_on_first_solution:
                break
            try:
                self.find_next_solution_for_expansion()
            except BacktrackError:
                break
            solution_found = self.check_current_solution()
        logger.info('Found best path {} with cost {}'.format(self.best_path, self.best_cost))
        return self.best_path, self.best_cost

    def check_current_solution(self):
        try:
            self.expand_current_solution()
            self.save_current_solution()
            return True
        except (ExpansionError, IncompletePathError):
            return False

    def expand_current_solution(self):
        while not self.current_solution.is_leaf:
            if self.current_solution.lower_bound <= self.best_cost:
                try:
                    self.current_solution.expand()
                except SplitPointNotFound:
                    self.current_solution.mark_as_completed()
                    raise ExpansionError('Split point not found')
                left_bound, right_bound = self.current_solution.left.lower_bound, self.current_solution.right.lower_bound
                logger.info('Left lower bound: {}. Right lower bound: {}'.format(left_bound, right_bound))
                self.current_solution = self.current_solution.left if left_bound <= right_bound else self.current_solution.right
                logger.info('Expanded to {}'.format(self.current_solution))
            else:
                self.current_solution.mark_as_completed()
                raise ExpansionError('Lower bound exceeds best cost')
        self.current_solution.mark_as_completed()

    def save_current_solution(self):
        logger.info('Saving current solution')
        new_best_path = self.current_solution.map.path
        new_best_cost = self.current_solution.map.cost
        if len(new_best_path) < self.map.size + 1:
            raise IncompletePathError(
                'Incomplete path {} for edges {}'.format(new_best_path, self.current_solution.map.chosen_edges))
        if not self.best_cost or self.best_cost != new_best_cost:
            self.best_path = [new_best_path]
            self.best_cost = new_best_cost
        else:
            self.best_path.append(new_best_path)

    def find_next_solution_for_expansion(self):
        self.full_backtrack()
        while self.current_solution.completed or \
                self.best_cost < self.current_solution.right.lower_bound or \
                self.current_solution.right.completed:
            self.single_backtrack()
        self.current_solution.mark_as_completed()
        self.current_solution = self.current_solution.right
        logger.info('New expansion node {}'.format(self.current_solution))

    def full_backtrack(self):
        for _ in range(3):
            self.single_backtrack()

    def single_backtrack(self):
        if self.current_solution.parent:
            self.current_solution = self.current_solution.parent
            logger.info('Backtracked to {}\n{}'.format(self.current_solution.lower_bound, self.current_solution.map))
        else:
            raise BacktrackError('Reached the top of the tree')
