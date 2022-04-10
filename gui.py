

#source file for GUI.
#will be the main driver.

import tkinter as tk
import random

import chess
import soduku

width, height, grid_size = 1150, 720, 16

def get_hex(n):
    number = random.randint(0, 16 ** n)
    hexed = list(hex(number))
    hexed.pop(0)
    hexed.pop(0)
    while(len(hexed) < 6):
        hexed = ['0'] + hexed
    return '#' + ''.join(hexed)

def make_grid(canvas):

    for i in range(0, width, grid_size):
        for j in range(0, height, grid_size):
            canvas.create_rectangle(i, j, i+grid_size, j+grid_size, fill=get_hex(6), width=2)

def mouse_parse(event, canvas):
    if (event.x < grid_size) & (event.y < grid_size):
        print("SUDOKU")
        canvas.unbind("<Button-1>")
        soduku.call_sudoku(canvas)
    elif (event.x > (width - grid_size)) & (event.x > (width-grid_size)):
        print("CHESS")
        canvas.unbind("<Button-1>")
        chess.call_chess(canvas)
    else:
        print(event.x, event.y)

def main():
    root = tk.Tk()
    root.geometry(f"{width}x{height}")

    canvas = tk.Canvas(root, height=height, width=width, bg="black")
    canvas.pack()

    make_grid(canvas)

    canvas.bind('<Button-1>', lambda event:mouse_parse(event, canvas))

    root.mainloop()

main()
