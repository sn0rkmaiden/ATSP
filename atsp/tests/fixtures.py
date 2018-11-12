import os

import pytest

from atsp import Map, Atsp


@pytest.fixture
def city_map(test_set):
    test_set_path = os.path.join(os.path.dirname(__file__), 'test_data', '{}.txt'.format(test_set))
    return Map.from_file(test_set_path)


@pytest.fixture
def solver(city_map):
    return Atsp(city_map)
