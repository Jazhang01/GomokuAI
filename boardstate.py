# black stone: 1 --- white stone: -1
# black (1) goes first. players alternate turns

# properties:
#   the sum of the values on a board must be 0 or 1.
#   if the sum of the values on the board is 1, it is white's turn
#   if the sum of the values on the board is 0, it is black's turn

class BoardState(object):
    # Can take in some board if legal. Otherwise, uses blank board.
    def __init__(self, state=None):
        if state is None or not self.legal(state):
            print("Using blank board...")
            self.N = 19
            self.state = [[0 for i in range(self.N)] for j in range(self.N)]
        else:
            self.state = state
            self.N = len(state)

    # deep copy of self.state
    def get_state(self):
        out = [[0 for i in range(self.N)] for j in range(self.N)]
        for y, row in enumerate(self.state):
            for x, tile in enumerate(row):
                out[y][x] = tile
        return out

    def equals(self, other):
        assert isinstance(other, BoardState), "other is not a BoardState!"
        if self.N != other.N:
            return 0
        for y, row in enumerate(self.state):
            for x, tile in enumerate(row):
                if tile != other.get_state()[y][x]:
                    return 0
        return 1

    # returns the value of the person who just went
    def turn(self):
        if sum(sum(i) for i in self.state):
            return 1
        return -1

    # returns the value of the person who goes next
    def next_turn(self):
        return self.turn() * -1

    # returns a list of the coordinates of empty spaces (y, x)
    def empty(self):
        empty = []
        for y, row in enumerate(self.state):
            for x, tile in enumerate(row):
                if tile == 0:
                    empty.append((y, x))
        return empty

    def filled(self):
        filled = []
        for y, row in enumerate(self.state):
            for x, tile in enumerate(row):
                if tile != 0:
                    filled.append((y, x))
        return filled

    # TODO - make this algorithm more efficient
    # empty spaces near filled ones
    def filtered_empty(self, distance_bound):
        filtered_empty = []
        for empty_tile in self.empty():
            for filled_tile in self.filled():
                if BoardState.get_distance(empty_tile[0], empty_tile[1], filled_tile[0],
                                           filled_tile[1]) <= distance_bound:
                    filtered_empty.append(empty_tile)
                    break
        return filtered_empty

    # A player wins if they get >= 5 in a row
    # returns 1 or -1 if there is a winner, 0 if not
    def get_winner(self, mode=">=5"):
        for y, row in enumerate(self.state):
            for x, tile in enumerate(row):
                if self.state[y][x] == 0:
                    continue

                # check all 8 directions
                if self.within_bounds(y+4, x, self.N):
                    if self.state[y][x] + self.state[y+1][x] + self.state[y+2][x] + self.state[y+3][x] + self.state[y+4][x] == 5:
                        return 1
                    if self.state[y][x] + self.state[y+1][x] + self.state[y+2][x] + self.state[y+3][x] + self.state[y+4][x] == -5:
                        return -1
                if self.within_bounds(y-4, x, self.N):
                    if self.state[y][x] + self.state[y-1][x] + self.state[y-2][x] + self.state[y-3][x] + self.state[y-4][x] == 5:
                        return 1
                    if self.state[y][x] + self.state[y-1][x] + self.state[y-2][x] + self.state[y-3][x] + self.state[y-4][x] == -5:
                        return -1
                if self.within_bounds(y, x+4, self.N):
                    if sum(self.state[y][x:x+5]) == 5:
                        return 1
                    if sum(self.state[y][x:x+5]) == -5:
                        return -1
                if self.within_bounds(y, x-4, self.N):
                    if sum(self.state[y][x-4:x+1]) == 5:
                        return 1
                    if sum(self.state[y][x-4:x+1]) == -5:
                        return -1

                if self.within_bounds(y+4, x+4, self.N):
                    if self.state[y][x] + self.state[y+1][x+1] + self.state[y+2][x+2] + self.state[y+3][x+3] + self.state[y+4][x+4] == 5:
                        return 1
                    if self.state[y][x] + self.state[y+1][x+1] + self.state[y+2][x+2] + self.state[y+3][x+3] + self.state[y+4][x+4] == -5:
                        return -1
                if self.within_bounds(y-4, x+4, self.N):
                    if self.state[y][x] + self.state[y-1][x+1] + self.state[y-2][x+2] + self.state[y-3][x+3] + self.state[y-4][x+4] == 5:
                        return 1
                    if self.state[y][x] + self.state[y-1][x+1] + self.state[y-2][x+2] + self.state[y-3][x+3] + self.state[y-4][x+4] == -5:
                        return -1
                if self.within_bounds(y+4, x-4, self.N):
                    if self.state[y][x] + self.state[y+1][x-1] + self.state[y+2][x-2] + self.state[y+3][x-3] + self.state[y+4][x-4] == 5:
                        return 1
                    if self.state[y][x] + self.state[y+1][x-1] + self.state[y+2][x-2] + self.state[y+3][x-3] + self.state[y+4][x-4] == -5:
                        return -1
                if self.within_bounds(y-4, x-4, self.N):
                    if self.state[y][x] + self.state[y-1][x-1] + self.state[y-2][x-2] + self.state[y-3][x-3] + self.state[y-4][x-4] == 5:
                        return 1
                    if self.state[y][x] + self.state[y-1][x-1] + self.state[y-2][x-2] + self.state[y-3][x-3] + self.state[y-4][x-4] == -5:
                        return -1
        return 0

    """
    returns a str representation of the board state
    """
    def __str__(self):
        s = "\n".join([" ".join(["{:>2}".format(tile) for tile in row]) for row in self.state]) + "\n"
        return s

    """
    returns whether a coordinate (y, x) is within the NxN grid
    """
    @staticmethod
    def within_bounds(y, x, N):
        return N > x >= 0 and N > y >= 0

    """
    checks if a state is legal: the number of black and white pieces are equal or there is one more black piece
    """
    @staticmethod
    def legal(state):
        s = sum(sum(i) for i in state)
        return s == 0 or s == 1

    """
    Diagonal distance
    """
    @staticmethod
    def get_distance(y1, x1, y2, x2):
        return max(abs(y1 - y2), abs(x1 - x2))



def tester():
    bs = BoardState(state=[[ 1, 1,-1,-1,-1, 0],
                           [ 1, 0, 0, 0, 1, 0],
                           [-1, 1, 0, 1,-1,-1],
                           [-1, 1, 1, 0,-1, 1],
                           [-1, 1, 0,-1, 0, 0],
                           [ 1,-1, 0, 0, 1, 0]])
    print(bs.turn())
    print(bs.get_winner())
    print(bs.empty())
    bs2 = BoardState(state=[[ 1, 1,-1,-1,-1, 0],
                            [ 1, 0, 0, 0, 1, 0],
                            [-1, 1, 0, 1,-1,-1],
                            [-1, 1, 1, 0, 1, 1],
                            [-1, -1, 0,-1, 0, 0],
                            [ 1,-1, 0, 0, 1, 0]])
    print(bs.equals(bs2))
    #print(bs.equals([0, 1]))

#tester()
