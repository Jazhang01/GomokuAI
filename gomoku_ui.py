from tkinter import *

BOARD_SIZE = 19
STONE_SCALE_FACTOR = 0.7
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
GRID_WIDTH = 800
GRID_HEIGHT = 800
BUTTON_SCALE = 5/12

BLACK = 0
WHITE = 1

class Application(Frame):
    def __init__(self, master, width, height):
        super(Application, self).__init__(master)
        self.grid()
        self.player_turn = WHITE
        self.canvas = Canvas(master, width=width, height=height)
        self.canvas.bind("<Button-1>", self.onClick)
        # TODO: When player hovers, a faded/transparent piece shows on intersection
        #self.canvas.bind("<Motion>", self.hover)
        self.current_hover = tuple()
        self.create_widgets()
    def create_widgets(self):
        self.canvas.pack()
        self.grid_interval = int(GRID_WIDTH/(BOARD_SIZE+1))
        #Vertical
        for i in range(0, GRID_WIDTH, self.grid_interval):
            self.canvas.create_line([(i, self.grid_interval), (i, GRID_HEIGHT-self.grid_interval)], tag='grid_line')
        #Horizontal
        for i in range(0, GRID_HEIGHT, self.grid_interval):
            self.canvas.create_line([(self.grid_interval, i), (GRID_WIDTH-self.grid_interval, i)], tag='grid_line')

    def onClick(self, event):
        x,y = self.getIntersection(event.x, event.y)
        if (x != -1 and y != -1):
            color = ["black", "white"][self.player_turn]
            self.placePiece(x, y, color)
            #self.player_turn = (self.player_turn + 1) % 2
            self.player_turn = not self.player_turn
            # TODO: Don't let player place piece on the same spot
            # TODO: Add "undo" function

    def placePiece(self, x, y, color):
        piece = self.canvas.create_oval(x - (self.grid_interval * BUTTON_SCALE),
                                    y - (self.grid_interval * BUTTON_SCALE),
                                    x + (self.grid_interval * BUTTON_SCALE),
                                    y + (self.grid_interval * BUTTON_SCALE),
                                        fill = color)
        return piece

    #def hover(self, event):
        #print("hovered at", event.x, event.y)

    def getIntersection(self, x, y):
        mults = [i for i in range(self.grid_interval, GRID_WIDTH, self.grid_interval)]
        ans = [-1, -1]
        for i in range(0, len(mults)-1):
            if (mults[i] <= x and x <= mults[i+1]):
                if (x-mults[i] <= mults[i+1]-x):
                    ans[0] = mults[i]
                else:
                    ans[0] = mults[i+1]
            if (mults[i] <= y and y <= mults[i+1]):
                if (y-mults[i] <= mults[i+1]-y):
                    ans[1] = mults[i]
                else:
                    ans[1] = mults[i+1]
        return tuple(ans)

def main():
    root = Tk()
    root.title("Gomoku AI")
    app = Application(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    root.mainloop()

main()