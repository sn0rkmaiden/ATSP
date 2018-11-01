class Solution(object):

    def __init__(self, map, discarded_edges, chosen_edges):
        self.map = map
        self.discarded_edges = discarded_edges
        self.chosen_edges = chosen_edges
        self.left = None
        self.right = None
        self._expanded = False

    def expand(self):
