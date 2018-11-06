from .map import Map
from .tree import Tree
from math import inf


class Atsp(object):

    def __init__(self, city_map):
        self.city_map = city_map
        self.tree = Tree(city_map)

    def brute_force(self):
        min_cost, leaf = inf, None
        for node, cost in self.tree.traverse():
            if node.is_leaf and cost < min_cost:
                min_cost = cost
                leaf = node
        path = leaf.get_path()
        return min_cost, path

    def branch_and_bound(self):
        pass
