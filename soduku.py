
#sodoku file module
from sre_parse import WHITESPACE
import tkinter as tk
import numpy as np
import time

import use_model


DEFAULT_COLOR = "WHITE"
HIGHLIGHT_COLOR = 'yellow'
TOP_LEFT_X, TOP_LEFT_Y, GRID_SIZE = 305, 30, 60

boxes = [[0 for i in range(9)] for i in range(9)]               #ids for each box (ie, highlighted yellow)
box_option_ids = [0 for i in range(10)]                          #ids for the left options
numbers_ids = [[0 for i in range(9)] for i in range(9)]         #ids for the text shown
board = [[0 for i in range(9)] for i in range(9)]               #game data in 9x9 grid
current_box_focus = (-1, -1)                                    #which box is being highlighted


def draw_board():
    print("--"*10 + "board" + "--"*10)
    print(np.array(board))
    print(board)

def make_grids(canvas):
    ''' make the 9x9 grid thats blank
        inputs: canvas
        '''
    #boxes = numpy.array(boxes)
    print(boxes)
        #part 1 make boxes

    for i in range(9):
        for j in range(9):
            top_x, top_y = TOP_LEFT_X + GRID_SIZE*i, TOP_LEFT_Y + GRID_SIZE*j
            bot_x, bot_y = TOP_LEFT_X + GRID_SIZE*(i+1), TOP_LEFT_Y + GRID_SIZE*(j+1)
            temp_box = canvas.create_rectangle(top_x, top_y, bot_x, bot_y, fill=DEFAULT_COLOR, width=1)
            boxes[i][j] = temp_box

    xs = [305, 485, 665, 845]
    ys = [30, 210, 390, 570]
    for x in xs:
        canvas.create_line(x, 30, x, 30 + 540, width=3, fill='blue')
    for y in ys:
        canvas.create_line(305, y, 305 + 540, y, width=3, fill='blue')

    print(boxes)

    return boxes

def draw_number(canvas, x, y, number):
    '''
    Give the x,y index of the numbers 2D array to draw the number.
    '''
    top_x, top_y = TOP_LEFT_X + GRID_SIZE*x + GRID_SIZE/2, TOP_LEFT_Y + GRID_SIZE*y + GRID_SIZE/2
    number_id = canvas.create_text(top_x, top_y, text =str(number), fill='black')
    numbers_ids[x][y] = number_id
    board[x][y] = number

def draw_numbers(canvas):
    #global board
    '''
    Read in 9x9 grid of 0 for clear and 1-9 as numbers
    '''
    draw_board()
    for x in range(9):
        for y in range(9):
            if board[x][y] == 0:
                pass
            else:
                top_x, top_y = TOP_LEFT_X + GRID_SIZE*x + GRID_SIZE/2, TOP_LEFT_Y + GRID_SIZE*y + GRID_SIZE/2
                number_id = canvas.create_text(top_x, top_y, text =str(board[x][y]), fill='black')
                numbers_ids[x][y] = number_id

def show_number_options(canvas):
    global box_option_ids
    '''
    Displays numbers for user to select and insert onto game board
    '''

    #drawing grid around numbers

    #canvas.create_rectangle(122, 30, 182, 570, fill=DEFAULT_COLOR, width=1)

    ys = [30, 90, 150, 210, 270, 330, 390, 450, 510]

    box_option_ids = ["not_used"]

    for y in ys:
        rect = canvas.create_rectangle(122, y, 122 + 60, y+60, fill='white', width=3, outline='blue')
        box_option_ids.append(rect)

    #drawing numbers

    numbers = [i for i in range(1, 10)] #[0, 1, 2, 3, 4, 5, 7, 8]
    numbers = np.array(numbers)

    top_x, top_y = 152, 60
    bot_x, bot_y = 152, 540

    number_options = []

    for x in range(9):
        numbers[x] = x
    for y in range(9):
        canvas.create_text(top_x, top_y, text =str(y + 1), fill='black')
        top_y += 60

def grey_out_options(canvas, possbilities):
    print(f"Possilibntilnq;wljodh: {possbilities}")
    for index in box_option_ids:
        canvas.itemconfig(index, fill="grey")
    for poss in possbilities:
        canvas.itemconfig(box_option_ids[poss], fill="white")

