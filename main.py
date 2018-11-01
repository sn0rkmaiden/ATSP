from atsp import Atsp, Map
import cProfile

city_map = Map.from_file('test_data/tsp_3_1.txt')
reduction_cost = city_map._matrix.reduce()
point = city_map._matrix.find_division_point()
# print(reduction_cost)
print(point)
print(city_map)
city_map.choose_edge(*point)
print(city_map)
# atsp = Atsp('test_data/tsp_12.txt')
# # cProfile.run('atsp.brute_force()')
# min_cost, path = atsp.brute_force()
# print(min_cost)
# print(path)

