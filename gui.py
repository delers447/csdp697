from tkinter import *
import tkinter as tk
import random

#import chess
import soduku



root = Tk()
root.title("Choose Your Poison!")

# input area for proper password to enter game
password = Entry(root, width = 50, borderwidth = 10, bg = 'white', fg = 'black')
password.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

def call_Chess():
    # overwrite current geometry in order to send proper canvas to game
    width, height, grid_size = 1150, 720, 16
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    root.title("Queens Game")

    # send 'er
    canvas = tk.Canvas(root, height=height, width=width, bg="black")
    canvas.pack()
    #chess.call_chess(canvas)
    return

def call_Sudoku():
    # overwrite current geometry in order to send proper canvas to game
    width, height, grid_size = 1150, 720, 16    
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    root.title("Sudoku")

    # send 'er
    canvas = tk.Canvas(root, height=height, width=width, bg="black")
    canvas.pack()
    soduku.call_sudoku(canvas)
    return

'''
 takes clicked number, stores it,  and displays clicked number appended to end
'''
def click_button(num):

    # saves current number clicked as to put it in proper order, instead of the order clicked
    temp = password.get()
    # wipe password
    password.delete(0, END)
    # reset password to proper order
    password.insert(0, str(temp) + str(num))
    pass

'''
 clears password entry
'''
def clear_button():
    password.delete(0, END)
    return

'''
 checks password
'''
def enter_button():
    temp_pass = password.get()
    global entered_password
    entered_password = int(temp_pass)
    if(entered_password == 783658):
        call_Sudoku()
    elif(entered_password == 78336):
        call_Chess()

    return

'''
 gives hint if we decide this
'''
def hint_button():
    pass

def main():
    
    #root.geometry(f"{width}x{height}")
    #root.resizable(False, False)
    root.title("Title")

    # printing functional buttons to screen to move to selected game
    #myButton1 = Button(root, text = 'Sudoku', command = myClickSudoku)
    #myButton2 = Button(root, text = 'Queens Game', command = myClickChess)


    #initialize buttons
    button1 = Button(root, text = '1', padx = 80, pady = 40, command = lambda: click_button(1))
    button2 = Button(root, text = '2', padx = 80, pady = 40, command = lambda: click_button(2))
    button3 = Button(root, text = '3', padx = 80, pady = 40, command = lambda: click_button(3))
    button4 = Button(root, text = '4', padx = 80, pady = 40, command = lambda: click_button(4))
    button5 = Button(root, text = '5', padx = 80, pady = 40, command = lambda: click_button(5))
    button6 = Button(root, text = '6', padx = 80, pady = 40, command = lambda: click_button(6))
    button7 = Button(root, text = '7', padx = 80, pady = 40, command = lambda: click_button(7))
    button8 = Button(root, text = '8', padx = 80, pady = 40, command = lambda: click_button(8))
    button9 = Button(root, text = '9', padx = 80, pady = 40, command = lambda: click_button(9))
    button0 = Button(root, text = '0', padx = 80, pady = 40, command = lambda: click_button(0))
 
    button_clear = Button(root, text = 'CLEAR', padx = 80, pady = 40, command = clear_button)

    button_enter = Button(root, text = 'ENTER', padx = 80, pady = 40, command = enter_button)

    button_hint = Button(root, text = 'HINT?', padx = 80, pady = 40, command = hint_button)


    #slap buttons to screen
    button_clear.grid(row =5, column =1)

    button_enter.grid(row =5, column =3)

    button1.grid(row =1, column =1)
    button2.grid(row =1, column =2)
    button3.grid(row =1, column =3)
    button4.grid(row =2, column =1)
    button5.grid(row =2, column =2)
    button6.grid(row =2, column =3)
    button7.grid(row =3, column =1)
    button8.grid(row =3, column =2)
    button9.grid(row =3, column =3)

    button0.grid(row =5, column =2)

    root.mainloop()
    
main()
