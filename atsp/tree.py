class Tree(object):

    def __init__(self, city_map, start_city=0):
        self.map = city_map
        self.start_node = Node(start_city)
        self._expand(self.start_node, indexes=self.map.cities, costs=self.map.get_costs(start_city))

    def _expand(self, node, indexes, costs):
        indexes.remove(node.name)
        if indexes:
            costs = [costs[i] for i in indexes]
            node.build_children(names=indexes, costs=costs)
            for child in node.children:
                self._expand(child, list(indexes), costs=self.map.get_costs(child.name))
        else:
            node.build_children(names=[0], costs=[self.map.get_cost(node.name, self.start_node.name)])

    def traverse(self, node=None, cost=0):
        node = node or self.start_node
        cost += node.parent_edge_cost
        yield node, cost
        for child in node.children:
            yield from self.traverse(child, cost)


# ROOT_EDGE = (Node(None), Node(None), 0)


class Node(object):

    def __init__(self, name):
        self.name = name
        self._parent_edge = RootEdge()
        self._child_edges = []

    def get_path(self):
        node = self
        path = [node]
        while node.parent:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

    @property
    def parent(self):
        return self._parent_edge.source if self._parent_edge.source else None

    @property
    def parent_edge_cost(self):
        return self._parent_edge.cost

    @property
    def children(self):
        return self._child_edges
        # return [edge.destination for edge in self._child_edges]

    @property
    def is_leaf(self):
        return not self._child_edges

    def set_parent(self, edge):
        self._parent_edge = edge

    def build_children(self, names, costs):
        self._child_edges = [self._create_child(name, cost) for name, cost in zip(names, costs)]

    def _create_child(self, name, cost):
        node = Node(name)
        node.set_parent(Edge(self, node, cost))
        return node
        # return Edge(self, Node(name), cost=cost)

    def __repr__(self):
        return '{}({})'.format(self.name, self._parent_edge.cost if self._parent_edge else 0)


class Edge(object):

    def __init__(self, source, destination, cost):
        # destination.set_parent(self)
        self.source = source
        self.destination = destination
        self.cost = cost


class RootEdge(Edge):

    def __init__(self):
        super(RootEdge, self).__init__(source=None, destination=None, cost=0)
