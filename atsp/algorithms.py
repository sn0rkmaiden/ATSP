from .map import Map
from .tree import Tree
from math import inf


class MapBuilder(object):

    def build(self, file_path):
        return Map.from_file(file_path)


class TreeBuilder(object):

    def build(self, city_map):
        return Tree(city_map)


class Atsp(object):

    def __init__(self, file_path, map_builder=MapBuilder(), tree_builder=TreeBuilder()):
        city_map = map_builder.build(file_path)
        self.tree = tree_builder.build(city_map)

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