def instructions(canvas):
    pass

def highlight_box(canvas, boxes, x, y):
    '''

    '''
    for tx in range(9):
        for ty in range(9):
            canvas.itemconfig(boxes[tx][ty], fill=DEFAULT_COLOR)
    canvas.itemconfig(boxes[x][y], fill=HIGHLIGHT_COLOR)

def get_possbilities_rows(x, y):
    not_possible = set()
    for i in range(9):
        if board[i][y] != 0:
            not_possible.add(board[i][y])
    print(not_possible)
    return not_possible

def get_possbilities_columns(x, y):
    not_possible = set()
    for i in range(9):
        if board[x][i] != 0:
            not_possible.add(board[x][i])
    print(not_possible)
    return not_possible

def get_possbilities_square(x, y):
    print("Good luck Joey!")

def change_focus(canvas, x, y):
    global current_box_focus
    current_box_focus = (x, y)
    all_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    not_poss = get_possbilities_rows(x, y)      #returns [1, 2, 3, 4, 7]
    not_poss = not_poss.union(get_possbilities_columns(x, y))   #returns [6, 7, 8, 9]
    #not_poss = not_poss.union(get_possbilities_square(x, y))
    #print(f"{all_possibilities} - ( {get_possbilities_rows(x, y) } + {get_possbilities_columns(x, y)} )")
    grey_out_options(canvas, all_possibilities - not_poss )

def mouse_parser_right(event, canvas):
    global current_box_focus
    ''' Delete the number which was right clicked'''
    print(f"X:{event.x}, Y:{event.y}")
    #determine if the mouse was clicked in the 9x9 grid
    for x in range(9):
        for y in range(9):
            left_x, top_y = TOP_LEFT_X + GRID_SIZE*x, TOP_LEFT_Y + GRID_SIZE*y
            right_x, bot_y = TOP_LEFT_X + GRID_SIZE*(x+1), TOP_LEFT_Y + GRID_SIZE*(y+1)
            if event.x < right_x and event.x > left_x and event.y < bot_y and event.y > top_y:
                highlight_box(canvas, boxes, x, y)
                change_focus(canvas, x, y)
                print(f"Current focus is ({x},{y}) which is #: {board[x][y]}")
                canvas.delete(numbers_ids[x][y])
                board[x][y] = 0
                print(f"Current focus is ({x},{y}) which is #: {board[x][y]}")

def mouse_parser(event, canvas, boxes):
    global current_box_focus
    '''
    Figure where mouse was clicked, and use that info

    '''
    #figure the mouse presses
    print(f"X:{event.x}, Y:{event.y}")

    #determine if the mouse was clicked in the 9x9 grid
    for x in range(9):
        for y in range(9):
            left_x, top_y = TOP_LEFT_X + GRID_SIZE*x, TOP_LEFT_Y + GRID_SIZE*y
            right_x, bot_y = TOP_LEFT_X + GRID_SIZE*(x+1), TOP_LEFT_Y + GRID_SIZE*(y+1)
            if event.x < right_x and event.x > left_x and event.y < bot_y and event.y > top_y:
                highlight_box(canvas, boxes, x, y)
                change_focus(canvas, x, y)
                print(f"Current fofcus is ({x},{y}) which is #: {board[x][y]}")

    #determine if mouse click was in the side board options:
    for i in range(9):
        left_x, top_y = 122, 30+60*i
        right_x, bot_y = 182, 30+60*(i+1)
        if event.x < right_x and event.x > left_x and event.y < bot_y and event.y > top_y:
            if current_box_focus[0] == -1:
                print("No Hightlighted Box")
                pass
            else:
                x, y = current_box_focus
                draw_number(canvas, x, y, i+1)
                board[x][y] = i+1
                print(board[x][y])
                draw_board()

def call_sudoku(canvas):
    global board
    print("Hello World from planet Soduku")
    canvas.delete('all')
    boxes = make_grids(canvas)
    board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9]]
    draw_board()
    board = use_model.get_seed()
    draw_board()
    show_number_options(canvas)
    draw_numbers(canvas)
    instructions(canvas)

    canvas.bind('<Button-1>', lambda event:mouse_parser(event, canvas, boxes))
    canvas.bind('<Button-3>', lambda event:mouse_parser_right(event, canvas))
