from atsp.algorithms.base import Solver
from atsp.algorithms.common import MeasurementLog
from pprint import pformat
import random
import time
import logging


logger = logging.getLogger(__name__)


def swap_random_elements(path):
    a = random_path_index(path)
    b = random_path_index(path)
    while a == b:
        b = random_path_index(path)
    path[a], path[b] = path[b], path[a]
    return path


def random_path_index(path):
    return random.randint(1, len(path) - 2)


class Chromosome(object):

    def __init__(self, city_map, path):
        self.map = city_map
        self.path = path
        self.cost = self.map.calculate_cost(self.path)
        self.crossed_with = []

    def mutual_crossover(self, other):
        offspring_1 = self.cross(other)
        offspring_2 = other.cross(self)
        return offspring_1, offspring_2

    def cross(self, other):
        self.crossed_with.append(other)
        # split_index = self.map.size // 2
        split_index = random.randint(1, self.map.size - 1)
        my_part = self.path[1:split_index]
        other_part = [city for city in other.path[1:-1] if city not in my_part]
        offspring = [0] + my_part + other_part + [0]
        return Chromosome(self.map, offspring)

    def mutate(self):
        self.path = swap_random_elements(self.path)
        self.cost = self.map.calculate_cost(self.path)

    @staticmethod
    def random_path_index(path):
        return random.randint(1, len(path) - 2)

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.path == other.path

    def __hash__(self):
        return hash(repr(self.path))

    def __repr__(self):
        return f'Path {self.path} costs {self.cost}'


class GeneticSolver(Solver):

    def __init__(self, city_map, population_size, crossover_coefficient, mutation_coefficient):
        super(GeneticSolver, self).__init__(city_map)
        self.population_size = population_size
        self.crossover_coefficient = crossover_coefficient
        self.mutation_coefficient = mutation_coefficient
        self.population = self.initial_population()
        self.population_index = 0
        self.log = MeasurementLog()

    def initial_population(self):
        population = [Chromosome(self.map, self.random_path()) for _ in range(self.population_size)]
        population.sort()
        logger.debug('Generated population:\n{}'.format(pformat(population)))
        logger.info(f'Population max: {population[0]}')
        return population

    def breed(self):
            # logger.info(f'{len(offsprings)} offsprings, generating...')
        offsprings = self.generate_offsprings()
        self.add_mutations(offsprings)
        offsprings = list(set(offsprings))
        offsprings.sort()
        self.population = offsprings[:min(len(offsprings), self.population_size)]
        self.population_index += 1
        logger.debug(f'New population:\n{pformat(self.population)}')
        if self.population:
            logger.debug(f'New population max: {self.population[0]}')

    def add_mutations(self, offsprings):
        for offspring in offsprings:
            if random.uniform(0, 1) < self.mutation_coefficient:
                offspring.mutate()
        logger.debug(f'Mutated offsprings:\n{pformat(offsprings)}')
        
    def generate_offsprings(self):
        mates_per_chromosome = int(self.crossover_coefficient * (self.map.size - 1)) or 1
        offsprings = []
        for i, chromosome in enumerate(self.population):
            potential_mates = list(self.population)
            del potential_mates[i]
            for j, mate in enumerate(potential_mates):
                if len(chromosome.crossed_with) == mates_per_chromosome:
                    break
                if chromosome not in mate.crossed_with and len(mate.crossed_with) < mates_per_chromosome:
                    offsprings += list(chromosome.mutual_crossover(mate))
        # offsprings = list(set(offsprings))
        # offsprings.sort()
        logger.debug(f'Generated offsprings:\n{pformat(offsprings)}')
        # self.population = offsprings[:self.population_size]
        return offsprings

    def random_path(self):
        return [0] + random.sample(range(1, self.map.size), self.map.size - 1) + [0]

    def solve(self, timeout=60, print_timeout=5):
        self.population = self.initial_population()
        self.population_index = 0
        start_time = time.time()
        end_time = time.time() + timeout
        best_path, best_cost = None, None
        last_print = start_time
        logger.info('Timestamp,Best cost,Population')
        while time.time() < end_time and self.population:
            if time.time() - last_print > print_timeout:
                last_print = time.time()
                time_elapsed = round(last_print - start_time)
                self.log.add(time_elapsed, self.population_index, best_cost)
                logger.info('{},{},{}'.format(time_elapsed, best_cost, self.population_index))
            best_offspring = self.population[0]
            if not best_cost or best_cost > best_offspring.cost:
                best_cost = best_offspring.cost
                # logger.info(f'Best cost: {best_cost}')
                best_path = best_offspring.path
                best_solution_timestamp = time.time() - start_time
            self.breed()
        self.log.add_best(timestamp=best_solution_timestamp, cost=best_cost, path=best_path)
        return best_path, best_cost

