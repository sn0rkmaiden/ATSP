from atsp import Atsp, Map
from atsp.branch_and_bound import SolutionExplorer, Solution
import logging
import time
# logging.basicConfig(level=logging.INFO)

start = time.time()
city_map = Map.from_file('atsp/tests/test_data/tsp_17.txt')
path, cost = SolutionExplorer(city_map).find_first_solution()
print(path, cost)
end = time.time()
print(end - start)
