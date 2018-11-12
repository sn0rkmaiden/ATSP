from copy import deepcopy
from math import inf


class Solution(object):

    def __init__(self, city_map, parent=None):
        self.map = city_map
        self.parent = parent
        self.left = None
        self.right = None
        self.completed = False

    @property
    def is_leaf(self):
        r = set(tuple(set(row)) for row in self.map._matrix)
        return r == {(inf,)}

    def mark_as_completed(self):
        self.completed = True

    @property
    def lower_bound(self):
        return self.map.lower_bound

    @property
    def expanded(self):
        return self.left and self.right

    def expand(self):
        point = self.map.find_split_point()
        left_map, right_map = deepcopy(self.map), deepcopy(self.map)
        left_map.choose_edge(*point)
        right_map.discard_edge(*point)
        self.left = Solution(left_map, parent=self)
        self.right = Solution(right_map, parent=self)

    def __repr__(self):
        return 'Lower bound: {}, chosen edges {}, discarded edges {}, map:\n{}'.format(
            self.lower_bound, self.map.chosen_edges, self.map.discarded_edges, self.map
        )
