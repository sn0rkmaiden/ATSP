import logging
from abc import abstractmethod
from math import inf

logger = logging.getLogger(__name__)


class Solver(object):

    def __init__(self, city_map):
        self.map = city_map
        # logger.info('Start map:\n{}'.format(self.map))
        self.best_path = []
        self.best_cost = inf

    def reset(self):
        self.best_path, self.best_cost = [], inf

    @abstractmethod
    def solve(self, *args, **kwargs):
        self.reset()
