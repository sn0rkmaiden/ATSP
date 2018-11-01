from math import inf


class Matrix(object):

    def __init__(self, table):
        self.table = table
        self.zeros_to_infinities()

    def __getitem__(self, item):
        return self.table[item]

    def __setitem__(self, key, value):
        self.table[key] = value

    @property
    def size(self):
        return len(self.table)

    def zeros_to_infinities(self):
        for i, row in enumerate(self.table):
            for j, cell in enumerate(row):
                if not cell:
                    self.table[i][j] = inf

    def find_division_point(self):
        point, value = self._find_division_point(self.table)
        point2, value2 = self._find_division_point(self.get_inverted())
        point2.reverse()
        return point if value > value2 else point2

    @staticmethod
    def _find_division_point(table):
        min_values = [min([cell for cell in row if cell]) for row in table]
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
            self.table[i] = [cell - min_value for cell in row]
            reduction_cost += min_value
        return reduction_cost

    def __repr__(self):
        header = [''] + ['C{}'.format(i) for i, _ in enumerate(self.table)]
        matrix = [header] + self.table
        for i, _ in enumerate(matrix[1:]):
            matrix[i + 1] = ['C{}'.format(i)] + matrix[i + 1]
        return '\n'.join([' '.join(['%-4s' % cell for cell in row]) for row in matrix])


class Map(object):

    def __init__(self, matrix):
        self._matrix = matrix
        self.size = self._matrix.size

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as input_file:
            table = [
                [
                    int(cell) for cell in line.split()
                ] for line in input_file.readlines()[1:-1]
            ]
            return cls(Matrix(table))

    @property
    def cities(self):
        return list(range(self.size))

    def choose_edge(self, start, destination):
        for i in range(self.size):
            self._matrix[start][i] = inf
            self._matrix[i][destination] = inf

    def discard_edge(self, start, destination):
        self._matrix[start][destination] = inf

    def get_cost(self, source, destination):
        return self._matrix[source][destination]

    def get_costs(self, source):
        return self._matrix[source]

    def __repr__(self):
        return repr(self._matrix)
