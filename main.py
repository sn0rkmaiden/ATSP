from atsp import Atsp, Map
from atsp.branch_and_bound import SolutionExplorer, Solution
# import cProfile
import logging
import time

start = time.time()
logging.basicConfig(level=logging.INFO)
city_map = Map.from_file('atsp/tests/test_data/tsp_12.txt')
# reduction_cost = city_map._matrix.reduce()
# point = city_map._matrix.find_division_point()
# print(reduction_cost)
# print(point)
# print(city_map)
# city_map.choose_edge(*point)
# print(city_map)
path, cost = SolutionExplorer(city_map).solve()
print(path, cost)
end = time.time()
print(end-start)
# solution = Solution(city_map)
# for _ in city_map.cities[:]:
#     solution.expand()
#     solution = solution.left
    # print(s1.left.left.left.left.map)
# print(solution.map.total_path_cost)
# print(solution.map.chosen_edges)
    # atsp = Atsp('test_data/tsp_12.txt')
    # # cProfile.run('atsp.brute_force()')
    # min_cost, path = atsp.brute_force()
    # print(min_cost)
    # print(path)

