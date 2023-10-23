# 2 kyu
"""DESCRIPTION:
There are several difficulty of sudoku games, we can estimate the difficulty of a sudoku game based on how many cells are given of the 81 cells of the game.

Easy sudoku generally have over 32 givens
Medium sudoku have around 30-32 givens
Hard sudoku have around 28-30 givens
Very Hard sudoku have less than 28 givens
Note: The minimum of givens required to create a unique (with no multiple solutions) sudoku game is 17.

A hard sudoku game means that at start no cell will have a single candidates and thus require guessing and trial and error. A very hard will have several layers of multiple candidates for any empty cell.

Task:
Write a function called "sudoku_solver" that solves sudoku puzzles of any difficulty. The function will take a sudoku grid and it should return a 9x9 array with the proper answer for the puzzle.

Or it should raise an error in cases of: invalid grid (not 9x9, cell with values not in the range 1~9); multiple solutions for the same puzzle or the puzzle is unsolvable

"""
def print_line():
    """ Prints a line of 60 dashes. """
    print('-'*60)

def print_dicts(dictios_list):
    for dictionary in dictios_list:
        print(dictionary)
        print('\n')
                          

import copy


def fill_with(puzzle, i, j, n):
    """ Fills puzzle[i][j] with n."""
    puzzle[i][j] = n


def find_missing(puzzle, i, j):
    """ 
    Returns list of numbers that are not in row i, in column j or in the corresponding 
    square of puzzle, together with its length (i.e., of the list).
    """
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
    output = {h for h in range(1, 10)}.difference(numbers_set)
    return [output, len(output)]

def move_case(h, k, case, dictios_list):
    """ Moves the key-value pair of the key "case" from entry h to entry k 
    of dictios_list"""
    dictios_list[k][case] =  dictios_list[h][case]
    del dictios_list[h][case] 



def update_missing_dicts(k, dictios_list, i, j, n):
    """Updates the missing dictionary after filling position i,j with value n.
    Then it returns a list of the coordinates (different from (i, j)) where the 
    changes appened, and a boolean which is False if in the meantime any coordinate
    became unfillable. In this case the process stops."""
    modified_keys = [[] for k in range(8)]
    move_case_list = []
    del dictios_list[k][(i, j)]
    i_3, j_3 = i-(i % 3), j-(j % 3)
    temp_set = set()
    for h in range(8):
        if dictios_list[h]:
            for key in dictios_list[h].keys():
                key_is_in_square = i_3 <= key[0] < (i_3 + 3) and  j_3 <= key[1] < (j_3 + 3)
                if key_is_in_square or key[0] == i or key[1] == j:
                    if n in dictios_list[h][key]:
                        # I append n to the output only if it was actually discarded
                        if h == 0:
                            # Case of coordinates 'key' has become unfillable.
                            return [modified_keys, False, move_case_list]
                        # else...
                        modified_keys[h].append(key)
                        dictios_list[h][key].remove(n)
                        move_case_list.append((h, h-1, key, dictios_list))
    return [modified_keys, True, move_case_list]



def sudoku(puzzle, missing_dicts=None, reverse=False):
    """returns the solved puzzle as a 2d array of 9 x 9"""
    if missing_dicts == None:
        # This is the list of the dictionaries of the unfilled cases.
        # missing_dicts[k] is either an empty list or a single element list. In the latter case
        # the element is a dictionary which contains the cases where exactly k+1 numbers
        # are still allowed to be tried.
        missing_dicts = []
        for k in range(9):
            dictio = {(i, j): find_missing(puzzle, i, j)[0]
                        for i in range(9) for j in range(9)
                        if (not puzzle[i][j] and find_missing(puzzle, i, j)[1]==k+1)}
            missing_dicts.append(dictio)
    missing_is_empty = True
    for dictio in missing_dicts:
        if len(dictio):
            missing_is_empty = False
    if missing_is_empty:
        return puzzle
    for k in range(9):
        if missing_dicts[k]:
            for key in missing_dicts[k].keys():
                i, j = key
                missing_ij = [el for el in missing_dicts[k][(i, j)]]
                missing_ij.sort() #orders from 1 to 9
                len_ij = len(missing_ij)
                if reverse:
                    missing_ij.reverse()
                for n in missing_ij:
                    fill_with(puzzle, i, j, n)
                    # I update the missing dict and keep track of the changes
                    cuts_miss_dict_keys, go_on, moves_list = update_missing_dicts(k, missing_dicts, i, j, n)
                    if not go_on: # this means that in the meantime some coordinate became unfillable
                        fill_with(puzzle, i, j, 0)
                        missing_dicts[k][(i, j)] = {el for el in missing_ij}
                        for h in range(len(cuts_miss_dict_keys)):
                            for key in cuts_miss_dict_keys[h]:
                                missing_dicts[h][key].add(n)   
                    else:
                        for tupla in moves_list:
                            move_case(*tupla)
                        new_puzzle = sudoku(puzzle, missing_dicts)
                        if new_puzzle != None:
                            return new_puzzle
                        # if n doesn't work, I "erase" it, restore the missing_dicts, 
                        # and try another number
                        fill_with(puzzle, i, j, 0)
                        missing_dicts[k][(i, j)] = {el for el in missing_ij}
                        for tupla in moves_list:
                            move_case(tupla[1], tupla[0], tupla[2], tupla[3])
                            missing_dicts[tupla[0]][tupla[2]].add(n)
                return None
    return None


def check_puzzle_format(puzzle):
    """Returns False if puzzle is not a list of 9 lists, each one containing only
    integer numbers from 0 to 9."""
    number_of_rows = len(puzzle)
    if number_of_rows != 9:
        return False
    rows_len = [len(row) for row in puzzle]
    for leng in rows_len:
        if leng != 9:
            return False
    numbers = {el for row in puzzle for el in row}
    while len(numbers) > 0:
        n = numbers.pop()
        if n not in [i for i in range(0, 10)]:
            return False
    return True

def check_puzzle_repetitions(puzzle):
    """Returns False if the solution provided (without empty cases) is wrong."""
    ordered_nine = [i for i in range(1,10)]
    rows_are_fine = all([sorted(row)==ordered_nine for row in puzzle])
    columns_are_fine = all([sorted([row[j] for j in range(9)])==ordered_nine for row in puzzle])
    squares_bool = []
    square = []
    for h in range(3):
        for k in range(3):
            for i in range(3*h, 3*h+3):
                for j in range(3*k, 3*k+3):
                    square.append(puzzle[i][j])
            squares_bool.append(sorted(square)==ordered_nine)
            square = []
    squares_are_fine = all(squares_bool)
    if rows_are_fine and columns_are_fine and squares_are_fine:
        return True
    else:
        return False

def sudoku_solver(puzzle):
    if not check_puzzle_format(puzzle):
        raise Exception('Error: invalid grid format!')
    if len([row[i] for row in puzzle for i in range(9) if not row[i]]) > 64:
        raise Exception('Error: there are multiple solutions. Invalid grid!')
    puzzle2 = copy.deepcopy(puzzle)
    solution = sudoku(puzzle)
    if solution == None:
        raise Exception('Error: unsolvable grid!')
    elif not check_puzzle_repetitions(solution):
        raise Exception('Error: there are repetitions. Unsolvable grid!')
    else:
        solution2 = sudoku(puzzle2, None, True)
        if solution2 != solution:
            raise Exception('Error: there are multiple solutions. Invalid grid!')
    return solution
