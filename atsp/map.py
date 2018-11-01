class Map(object):

    def __init__(self, matrix):
        self._matrix = matrix

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
        return list(range(len(self._matrix)))

    def get_cost(self, source, destination):
        return self._matrix[source][destination]

    def get_costs(self, source):
        return self._matrix[source]

    def __repr__(self):
        header = [''] + ['C{}'.format(i) for i, _ in enumerate(self._matrix)]
        matrix = [header] + self._matrix
        for i, _ in enumerate(matrix[1:]):
            matrix[i + 1] = ['C{}'.format(i)] + matrix[i + 1]
        return '\n'.join([' '.join(['%-4s' % cell for cell in row]) for row in matrix])
