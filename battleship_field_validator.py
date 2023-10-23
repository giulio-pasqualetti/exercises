# 3kyu
"""
Write a function, called "validate_battlefield", that takes a field for 
well-known board game "Battleship" as an argument and returns true if it 
has a valid disposition of ships, false otherwise. Argument is guaranteed 
to be 10*10 two-dimension array. Elements in the array are numbers, 0 if 
the cell is free and 1 if occupied by ship.

Battleship (also Battleships or Sea Battle) is a guessing game for two 
players. Each player has a 10x10 grid containing several "ships" and 
objective is to destroy enemy's forces by targetting individual cells on 
his field. The ship occupies one or more cells in the grid. Size and number
of ships may differ from version to version. In this kata we will use 
Soviet/Russian version of the game.

Before the game begins, players set up the board and place the ships 
accordingly to the following rules:

There must be a single battleship (size of 4 cells), 2 cruisers (size 3), 
3 destroyers (size 2) and 4 submarines (size 1). 

Any additional ships are not allowed, as well as missing ships.

Each ship must be a straight line, except for submarines, which are just 
single cell.

The ship cannot overlap or be in contact with any other ship, neither by
edge nor by corner.


This is all you need to solve this kata. If you're interested in more information about the game, visit this link:
https://en.wikipedia.org/wiki/Battleship_(game)
"""


class Ship:
    def __init__(self, size):
        self.size = size
        self.position = set()
        self.is_present = False

    def surroundings(self):
        neighbouring_cases = set()
        for case in self.position:
            i, j = case
            surrounding_cases = {(h, k) for h in range(i-1, i+2) for k in range(
                j-1, j+2) if 0 <= h < 10 and 0 <= k < 10 and (h, k) not in self.position}
            neighbouring_cases.update(surrounding_cases)
        return neighbouring_cases


def coordinates(field):
    return {(i, j) for i in range(10) for j in range(10) if field[i][j]}


def find_ship(coordinates, size):
    for case in coordinates:
        i, j = case
        horizontal_ship = {(i, j+h) for h in range(size)}
        vertical_ship = {(i+h, j) for h in range(size)}
        if all(case in coordinates for case in horizontal_ship):
            return True, horizontal_ship
        elif all(case in coordinates for case in vertical_ship):
            return True, vertical_ship
    return False, []


def substract(main, excluded):
    return {case for case in main if case not in excluded}


def validate_battlefield(field):
    field_coordinates = coordinates(field)

    # First check: there must be exactly 20 1's (and 80 zeroes)
    if len(field_coordinates) != 20:
        return False

    # Second check: ships sizes and shapes must fulfill the conditions
    fleet_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    fleet = []
    for size in fleet_sizes:
        ship = Ship(size)
        ship.is_present, ship.position = find_ship(field_coordinates, ship.size)
        if not ship.is_present:
            return False
        fleet.append(ship)
        field_coordinates = substract(field_coordinates, ship.position)

     # Third check: ships must not be adjacent
    for k, ship in enumerate(fleet):
        surroundings = ship.surroundings()
        for other_ship in fleet[k+1:]:
            if surroundings & other_ship.position:
                return False
    return True


# Example of input
field = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
         [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
         [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

validate_battlefield(field)
