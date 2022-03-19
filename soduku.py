
#sodoku file module
import tkinter as tk

def call_sudoku(canvas):
    print("Hello World from planet Soduku")
    canvas.delete('all')
    canvas.create_text(100, 100, text="Hello World from planet Soduku", fill='red')
