from copy import deepcopy


class ExpansionError(Exception):
    pass


class Solution(object):

    def __init__(self, city_map):
        self.map = city_map
        self.left = None
        self.right = None

    @property
    def expanded(self):
        return self.left and self.right

    def expand(self):
        # print(self.map)
        point = self.map.find_division_point()
        if not point:
            raise ExpansionError('Expansion limit reached:\n{}'.format(self.map))
        left_map, right_map = deepcopy(self.map), deepcopy(self.map)
        left_map.choose_edge(*point)
        right_map.discard_edge(*point)
        self.left = Solution(left_map)
        self.right = Solution(right_map)


class SolutionExplorer(object):

    def __init__(self, city_map):
        self.map = city_map
        self.start_solution = Solution(self.map)
        self.current_solution = self.start_solution
        self.best_path = None
        self.best_cost = None

    def solve(self):
        self.expand()
        return self.best_path, self.best_cost

    def expand(self):
        for _ in self.map.cities:
            self.current_solution.expand()
            self.current_solution = self.current_solution.left
        self.best_path = self.current_solution.map.build_total_path()
        self.best_cost = self.current_solution.map.total_path_cost
