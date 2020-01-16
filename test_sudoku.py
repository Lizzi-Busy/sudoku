## Run the tests by running
## pytest -v test_sudoku.py

import pytest
from sudoku_grid import *


@pytest.fixture
def solved_grid():
    grid = read_grid("Resources/grids/grid1.txt")
    return solve_sudoku(grid, next_cell, order_choices)


def test_most_constrained(solved_grid):
    assert (7,2) == most_constrained(read_grid("Resources/grids/hard1.txt")), "case 1 passed"
    assert (8,1) == most_constrained(read_grid("Resources/grids/hard2.txt")), "case 2 passed"
    with pytest.raises(ValueError):
        most_constrained(solved_grid), "should filter out all assigned cells"

def test_least_constrained(solved_grid):
    assert (2,3) == least_constrained(read_grid("Resources/grids/hard1.txt")), "case 1 passed"
    assert (3,5) == least_constrained(read_grid("Resources/grids/hard2.txt")), "case 2 passed"
    with pytest.raises(ValueError):
        least_constrained(solved_grid), "should filter out all assigned cells"

def test_ascending_order(solved_grid):
    assert [1,6,7,9] == ascending_order(read_grid("Resources/grids/hard1.txt"), (1, 2)), "case 1 passed"
    assert [4,7,9] == ascending_order(read_grid("Resources/grids/hard2.txt"), (1, 3)), "case 2 passed"
    assert [4] == ascending_order(solved_grid, (1, 1)), "single element passed"
    with pytest.raises(KeyError):
        ascending_order(solved_grid, (1,10)), "raise error if cell doesn't exist"


def test_descending_order(solved_grid):
    assert [9,7,6,1] == descending_order(read_grid("Resources/grids/hard1.txt"), (1, 2)), "case 1 passed"
    assert [9,7,4] == descending_order(read_grid("Resources/grids/hard2.txt"), (1, 3)), "case 2 passed"
    assert [4] == descending_order(solved_grid, (1, 1)), "single element passed"
    with pytest.raises(KeyError):
        descending_order(solved_grid, (1,10)), "raise error if cell doesn't exist"

def test_random_order(solved_grid):
    """test random with 0.2 tolerance level"""
    count_asc = 0
    count_des = 0
    for _ in range(10):
        if [1,6,7,9] == random_order(read_grid("Resources/grids/hard1.txt"), (1, 2)):
            count_asc += 1
        if [9,7,6,1] == random_order(read_grid("Resources/grids/hard1.txt"), (1, 2)):
            count_des += 1
    assert count_asc <= 2, "diff from ascending order"
    assert count_des <= 2, "diff from descending order"
    # edge case
    assert [4] == random_order(solved_grid, (1, 1)), "single element passed"
    with pytest.raises(KeyError):
        random_order(solved_grid, (1,10)), "raise error if cell doesn't exist"

def test_assign(solved_grid):
    assert False == assign(solved_grid, (1,1), 5), "should not assign to a cell that's already assigned"
    grid = read_grid("Resources/grids/hard1.txt")
    assert False == assign(grid, (1,2), 4), "should not assign digits not in possible_digits"
    assert False == assign(grid, (1,2), 0), "should not assign digits beyond bounds"
    # assign a digit and check that it is assigned
    new_grid = assign(grid, (1,2), 9)
    assert 9 == new_grid.cells[(1,2)].pop(), "digit is assigned"

def test_eliminate(solved_grid):
    assert False == eliminate(solved_grid, (1,1), 4), "should not remove assigned digit"
    # remove a digit and check that it is removed
    grid = read_grid("Resources/grids/hard1.txt")
    new_grid_1 = eliminate(grid, (1, 2), 2)
    assert {9,7,6,1} == new_grid_1.cells[(1, 2)], "return the original cell if digit not in possible_digits"
    new_grid_2 = eliminate(grid, (1, 2), 9)
    assert {7,6,1} == new_grid_2.cells[(1, 2)], "digit is removed"

def test_solve_sudoku(solved_grid):
    assert solved_grid == solve_sudoku(solved_grid, next_cell, order_choices), "return the grid if already solved"
    grid1 = solve_sudoku(read_grid("Resources/grids/hard1.txt"), next_cell, order_choices)
    grid2 = solve_sudoku(read_grid("Resources/grids/hard2.txt"), next_cell, order_choices)
    grid3 = solve_sudoku(read_grid("Resources/grids/grid3.txt"), next_cell, order_choices)
    assert solved(grid1) and solved(grid2) and solved(grid3), "all grids solved"
