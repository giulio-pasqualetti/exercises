# 3 kyu
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
# PROBLEM: on big tables this code exceeds maximum recursion depth

class Path:
    def __init__(self, path, toll_map):
        self.path = path
        self.end = path[-1]
        self.toll_map = toll_map
        self.cost = sum([toll_map[i][j] for (i, j) in path[:-1]])
        self.surroundings = {
            (i,j) for i in range(len(toll_map)) for j in range(len(toll_map[0])) 
            if (i,j) not in path and ((i-1,j) in path[:-1] or (i+1,j) in path[:-1] or (i,j-1) in path[:-1] or (i,j+1) in path[:-1])
            }

    def get_new_cases(self):
        i, j = self.end
        possible_new_cases = [(i+h, j) for h in [-1, 1] if 0 <= i+h < len(self.toll_map)] + [
            (i, j+h) for h in [-1, 1] if 0 <= j+h < len(self.toll_map[0])]
        possible_new_cases = [case for case in possible_new_cases if case not in self.surroundings]
        return [case for case in possible_new_cases if case not in self.path]

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
        

def find_minimal_path(toll_map, start, finish, current_path=None, candidate_minimal_path=None):
    if current_path == None:
        current_path = Path([start], toll_map)
    if current_path.end == finish:
        if candidate_minimal_path==None or current_path.cost < candidate_minimal_path.cost:
            #deep copy
            candidate_minimal_path = Path(current_path.path[:], toll_map)
    else:
        for case in current_path.get_new_cases():
            current_path.add_case(case)
            if candidate_minimal_path == None or current_path.cost < candidate_minimal_path.cost:
                candidate_minimal_path = find_minimal_path(toll_map, start, finish, current_path, candidate_minimal_path)
            current_path.cut_last_case()
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
    print(f'Cost = {minimazing_path.cost}')
    return translate(minimazing_path.path)