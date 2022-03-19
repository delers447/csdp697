
#chess file module
import tkinter as tk

def call_chess(canvas):
    print("Hello World from planet Chess")
    canvas.delete('all')
    canvas.create_text(100, 100, text="Hello World from planet Chess", fill='red')
