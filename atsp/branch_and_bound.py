from copy import deepcopy
from math import inf
import logging

logger = logging.getLogger(__name__)
class ExpansionError(Exception):
    pass


class Solution(object):

    def __init__(self, city_map, parent=None):
        self.map = city_map
        self.parent = parent
        self.left = None
        self.right = None
        self.discarded = False
        self.max_depth = len(self.map.cities)
        self.depth = self.parent.depth + 1 if self.parent else 0

    @property
    def is_leaf(self):
        r = set(tuple(set(row)) for row in self.map._matrix)
        # print(r)
        return r == {(inf,)}#self.depth == self.max_depth

    def discard(self):
        self.discarded = True

    @property
    def lower_bound(self):
        return self.map.lower_bound

    @property
    def expanded(self):
        return self.left and self.right

    def expand(self):
        # print(self.map)
        point = self.map.find_division_point()
        if not point:
            raise ExpansionError('Expansion limit reached:\n{}'.format(self))
        left_map, right_map = deepcopy(self.map), deepcopy(self.map)
        left_map.choose_edge(*point)
        right_map.discard_edge(*point)
        self.left = Solution(left_map, parent=self)
        self.right = Solution(right_map, parent=self)

    def __repr__(self):
        return 'Lower bound: {}, chosen edges {}, discarded edges {}, map:\n{}'.format(
            self.lower_bound, self.map.chosen_edges, self.map.discarded_edges, self.map
        )

class BacktrackError(Exception):
    pass


class SolutionExplorer(object):

    def __init__(self, city_map):
        self.map = city_map
        logger.info('Start map:\n{}'.format(city_map))
        self.start_solution = Solution(self.map)
        self.current_solution = self.start_solution
        self.best_path = []
        self.best_cost = inf

    def find_all_solutions(self):
        return self._solve(exit_on_first_solution=False)

    def solve(self):
        return self._solve(exit_on_first_solution=True)

    def _solve(self, exit_on_first_solution):
        self.dig_left()
        # self.find_next_possible_solution()
        while True:
            if self.best_path and exit_on_first_solution:
                break
            try:
                self.find_next_possible_solution()
            except BacktrackError:
                break
            self.dig_left()
        return self.best_path, self.best_cost

    def dig_left(self):
        # for _ in self.map.cities:
        #     self.current_solution.expand()
        #     self.current_solution = self.current_solution.left
        while not self.current_solution.is_leaf:
            # print(self.current_solution.depth)
            # print(self.current_solution.map)
            if not self.best_cost or self.current_solution.lower_bound <= self.best_cost:
                try:
                    self.current_solution.expand()
                except ExpansionError:
                    return
                if self.current_solution.left.lower_bound <= self.current_solution.right.lower_bound:

                    self.current_solution = self.current_solution.left
                else:
                    self.current_solution = self.current_solution.right
                logger.info('Expanded to {}'.format(self.current_solution))
            else:
                return
        # self.current_solution.discard()
        if not self.current_solution.is_leaf:
            return
        logger.info('Saving current solution')
        # self.current_solution.map.chosen_edges.remove([13, 0])
        new_best_path = self.current_solution.map.build_total_path()
        new_best_cost = self.current_solution.map.total_path_cost
        if len(new_best_path) < self.map.size + 1:
            # logger.warning('Incomplete path {} for edges {}'.format(new_best_path, self.current_solution.map.chosen_edges))
            return
        if not self.best_cost or self.best_cost != new_best_cost:
            self.best_path = [new_best_path]
            self.best_cost = new_best_cost
        else:
            self.best_path.append(new_best_path)

    def find_next_possible_solution(self):
        self.backtrack()
        self.backtrack()
        self.backtrack()
        while self.current_solution.discarded or \
            self.best_cost < self.current_solution.right.lower_bound or self.current_solution.right.discarded:
            self.backtrack()
        self.current_solution.discard()
        self.current_solution = self.current_solution.right
        logger.info('New expansion node {}'.format(self.current_solution))

    def backtrack(self):
        if self.current_solution.parent:
            self.current_solution = self.current_solution.parent
            logger.info('Backtracked to {}\n{}'.format(self.current_solution.lower_bound, self.current_solution.map))
        else:
            raise BacktrackError('Reached the top of the tree')
