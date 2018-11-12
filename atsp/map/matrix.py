import logging
from math import inf

logger = logging.getLogger(__name__)


class SplitPointNotFound(Exception):
    pass


class Matrix(object):

    def __init__(self, table):
        self.table = table
        self.prepare_diagonal()

    def __getitem__(self, item):
        return self.table[item]

    def __setitem__(self, key, value):
        self.table[key] = value

    @property
    def size(self):
        return len(self.table)

    def prepare_diagonal(self):
        for i in range(self.size):
            self.table[i][i] = inf

    def check_point_for_cycle(self, point, chosen_edges):
        new_chosen_edges = chosen_edges + [point]
        paths = self.build_total_paths(new_chosen_edges)
        for path in paths:
            if len(path) < len(self.table) + 1 and path[0] == path[-1]:
                logger.debug('Point {} forms a cycle in path {}'.format(point, path))
                return True
        return False

    def build_total_paths(self, chosen_edges):
        paths = [self._build_total_path([i], list(chosen_edges)) for i in range(self.size)]
        return [path for path in paths if len(path) > 1]

    def _build_total_path(self, path, edges):
        for i, edge in enumerate(edges):
            if edge[0] == path[-1]:
                path.append(edges.pop(i)[1])
                return self._build_total_path(path, edges)
        return path

    def find_split_point(self, chosen_edges):
        max_reduction_cost = -1
        point = None
        inverted = self.get_inverted()
        for i, row in enumerate(self.table):
            for j, column in enumerate(inverted):
                if self.table[i][j] == 0:
                    reduction_cost = self._reduction_cost(row, j) + self._reduction_cost(column, i)
                    possible_point = [i, j]
                    if reduction_cost >= max_reduction_cost and not self.check_point_for_cycle(possible_point,
                                                                                               chosen_edges):
                        logger.info('Reduction cost {} for point {}'.format(reduction_cost, possible_point))
                        max_reduction_cost = reduction_cost
                        point = possible_point
        if point:
            return point
        else:
            raise SplitPointNotFound(self)

    @staticmethod
    def _reduction_cost(row, index):
        row = list(row)
        del row[index]
        return min(row)

    @staticmethod
    def _find_division_point(table):
        min_values = [min([cell for cell in row if cell]) for row in table]
        min_values = [0 if value == inf else value for value in min_values]
        max_min_value = max(min_values)
        row_index = min_values.index(max_min_value)
        column_index = table[row_index].index(0)
        return [row_index, column_index], max_min_value

    def invert(self):
        self.table = self.get_inverted()

    def get_inverted(self):
        return [list(row) for row in zip(*self.table)]

    def reduce(self):
        reduction_cost = self.reduce_rows()
        self.invert()
        reduction_cost += self.reduce_rows()
        self.invert()
        return reduction_cost

    def reduce_rows(self):
        reduction_cost = 0
        for i, row in enumerate(self.table):
            min_value = min(row)
            if min_value == inf:
                continue
            self.table[i] = [cell - min_value for cell in row]
            reduction_cost += min_value
        return reduction_cost

    def __repr__(self):
        header = [''] + ['C{}'.format(i) for i, _ in enumerate(self.table)]
        matrix = [header] + self.table
        for i, _ in enumerate(matrix[1:]):
            matrix[i + 1] = ['C{}'.format(i)] + matrix[i + 1]
        return '\n'.join([' '.join(['%-4s' % cell for cell in row]) for row in matrix])
