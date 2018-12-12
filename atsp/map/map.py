import logging
from copy import deepcopy
from math import inf
from random import randint

from .matrix import Matrix

logger = logging.getLogger(__name__)


class Map(object):

    def __init__(self, matrix):
        logger.info('Created map from matrix:\n{}'.format(matrix))
        self.original_matrix = deepcopy(matrix)
        self._matrix = matrix
        self.size = self._matrix.size
        self.discarded_edges = []
        self.chosen_edges = []
        self.lower_bound = 0
        self._update_lower_bound()

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as input_file:
            table = [
                [
                    int(cell) for cell in line.split()
                ] for line in input_file.readlines()[1:-1]
            ]
            return cls(Matrix(table))

    @classmethod
    def from_atsp(cls, file_path):
        with open(file_path, 'r') as input_file:
            dimension = None
            while not dimension:
                line = input_file.readline()
                if line.startswith('DIMENSION'):
                    dimension = int(line.split(' ')[1])
            while not input_file.readline().startswith('EDGE_WEIGHT_SECTION'):
                pass
            table = []
            current_row = []
            current_line = input_file.readline()
            while not current_line.startswith('EOF'):
                current_row += [int(cell) for cell in current_line.split()]
                current_line = input_file.readline()
                if len(current_row) >= dimension:
                    row = current_row[:dimension]
                    current_row = current_row[dimension:]
                    table.append(row)
            return cls(Matrix(table))

    @classmethod
    def from_random_matrix(cls, size, min_value=0, max_value=100):
        table = [
            [
                randint(min_value, max_value) for _ in range(size)
            ] for _ in range(size)
        ]
        return cls(Matrix(table))

    @property
    def cost(self):
        return self.calculate_cost(self.path)

    def calculate_cost(self, path):
        cost = 0
        for i, city in enumerate(path[:-1]):
            next_city = path[i + 1]
            cost += self.original_matrix[city][next_city]
        return cost

    @property
    def path(self):
        return self._build_path([0], list(self.chosen_edges))

    @classmethod
    def _build_path(cls, path, edges):
        for i, edge in enumerate(edges):
            if edge[0] == path[-1]:
                path.append(edges.pop(i)[1])
                return cls._build_path(path, edges)
        return path

    def find_split_point(self):
        return self._matrix.find_split_point(self.chosen_edges)

    def choose_edge(self, start, destination):
        for i in range(self.size):
            self._matrix[start][i] = inf
            self._matrix[i][destination] = inf
        self._matrix[destination][start] = inf
        self.chosen_edges.append([start, destination])
        self._update_lower_bound()

    def discard_edge(self, start, destination):
        self._matrix[start][destination] = inf
        self.discarded_edges += [start, destination]
        self._update_lower_bound()

    def _update_lower_bound(self):
        self.lower_bound += self._matrix.reduce()

    def __repr__(self):
        return repr(self._matrix)
