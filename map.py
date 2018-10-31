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

    def cost(self, source, destination):
        return self.matrix[source][destination]

    def __repr__(self):
        header = [''] + ['C{}'.format(i) for i, _ in enumerate(self.matrix)]
        matrix = [header] + self.matrix
        for i, _ in enumerate(matrix[1:]):
            matrix[i + 1] = ['C{}'.format(i)] + matrix[i + 1]
        return '\n'.join([' '.join(['%-4s' % cell for cell in row]) for row in matrix])


if __name__ == '__main__':
    city_map = Map.from_file('test_data/tsp_6_1.txt')
    print(city_map)
    print(city_map.cost(3, 5))
