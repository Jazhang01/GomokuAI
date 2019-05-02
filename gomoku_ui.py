from tkinter import *
#from gamestate import gomoku_state

BOARD_SIZE = 19
STONE_SIZE_FACTOR = 0.8
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_WIDTH = 800
GRID_HEIGHT = 800


BLACK = 0
WHITE = 1

class Application(Frame):
    def __init__(self, master, width, height):
        super(Application, self).__init__(master)
        self.grid()
        self.player_turn = WHITE
        self.canvas = Canvas(master, width=width, height=height)
        self.mults = None
        self.welcome()
    def set_up_board(self):
        self.canvas.bind("<Button-1>", self.onClick)
        self.canvas.pack()
        # TODO: When player hovers, a faded/transparent piece shows on intersection
        #self.canvas.bind("<Motion>", self.hover)
        #self.current_hover = tuple()
        self.grid_interval = int(GRID_WIDTH/(BOARD_SIZE+1))
        self.mults = [i for i in range(self.grid_interval, GRID_WIDTH, self.grid_interval)]
        #Vertical
        for i in range(0, GRID_WIDTH, self.grid_interval):
            self.canvas.create_line([(i, self.grid_interval), (i, GRID_HEIGHT-self.grid_interval)], tag='grid_line')
        #Horizontal
        for i in range(0, GRID_HEIGHT, self.grid_interval):
            self.canvas.create_line([(self.grid_interval, i), (GRID_WIDTH-self.grid_interval, i)], tag='grid_line')
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
    def onClick(self, event):
        x,y = self.getIntersection(event.x, event.y)
        if (x != -1 and y != -1):
            color = ["black", "white"][self.player_turn]
            self.placePiece(x, y, color)
            self.player_turn = not self.player_turn
            # TODO: Don't let player place piece on the same spot
            # TODO: Add "undo" function

    def placePiece(self, x, y, color):
        scale = STONE_SIZE_FACTOR / 2
        piece = self.canvas.create_oval(x - (self.grid_interval * scale),
                                    y - (self.grid_interval * scale),
                                    x + (self.grid_interval * scale),
                                    y + (self.grid_interval * scale),
                                        fill = color)
        return piece

    #def hover(self, event):
        #print("hovered at", event.x, event.y)

    def getIntersection(self, x, y):
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

def main():
    root = Tk()
    root.title("Gomoku")
    root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
    app = Application(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    root.mainloop()

main()