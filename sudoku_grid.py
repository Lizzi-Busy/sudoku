"""
Represent a Sudoku grid, read one from a file, and solve with backtracking.

The grid is represented as a Sudoku object with a few fields:

- `cells` is a dictionary whose keys are cell coordinates and whose values are
  sets of possible values for that cell. Hence `grid.cells[(1,1)]` is the set
  of possible values for the top left cell.
- `peers` is a dictionary whose keys are cell coordinates and whose values are
  sets of coordinates of peers for each cell.
- `n` is the block size of the grid. A 9 x 9 Sudoku grid has n = 3, since each
  block is 3 x 3.
"""

import math
from random import shuffle
from sudoku_grid_util import *


#################### STEP 1 ####################

def most_constrained(grid):
    """pick the cell with the fewest possible digits"""
    d = grid[0]
    # filter out assigned cells
    key_list = list(filter(lambda key: len(d[key])>1, d))
    count_list = list(map(lambda k: len(d[k]), key_list))
    i = count_list.index(min(count_list))
    return key_list[i]
    

def least_constrained(grid):
    """pick the cell with the most possible digits"""
    d = grid[0]
    # filter out assigned cells
    key_list = list(filter(lambda key: len(d[key])>1, d))
    count_list = list(map(lambda k: len(d[k]), key_list))
    i = count_list.index(max(count_list))
    return key_list[i]


def next_cell(grid):
    """decide the coordinates of the cell we should fill in next"""
    return most_constrained(grid)


def ascending_order(grid, cell):
    return sorted(grid[0][cell])


def descending_order(grid, cell):
    return sorted(grid[0][cell], reverse=True)


def random_order(grid, cell):
    l = list(grid[0][cell])
    shuffle(l)
    return l


def order_choices(grid, next_idx):
    """give an ordered list of the possible values in a cell"""
    return smallest_first(grid, next_idx)


def solve_sudoku(grid, next_cell, order_choices):
    """Solve a Sudoku grid via backtracking.

    If the grid cannot be solved, return False.

    grid: A Sudoku object returned from `parse_grid`
    next_cell: A function that takes the current grid and returns the
        coordinates of the cell we should fill in next
    order_choices: A function that takes the current grid and the coordinates
        of the cell chosen to fill in next, and returns an ordered list of the
        values that should be tried in that cell
    """

    if grid == False:
        ## must have died earlier
        return False

    if solved(grid):
        ## This is a solution. We win.
        return grid

    next_idx = next_cell(grid)
    choices = order_choices(grid, next_idx)

    for choice in choices:
        new_grid = assign(grid, next_idx, choice)
        outcome = solve_sudoku(new_grid, next_cell, order_choices)
        if outcome != False:
            return outcome

    return False

        

#################### STEP 2 ####################

def assign(grid, cell, digit):
    """Return a new grid with cell assigned to be a certain digit.

    Works by using `eliminate()` to remove all other values and propagate the
    constraint to peer cells. Returns False if assigning this value leads to a
    contradiction and is impossible, otherwise returns the new grid.
    """

    grid = grid.copy()

    cur_digits = grid.cells[cell]

    other_values = cur_digits - {digit}

    ## eliminate all other values from this cell

    if grid == False:
        return False
    else:
        for d in other_values:
            grid = eliminate(grid, cell, d)

    return grid


def eliminate(grid, cell, digit):
    """Eliminate `digit` from the possible values of `cell`.

    Destructively modifies the grid passed in. Returns False if removing this
    digit leaves the cell with no other possible values, meaning the grid is
    unsolvable, otherwise returns the grid.
    """

    if grid == False:
        ## current grid is impossible
        return False

    possible_digits = grid.cells[cell]

    if digit not in possible_digits:
        ## This value was already eliminated.
        return grid

    new_digits = possible_digits - {digit}
    grid.cells[cell] = new_digits

    if len(new_digits) == 0:
        ## We've eliminated the only possible value for this cell. Abort.
        return False
    elif len(new_digits) == 1:
        ## propagate constraints to peer cells
        for peer in grid.peers[cell]:
            grid = eliminate(grid, peer, list(new_digits)[0])

    return grid


##################### STOP HERE #####################
## Functions below are for reference

def read_grid(filename):
    """Read a grid from a file and return the Sudoku object."""
    f = open(filename, "r")

    grid = list(map(lambda line: [int(c) if c != "0" else None
                                  for c in line[:-1]],
                    f))

    return parse_grid(grid)

def count_calls(fn):
    """Takes a function and return a new function that counts calls to itself.

    The number of calls is tracked in a `.calls` property of the function.
    The new function must have the same name as the old, so the old recurses
    into it correctly.

    For example:

    solve_sudoku = count_calls(solve_sudoku)
    solve_sudoku(grid, most_constrained, smallest_first)
    solve_sudoku.calls #=> number of calls

    solve_sudoku.calls = 0 # resets count
    """

    def counter(*args, **kwargs):
        counter.calls += 1
        return fn(*args, **kwargs)

    counter.calls = 0

    return counter

def solved(grid):
    """Test if all values have been filled in.

    A grid is solved if all cells have only one possible value."""

    return all(len(vals) == 1 for vals in grid.cells.values())

def parse_grid(grid_rows):
    """Take a read-in grid and turn it into a Sudoku object.

    Takes the list of lines from `read_grid` and an empty Sudoku object,
    then assigns each cell the correct values.
    """

    n = int(math.sqrt(len(grid_rows)))

    assert n**2 == len(grid_rows), "Side length must be square of block size"

    new_grid = empty_grid(n)

    for row, cols in enumerate(grid_rows, 1):
        for col, val in enumerate(cols, 1):
            if val is not None:
                new_grid = assign(new_grid, (row, col), val)

    if new_grid == False:
        return False

    return new_grid


# SAMPLE OUTPUT
# grid = read_grid("Resources/grids/hard1.txt")
# solve_sudoku = count_calls(solve_sudoku)
# solve_sudoku(grid, most_constrained, ascending_order)
# most_con = solve_sudoku.calls
# print(most_con)
# solve_sudoku.calls = 0 # resets count
