# 3 kyu. This code seems to still be too slow for large inputs
"""
You should be familiar with the "Find the shortest path" problem. 
But what if moving to a neighboring coordinate counted not as 1 step but 
as N *steps? *

INSTRUCTIONS

Your task is to write a function, called "cheapest_path", that
finds the path through the field which has the lowest cost 
to go through.

As input you will receive:

- a toll_map matrix (as variable t) which holds data about how expensive 
it is to go through the given field coordinates
- a start coordinate (tuple) which holds information about your starting 
position
- a finish coordinate (tuple) which holds information about the position 
you have to get to

As output you should return:

the directions list
EXAMPLE

INPUT:

toll_map  |  start  |  finish
          |         |
[         |         |
 [1,9,1], |  (0,0)  |  (0,2)
 [2,9,1], |         |
 [2,1,1], |         |
]         |         |



OUTPUT:

["down", "down", "right", "right", "up", "up"]

CLARIFICATIONS

- the start and finish tuples represent (row, col) indices
- the total cost is increased after leaving the matrix coordinate, 
not entering it
- the field will be rectangular, not necessarily a square
- the field will always be of correct shape
- the actual tests will check total_cost based on your returned 
directions list, not the directions themselves, so you shouldn't 
worry about having multiple possible solutions
"""


class Path:
    def __init__(self, path, toll_map):
        self.path = path
        self.end = path[-1]
        self.toll_map = toll_map
        self.cost = sum([toll_map[i][j] for (i, j) in path[:-1]])
        self.surroundings = {
            (i, j) for i in range(len(toll_map)) for j in range(len(toll_map[0]))
            if (i, j) not in path and ((i-1, j) in path[:-1] or (i+1, j) in path[:-1] or (i, j-1) in path[:-1] or (i, j+1) in path[:-1])
        }

    def get_new_cases(self):
        i, j = self.end
        possible_new_cases = [(i+h, j) for h in [-1, 1] if 0 <= i+h < len(self.toll_map)] + [
            (i, j+h) for h in [-1, 1] if 0 <= j+h < len(self.toll_map[0])]
        possible_new_cases = [
            case for case in possible_new_cases if case not in self.surroundings]
        new_cases = [case for case in possible_new_cases if case not in self.path]
        return new_cases
    def add_case(self, new_case):
        i, j = self.end
        self.cost += self.toll_map[i][j]
        self.path.append(new_case)
        self.end = new_case

    def cut_last_case(self):
        self.path.pop()
        self.end = self.path[-1]
        i, j = self.end
        self.cost = self.cost - self.toll_map[i][j]
    
    def trim(self, cases_to_check):
        # I keep cutting the end of the path until I reach the case
        # that has actually generated the last element of cases_to_check
        # (which is the next in line to be checked)
        while cases_to_check and self.end != cases_to_check[-1][0]:
            # print(f'Cutting {self.end}')
            self.cut_last_case()


def find_minimal_path(toll_map, start, finish):
    def sum_cases(case1, case2):
        return (case1[0] + case2[0], case1[1] + case2[1])

    def directions_from(beginning):
        nonlocal finish
        output = set()
        if beginning[0] < finish[0]:
            output.add((1,0)) #down
        elif beginning[0] > finish[0]:
            output.add((-1,0)) #up
        if beginning[1] < finish[1]:
            output.add((0,1)) #right
        elif beginning[1] > finish[1]:
            output.add((0,-1)) #left
        return output  

    def sort_new_cases(generator, cases, directions):
        output = []
        for el in directions:
            case = sum_cases(generator, el)
            if case in cases:
                output.append(case)
        rest = [case for case in cases if case not in output]
        return rest + output


    path = Path([start], toll_map)
    maximal_cost = sum([sum(toll_map[i]) for i in range(len(toll_map))])
    candidate_minimal_path = Path([start], toll_map)
    candidate_minimal_path.cost = maximal_cost
    # Initialize the list of the cases to be checked.
    # Each element is a couple, where the case to be checked is
    # the second argument, while the first one is his "generator".
    new_cases = path.get_new_cases()
    directions = directions_from(start)
    new_cases = sort_new_cases(start, new_cases, directions)
    cases_to_be_checked = [(start, case) for case in new_cases]
    while cases_to_be_checked:
        case = cases_to_be_checked.pop()[1]
        path.add_case(case)
        if path.cost >= candidate_minimal_path.cost:
            path.trim(cases_to_be_checked)
        elif path.end == finish:
            candidate_minimal_path = Path(path.path[:], toll_map)
            path.trim(cases_to_be_checked)
        else:
            new_cases = path.get_new_cases()
            if not new_cases:  # i.e. I am in a dead end
                path.trim(cases_to_be_checked)
            else:
                directions = directions_from(case)
                new_cases = sort_new_cases(case, new_cases, directions)
                cases_to_be_checked.extend(
                    [(case, new_case) for new_case in new_cases])
    return candidate_minimal_path


def get_direction(start, end):
    i, j = start
    h, k = end
    if h == i+1:
        return "down"
    elif h == i-1:
        return "up"
    elif k == j+1:
        return "right"
    else:
        return "left"


def translate(path):
    directions = []
    for k in range(1, len(path)):
        directions.append(get_direction(path[k-1], path[k]))
    return directions


def cheapest_path(toll_map, start, finish):
    if start == finish:
        return []
    minimazing_path = find_minimal_path(toll_map, start, finish)
    return translate(minimazing_path.path)
