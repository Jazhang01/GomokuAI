from tkinter import *

BOARD_SIZE = 19
STONE_SCALE_FACTOR = 0.7
WIDTH = 900
HEIGHT = 900

# TODO: Make 'Button' class that allows user to place their stone (black or white)
# https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python

class Application(Frame):
    def __init__(self, master, width, height):
        super(Application, self).__init__(master)
        self.grid()
        self.canvas = Canvas(master, width=width, height=height)
        self.create_widgets()
    def place_point(self, x,y):
        self.canvas.create_oval(x,y,x,y, width=10, fill='black')
    def onObjectClick(event):
        print ('Clicked')
    def create_widgets(self):
        self.canvas.pack()
        self.GRID_WIDTH = 800
        self.GRID_HEIGHT = 800
        self.grid_interval = int(self.GRID_WIDTH/(BOARD_SIZE+1))
        #Vertical
        for i in range(0, self.GRID_WIDTH, self.grid_interval):
            self.canvas.create_line([(i, self.grid_interval), (i, self.GRID_HEIGHT-self.grid_interval)], tag='grid_line')
        #Horizontal
        for i in range(0, self.GRID_HEIGHT, self.grid_interval):
            self.canvas.create_line([(self.grid_interval, i), (self.GRID_WIDTH-self.grid_interval, i)], tag='grid_line')
        for i in range(1,BOARD_SIZE+1):
            for j in range (1, BOARD_SIZE+1):
                # TODO: Add button at this intersection
                # Coordinates of intersection: i*self.grid_interval, j*self.grid_interval

def main():
    root = Tk()
    root.title("Gomoku AI")
    app = Application(root, WIDTH, HEIGHT)
    root.mainloop()

main()