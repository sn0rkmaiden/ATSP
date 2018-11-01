from atsp import Atsp
import cProfile

atsp = Atsp('test_data/tsp_12.txt')
# cProfile.run('atsp.brute_force()')
min_cost, path = atsp.brute_force()
print(min_cost)
print(path)

