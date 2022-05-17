
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
global_possbilities = set()                                     #the numbers which are allowed.
model_box_ids = []                                              #ids of the Huds up display for the model

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

def draw_number(canvas, x, y, number, color='black'):
    '''
    Give the x,y index of the numbers 2D array to draw the number.
    '''
    top_x, top_y = TOP_LEFT_X + GRID_SIZE*x + GRID_SIZE/2, TOP_LEFT_Y + GRID_SIZE*y + GRID_SIZE/2
    number_id = canvas.create_text(top_x, top_y, text =str(number), fill=color)
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
    #draing lines around the options.
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
    global global_possbilities
    print(f"Possilibntilnq;wljodh: {possbilities}")
    global_possbilities = possbilities
    print(f"Global Possilibntilnq;wljodh: {global_possbilities}")
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
    '''Determine which square the current_focus is and then return list of Not_possibilities.'''
    square_1 = {(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)}
    square_2 = {(3,0), (4,0), (5,0), (3,1), (4,1), (5,1), (3,2), (4,2), (5,2)}
    square_3 = {(6,0), (7,0), (8,0), (6,1), (7,1), (8,1), (6,2), (7,2), (8,2)}
    square_4 = {(0,3), (1,3), (2,3), (0,4), (1,4), (2,4), (0,5), (1,5), (2,5)}
    square_5 = {(3,3), (4,3), (5,3), (3,4), (4,4), (5,4), (3,5), (4,5), (5,5)}
    square_6 = {(6,3), (7,3), (8,3), (6,4), (7,4), (8,4), (6,5), (7,5), (8,5)}
    square_7 = {(0,6), (1,6), (2,6), (0,7), (1,7), (2,7), (0,8), (1,8), (2,8)}
    square_8 = {(3,6), (4,6), (5,6), (3,7), (4,7), (5,7), (3,8), (4,8), (5,8)}
    square_9 = {(6,6), (7,6), (8,6), (6,7), (7,7), (7,8), (6,8), (8,7), (8,8)}

    squares = [square_1, square_2, square_3, square_4, square_5, square_6, square_7, square_8, square_9]
    focus = x, y
    for i, square in enumerate(squares):
        #print("=="*10 + "Did you get here?")
        if focus in square:
            print(f"The hightlighted box ({x},{y}) is in square {i+1}.")
            not_possible = set()
            for cords in square:
                x, y = cords
                if board[x][y] != 0:
                    not_possible.add(board[x][y])
            print(not_possible)
            return not_possible
#(target_x, target_y), (top_prob, top_index, top_prediction), color
def draw_model_box(canvas, target_coords, model_output, color):
    """Print heads up display based on the model predictions
        (target_x,target_y) is the top left box coords
        (top_prob, top_index, top_prediction) is the three outputs fromt the output
        color of box  #1 green, #2 orange, #3 red
    """
    target_x, target_y = target_coords
    top_prob, top_index, top_prediction = model_output
    box_id = canvas.create_rectangle(target_x, target_y, target_x + 275, target_y + 120, fill=color, width=1)
    string_text_1 = f"There is a {round(top_prob * 100, 3)}%"
    string_text_2 = f"chance that the number is a {top_prediction}."
    text_id_1 = canvas.create_text(target_x + 137, target_y + 40, text = string_text_1, fill="black")
    text_id_2 = canvas.create_text(target_x + 137, target_y + 80, text = string_text_2, fill="black")
    box_y, box_x = top_index%9, int(top_index / 9)
    x_pixel, y_pixel= TOP_LEFT_X + GRID_SIZE*box_x+30, TOP_LEFT_Y + GRID_SIZE*box_y+15

    line_id = canvas.create_line(target_x, target_y, x_pixel, y_pixel, width=2, fill=color)

    return box_id, line_id, text_id_1, text_id_2

def change_focus(canvas, x, y):
    global current_box_focus
    current_box_focus = (x, y)
    all_possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    not_poss = get_possbilities_rows(x, y)      #returns [1, 2, 3, 4, 7]
    not_poss = not_poss.union(get_possbilities_columns(x, y))   #returns [6, 7, 8, 9]
    not_poss = not_poss.union(get_possbilities_square(x, y))
    grey_out_options(canvas, all_possibilities - not_poss )
    model_HUDS(canvas)

def model_HUDS(canvas):
    global model_box_ids
    top, second, third = use_model.get_top_3(board) #prob, index, prediction
    top_cord, second_cord, third_cord = (860, 30), (860, 30+3*GRID_SIZE), (860, 30+6*GRID_SIZE)

    for id in model_box_ids:
        for i in id:
            canvas.delete(i)
    model_box_ids = []
    print("Top Three: ", top, second, third)
    if top[0] != 0:
        model_box_ids.append(draw_model_box(canvas, top_cord, top, "green"))
    if second[0] != 0:
        model_box_ids.append(draw_model_box(canvas, second_cord, second, "orange"))
    if third[0] != 0:
        model_box_ids.append(draw_model_box(canvas, third_cord, third, "yellow"))


def space_event(event, canvas):
    '''When space bar is pressed, find top possbilitiy and fill in box,
        helpful text popping up.'''

    (top_prob, top_index, top_prediction), (second_prob, second_index, second_prediction), (third_prob, third_index, third_prediction) = use_model.get_top_3(board)

    #print("Top Three: ", (top_prob, top_index, top_prediction), (second_prob, second_index, second_prediction), (third_prob, third_index, third_prediction))
    top_y, top_x = top_index%9, int(top_index / 9)
    #draw_board()
    print(f"Top x,y: ({top_x},{top_y})")
    if top_prob != 0:
        canvas.itemconfig(boxes[top_x][top_y], fill="black")
        draw_number(canvas, top_x, top_y, top_prediction, color='green')
        model_HUDS(canvas)

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
                print(f"Current focus is ({x},{y}) which is #: {board[x][y]}")
                canvas.delete(numbers_ids[x][y])
                board[x][y] = 0
                change_focus(canvas, x, y)
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
                if ((i+1) in global_possbilities) and board[x][y] == 0:
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

    canvas.focus_set()
    canvas.bind('<Button-1>', lambda event:mouse_parser(event, canvas, boxes))
    canvas.bind('<Button-3>', lambda event:mouse_parser_right(event, canvas))
    canvas.bind('<space>', lambda event:space_event(event, canvas))
