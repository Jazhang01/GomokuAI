from tkinter import *
import gomoku_state

BOARD_SIZE = 19
STONE_SIZE_FACTOR = 0.8
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_WIDTH = 800
GRID_HEIGHT = 800

BLACK = 1
WHITE = -1

# TODO: General formatting of buttons/text boxes
# TODO: ** Integrate gamestate.py into Application

class Application(Frame):
    """
    Takes: width, height

    Initialize variables for Application:
    - board: a 2D array initialized to all 0s
    - player_turn
    - placed_pieces: an array (used as a stack) that keeps track of pieces placed in order
        - each piece is a Canvas object (oval)
    - grid_interval: adjusts spacing of lines on the board (determined by GRID_WIDTH and BOARD_SIZE)
    """
    def __init__(self, master, width, height):
        super(Application, self).__init__(master)
        self.grid()
        self.master = master
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.moves = 0
        self.player_turn = BLACK
        self.placed_pieces = []
        self.canvas = Canvas(master, width=width, height=height)
        self.grid_interval = int(GRID_WIDTH / (BOARD_SIZE + 1))
        self.mults = None
        self.welcome()

    """
    Sets up welcome screen:
    - Title
    - Play button
    """
    def welcome(self):
        self.title = Label(self,
              text = "Gomoku")
        self.title.config(font = ("Helvetica", 35))
        self.title.grid(row = 0, column = 0, columnspan = 3)
        self.start_btn = Button(self,
                                text = "Play",
                                command = self.set_up_board)
        self.start_btn.config(font = ("Helvetica", 18))
        self.start_btn.grid(row = 1, column = 2)
        # TODO: Player v. Player, Player v. Computer

    """
    Sets up the board, including miscellaneous buttons such as undo, etc.
    """
    def set_up_board(self):
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.grid(row = 0, column = 0)
        # TODO: When player hovers, a faded/transparent piece shows on intersection
        # self.canvas.bind("<Motion>", self.hover)
        # self.current_hover = tuple()
        self.draw_board()
        self.undo_btn = Button(self.master,
                                text = "Undo",
                                command = self.undo_move)
        self.undo_btn.config(font = ("Helvetica", 18))
        self.undo_btn.grid(row = 1, column = 0)

    """
    Draws lines of board on canvas (board)
    """
    def draw_board(self):
        self.mults = [i for i in range(self.grid_interval, GRID_WIDTH, self.grid_interval)]
        # Vertical
        for i in range(0, GRID_WIDTH, self.grid_interval):
            self.canvas.create_line([(i, self.grid_interval), (i, GRID_HEIGHT - self.grid_interval)], tag='grid_line')
        # Horizontal
        for i in range(0, GRID_HEIGHT, self.grid_interval):
            self.canvas.create_line([(self.grid_interval, i), (GRID_WIDTH - self.grid_interval, i)], tag='grid_line')

    """
    Handles user's click on canvas (board)
    - If the click is near an available spot, user can place piece
    """
    def onClick(self, event):
        x,y = self.get_intersection(event.x, event.y)
        if (x != -1 and y != -1):
            board_coords = self.get_board_coordinates(x, y)
            if self.board[board_coords[0]][board_coords[1]] == 0: # player is able to place piece
                self.placed_pieces.append(Piece(board_coords[0],
                                                board_coords[1],
                                                self.player_turn,
                                                self.placePiece(x, y),
                                                self))
                self.board[board_coords[0]][board_coords[1]] = self.player_turn
                self.player_turn = (-1)*self.player_turn
                self.moves += 1
                possible_winner = gomoku_state.BoardState(self.board, tuple([board_coords[0],board_coords[1]])).get_winner()
                if possible_winner != 0:
                    self.winner(possible_winner)

    """
    Draws piece with corresponding color of player's turn and adds to the self.placed_pieces stack
    """
    def placePiece(self, x, y):
        if self.player_turn == BLACK:
            color = "black"
        else:
            color = "white"
        scale = STONE_SIZE_FACTOR / 2
        piece = self.canvas.create_oval(x - (self.grid_interval * scale),
                                    y - (self.grid_interval * scale),
                                    x + (self.grid_interval * scale),
                                    y + (self.grid_interval * scale),
                                        fill = color)
        return piece

    """
    Converts canvas coordinates to index values for the 2D array self.board
    """
    def get_board_coordinates(self, x, y):
        return int(x/self.grid_interval-1), int(y/self.grid_interval-1)

    """
    Undoes move:
    - Pops last piece from self.placed_pieces stack
    - Swaps current player turn
    - Deletes last piece from canvas (board)
    """
    def undo_move(self):
        if len(self.placed_pieces) > 0:
            last_piece = self.placed_pieces.pop()
            self.board[last_piece.x][last_piece.y] = 0
            self.player_turn = (-1)*self.player_turn
            last_piece.remove()
            self.moves -= 1

    #def hover(self, event):
        #print("hovered at", event.x, event.y)

    """
    Gets the nearest set of coordinates that is the intersection of two lines on the canvas
    """
    def get_intersection(self, x, y):
        ans = [-1, -1]
        for i in range(0, len(self.mults)-1):
            if (self.mults[i] <= x and x <= self.mults[i+1]):
                if (x-self.mults[i] <= self.mults[i+1]-x):
                    ans[0] = self.mults[i]
                else:
                    ans[0] = self.mults[i+1]
            if (self.mults[i] <= y and y <= self.mults[i+1]):
                if (y-self.mults[i] <= self.mults[i+1]-y):
                    ans[1] = self.mults[i]
                else:
                    ans[1] = self.mults[i+1]
        return tuple(ans)

    """
    Called when one of the players has won
    """
    def winner(self, winner):
        self.winner_msg = Label(self.master,
                                text="White wins!" if winner == WHITE else "Black wins!")
        self.winner_msg.config(font=("Helvetica", 30))
        self.winner_msg.grid(row=2, column=0)

class Piece:
    def __init__(self, x, y, player, obj, app):
        self.x = x
        self.y = y
        self.player = player
        self.obj = obj
        self.app = app

    def remove(self):
        self.app.canvas.delete(self.obj)

def main():
    root = Tk()
    root.title("Gomoku")
    #root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
    app = Application(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    root.mainloop()

main()