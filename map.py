class Map(object):

    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as input_file:
            matrix = [
                [
                    int(cell) for cell in line.split()
                ] for line in input_file.readlines()[1:-1]
            ]
            return cls(matrix)

    @property
    def cities(self):
        return list(range(len(self.matrix)))

    def cost(self, source, destination):
        return self.matrix[source][destination]

    def get_costs(self, source):
        return self.matrix[source]

    def __repr__(self):
        header = [''] + ['C{}'.format(i) for i, _ in enumerate(self.matrix)]
        matrix = [header] + self.matrix
        for i, _ in enumerate(matrix[1:]):
            matrix[i + 1] = ['C{}'.format(i)] + matrix[i + 1]
        return '\n'.join([' '.join(['%-4s' % cell for cell in row]) for row in matrix])


class Tree(object):

    def __init__(self, city_map):
        self.map = city_map
        self.start_node = Node(0)
        self.expand(self.start_node, indexes=self.map.cities, costs=self.map.get_costs(0))

    def expand(self, node, indexes, costs):
        indexes.remove(node.name)
        if indexes:
            costs = [costs[i] for i in indexes]
            node.build_children(names=indexes, costs=costs)
            for child in node.children:
                self.expand(child, list(indexes), costs=self.map.get_costs(child.name))
        else:
            node.build_children(names=[0], costs=[self.map.cost(node.name, self.start_node.name)])

    def traverse(self, node=None, cost=0):
        node = node or self.start_node
        cost += node.parent_edge_cost
        yield node, cost
        for child in node.children:
            yield from self.traverse(child, cost)


class Node(object):

    def __init__(self, name):
        self.name = name
        self._parent_edge = None
        self._child_edges = []

    @property
    def parent(self):
        return self._parent_edge.source if self._parent_edge else None

    @property
    def parent_edge_cost(self):
        return self._parent_edge.cost if self._parent_edge else 0

    @property
    def children(self):
        return [edge.destination for edge in self._child_edges]

    @property
    def is_leaf(self):
        return not self._child_edges

    def set_parent(self, edge):
        self._parent_edge = edge

    def build_children(self, names, costs):
        self._child_edges = [self.create_child(name, cost) for name, cost in zip(names, costs)]

    def create_child(self, name, cost):
        return Edge(self, Node(name), cost=cost)

    def __repr__(self):
        return '{}({})'.format(self.name, self._parent_edge.cost if self._parent_edge else 0)


class Edge(object):

    def __init__(self, source, destination, cost):
        destination.set_parent(self)
        self.source = source
        self.destination = destination
        self.cost = cost


if __name__ == '__main__':
    city_map = Map.from_file('test_data/tsp_10.txt')
    print(city_map)
    # print(city_map.cost(3, 5))
    tree = Tree(city_map)
    min_path = None
    leaf = None
    for node, cost in tree.traverse():
        # print( node, node.is_leaf, cost)
        if node.is_leaf:
            old_min_path = min_path
            min_path = min(min_path, cost) if min_path else cost
            if old_min_path != min_path:
                leaf = node
    while leaf.parent:
        print(leaf)
        leaf = leaf.parent
    print(min_path)
