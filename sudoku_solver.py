# 3 kyu
"""Write a function, called "sudoku", that will solve a 9x9 Sudoku puzzle. The function will take one 
argument consisting of the 2D puzzle array, with the value 0 representing an unknown 
square.

The Sudokus tested against your function will be "easy" (i.e. determinable; 
there will be no need to assume and test possibilities on unknowns) and can be solved 
with a brute-force approach.

For Sudoku rules, see the Wikipedia article.

puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

sudoku(puzzle)
# Should return
 [[5,3,4,6,7,8,9,1,2],
  [6,7,2,1,9,5,3,4,8],
  [1,9,8,3,4,2,5,6,7],
  [8,5,9,7,6,1,4,2,3],
  [4,2,6,8,5,3,7,9,1],
  [7,1,3,9,2,4,8,5,6],
  [9,6,1,5,3,7,2,8,4],
  [2,8,7,4,1,9,6,3,5],
  [3,4,5,2,8,6,1,7,9]]"""

"""Remark by Giulio: the following is a brute-force solver."""








import copy

def fill_with(puzzlee, i, j, n):
    puzzle = deep_copy(puzzlee)
    """ Fill puzzle[i][j] with n and returns the result"""
    puzzle[i][j] = n
    return puzzle


def deep_copy(puzzle):
    return copy.deepcopy(puzzle)


def find_missing(puzzle, i, j):
    """ Returns list of numbers that are not it row i or in column j of puzzle"""
    numbers_from_row = {puzzle[i][k] for k in range(9) if puzzle[i][k] != 0}
    numbers_from_column = {puzzle[h][j] for h in range(9) if puzzle[h][j] != 0}
    i_3, j_3 = i-(i % 3), j-(j % 3)
    numbers_from_square = set()
    for h in range(i_3, i_3+3):
        for k in range(j_3, j_3+3):
            if puzzle[h][k] != 0:
                numbers_from_square.add(puzzle[h][k])
    numbers_set = numbers_from_row.union(
        numbers_from_column, numbers_from_square)
    return {h for h in range(1, 10)}.difference(numbers_set)


def sudoku(puzzlee):
    """return the solved puzzlee as a 2d array of 9 x 9"""
    puzzle = deep_copy(puzzlee)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                missing = find_missing(puzzle, i, j)
                while len(missing) > 0:
                    n = missing.pop()
                    new_puzzle = sudoku(fill_with(puzzle, i, j, n))
                    if new_puzzle != None:
                        return new_puzzle
                return None
    return puzzle