from gamestate import GameState
from copy import deepcopy
import random

class BoardState(GameState):
    WINNING_LINES = [((-4, 0), (4, 0), (1, 0), 5),
                     ((0, -4), (0, 4), (0, 1), 5),
                     ((-4, -4), (4, 4), (1, 1), 5),
                     ((-4, 4), (4, -4), (1, -1), 5)]
    """
    Takes:
        grid: a 2d grid representing the board
        turn: the player who made the most recent move
        recent_move: tuple (y, x) representing the most recent move
        coordinates: a list of tuples (y, x) representing the possible moves of the parent state. This is so that 
                        generate_next_states does not have to recalculate all the possible moves
        search_breadth: the diagonal distance around filled tiles to search during generate_next_states
    """
    def __init__(self, grid, recent_move, turn=1, coordinates=None, filled=None, search_breadth=2):
        super().__init__(turn)
        assert BoardState.legal(grid), "grid not legal"
        self.grid = grid
        self.recent_move = recent_move
        self.search_breadth = search_breadth
        self.filled = filled if filled is not None else self.generate_filled()
        self.coordinates = coordinates if coordinates is not None else self.generate_coordinates()

    """
    Returns the player who made the most recent move
    """
    def get_turn(self):
        return self.turn

    """
    Returns the length of the square grid
    """
    def size(self):
        return len(self.grid[0])

    """
    Returns a list of tuples (y, x) representing all the empty tiles 
    """
    def empty(self):
        empty = []
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == 0:
                    empty.append((y, x))
        return empty

    """
    Returns a list of tuples (y, x) representing all the filled tiles 
    This function should only be called for the parent state when filled = None
    """
    def generate_filled(self):
        filled = []
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile != 0:
                    filled.append((y, x))
        return filled

    """
    Returns a list of tuples (y, x) representing all the empty tiles that are search_breadth away from the filled tiles
    This function should only be called for the parent state when coordinates = None
    """
    def generate_coordinates(self):
        coordinates = []
        for empty_tile in self.empty():
            for filled_tile in self.filled:
                if BoardState.diagonal_distance(empty_tile[0], empty_tile[1], filled_tile[0],
                                           filled_tile[1]) <= self.search_breadth:
                    coordinates.append(empty_tile)
                    break
        return coordinates

    """
    Adds a few more coordinates to self.coordinates based on recent_move.
    """
    def update_coordinates(self):
        y, x = tuple(c - self.search_breadth for c in self.recent_move)
        for i in range(self.search_breadth * 2 + 1):
            for j in range(self.search_breadth * 2 + 1):
                if not self.within_bounds(y + i, x + j):
                    continue
                if self.grid[y + i][x + j] != 0:
                    continue
                for fy, fx in self.filled:
                    if BoardState.diagonal_distance(y + i, x + j, fy, fx) <= self.search_breadth \
                            and (y + i, x + j) not in self.coordinates:
                        self.coordinates.append((y + i, x + j))
                        break

    """
      Returns a random next state.
    """
    def random_next_state(self):
        self.update_coordinates()
        if len(self.coordinates) == 0:
            return None
        y, x = random.choice(self.coordinates)
        return self.play(y, x)

    """
    Creates a state from given move
    """
    def play(self, y, x):
        grid_copy = deepcopy(self.grid)
        grid_copy[y][x] = self.turn * -1
        coord_copy = deepcopy(self.coordinates)
        coord_copy.remove((y, x))
        filled_copy = deepcopy(self.filled)
        filled_copy.append((y, x))
        return BoardState(grid_copy, turn=self.turn*-1, recent_move=(y, x),
                          coordinates=coord_copy, filled=filled_copy,
                          search_breadth=self.search_breadth)

    """
    Returns an iterable of next GameStates
    """
    def generate_next_states(self):
        self.update_coordinates()
        next_states = []
        for y, x in self.coordinates:
            next_state = self.play(y, x)
            next_states.append(next_state)
        return next_states

    """
    Returns the winner if there is a winner
    Returns 0 if there is no winner
    Gets winner based on recent move
    """
    def get_winner(self):
        for line in BoardState.WINNING_LINES:
            y_i, x_i = tuple(a+b for a,b in zip(self.recent_move, line[0]))
            y_f, x_f = tuple(a+b for a,b in zip(self.recent_move, line[1]))
            dy, dx = line[2]
            line_length = line[3]
            while not self.within_bounds(y_i, x_i):
                y_i += dy
                x_i += dx
            while not self.within_bounds(y_f, x_f):
                y_f -= dy
                x_f -= dx
            line_sum = 0
            while BoardState.diagonal_distance(y_f, x_f, y_i, x_i) + 1 >= line_length:
                for i in range(line_length):
                    line_sum += self.grid[y_i][x_i]
                    y_i += dy
                    x_i += dx
                # check for winner
                if line_sum == 5:
                    return 1
                if line_sum == -5:
                    return -1
                # step back
                line_sum = 0
                y_i -= (line_length - 1) * dy
                x_i -= (line_length - 1) * dx
        return 0

    """
     returns whether a coordinate (y, x) is within the grid
    """
    def within_bounds(self, y, x):
        N = self.size()
        return N > x >= 0 and N > y >= 0

    """
    An immutable object that represents the GameState
    Should be able to differentiate between GameStates
    """
    def get_all_features(self):
        return tuple([[tuple(row) for row in self.grid]])

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.get_all_features() == other.get_all_features())

    """
    returns a str representation of the board state
    """
    def __str__(self):
        s = "\n".join([" ".join(["{:>2}".format(tile) for tile in row]) for row in self.grid]) + "\n"
        return s

    """
    checks if a grid is legal: the number of black and white pieces are equal or there is one more black piece
    """
    @staticmethod
    def legal(grid):
        s = sum(sum(row) for row in grid)
        return s == 0 or s == 1

    """
    Diagonal distance
    """
    @staticmethod
    def diagonal_distance(y1, x1, y2, x2):
        return max(abs(y1 - y2), abs(x1 - x2))


