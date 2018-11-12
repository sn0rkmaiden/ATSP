import pytest

from .fixtures import solver, city_map


@pytest.mark.parametrize(
    'test_set,expected_path,expected_cost',
    [
        ('tsp_6_1', [0, 1, 2, 3, 4, 5, 0], 132),
        ('tsp_6_2', [0, 5, 1, 2, 3, 4, 0], 80),
        ('tsp_10', [0, 3, 4, 2, 8, 7, 6, 9, 1, 5, 0], 212)
    ])
def test_brute_force(expected_path, expected_cost, solver):
    paths, cost = solver.brute_force()
    assert cost == expected_cost
    assert expected_path in paths
