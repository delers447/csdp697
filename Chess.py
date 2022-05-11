# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 07:51:14 2022

@author: j.casuzu
"""


#chess file module
import tkinter as tk, numpy as np, math, QueenSolution as qs
from PIL import ImageTk, Image

#Creates Main Grid
def Chess_grid(canvas, gridcolor):
    global GRIDWIDTH_START, GRID_WIDTH, GRIDHEIGHT_START, GRID_HEIGHT
    grid_centers= [] 
    counter = 0
    
    for j in range(GRIDHEIGHT_START, GRID_HEIGHT, GRIDUNIT_SIZE):
        for i in range(GRIDWIDTH_START, GRID_WIDTH, GRIDUNIT_SIZE):
            
            grid_centers.append([])
            grid_centers[counter].append(i+(GRIDUNIT_SIZE/2))
            grid_centers[counter].append(j+(GRIDUNIT_SIZE/2))
            #print("[", grid_centers[counter][0], ", ", grid_centers[counter][1], "]")
            counter += 1
            
            gridcolor, fill_color = Alt_fill(gridcolor)
            canvas.create_rectangle(i, j, i+GRIDUNIT_SIZE, j+GRIDUNIT_SIZE, fill=fill_color)
        gridcolor, fill_color = Alt_fill(gridcolor)  
    #grid_centers = np.reshape(grid_centers, (8, 8))
    return GRIDHEIGHT_START, grid_centers

#Creates side grid            
def Chess_sidegrid(canvas, top_height, sideGrid_Size):
    column = SCREENWIDTH - sideGrid_Size - wall_space 
    canvas.create_rectangle(column, top_height, column + sideGrid_Size, top_height + sideGrid_Size, fill = '#FFD59A' )       
    return column, top_height

#Alternates Grid Colors           
def Alt_fill(gridcolor):
    if(gridcolor):
        gridcolor = False
        return gridcolor, '#FFD59A' #light brown
    else:
        gridcolor = True
        return gridcolor, '#CC7722'  #Dark brown
    

   
#Prepares the image to be dispalyed on the canvas
#BorderSpaceX and BorderSpaceY govern the space between the image and the border it is in
def Image_preparer(filepath, BorderSpaceX, BorderSpaceY, objectForm):
    imgtemp = Image.open(filepath)
    
    if(objectForm == "button"):  
       imgtemp = imgtemp.resize((BorderSpaceX, BorderSpaceY))  
    elif(objectForm=="frame"):
        imgtemp = imgtemp.resize((BorderSpaceX, BorderSpaceY))  
    else:
        imgtemp = imgtemp.resize((GRIDUNIT_SIZE + BorderSpaceX, GRIDUNIT_SIZE + BorderSpaceY))
    
    #Creates the image object
    finalImage = ImageTk.PhotoImage(imgtemp)   
    return finalImage
  

def MoveQueen_image(e, a, gCenters, side_xpos, side_ypos):
    global queentags_count
    shift = 115
    Queen_selector(e.x, e.y)
    tag = queen_Tags[queentags_count]
    
    rangex1 = int(queensPositions[queentags_count][0] - shift)
    rangex2 = int(queensPositions[queentags_count][0] + shift)
    rangey1 = int(queensPositions[queentags_count][1] - shift)
    rangey2 = int(queensPositions[queentags_count][1] + shift)
    
    if (e.x in range(rangex1, rangex2)and e.y in range(rangey1, rangey2)):
    
        tagXpos, tagYpos = a.coords(queen_Tags[queentags_count]) 
    
        moveby_Xpos, moveby_Ypos = e.x- tagXpos, e.y - tagYpos
        a.move(tag,  moveby_Xpos, moveby_Ypos) 
        
      
        queensPositions[queentags_count][0] = tagXpos + moveby_Xpos
        queensPositions[queentags_count][1] = tagYpos + moveby_Ypos
        
        #print(queentags_count)
        a.bind("<ButtonRelease-1>", 
                lambda e: Button_released(e.x,
                                          e.y,
                                          a = a,
                                          tag = queen_Tags[queentags_count], 
                                          gCenters = gCenters,
                                          side_xpos = side_xpos,
                                          side_ypos = side_ypos))


def Grid_snap(canvas, grid_centers, tag, side_xpos, side_ypos):
    posX, posY = 0, 0
    tagXpos, tagYpos = canvas.coords(tag)    
    short_dist = math.dist([tagXpos, tagYpos], [ grid_centers[0][0] , grid_centers[0][1] ])
    
    if((tagXpos in range(GRIDWIDTH_START, GRID_WIDTH)) and (tagYpos in range(GRIDHEIGHT_START, GRID_HEIGHT))):
       for i in range(len(grid_centers)):
           distance = math.dist([tagXpos, tagYpos], [grid_centers[i][0], grid_centers[i][1]])
           if(distance <= short_dist):
                short_dist = distance
                Px, Py = grid_centers[i][0], grid_centers[i][1]
                posX, posY = int(i%8), int(i/8) 
              
           snapXpos, snapYpos = Px, Py 
           insideGrid = True  
           
           
    else:
        insideGrid = False
        snapXpos, snapYpos = side_xpos, side_ypos
    
    #print("PX, PY = [", Px, " ", Py, "] ")
    return insideGrid, posX, posY, snapXpos, snapYpos

def Button_released(mouseX, mouseY, a, tag, gCenters, side_xpos, side_ypos):
    global queentags_count, queenSelectFlag
    global GRIDWIDTH_START, GRID_WIDTH, GRIDHEIGHT_START, GRID_HEIGHT, GRIDUNIT_SIZE
    global queensPositions, queensMatrix, lastqueensPositions
   
    InsideGrid, matrixPosX, matrixPosY, snapXpos, snapYpos = Grid_snap(a, 
                                                                       gCenters,
                                                                       tag,
                                                                       side_xpos,
                                                                       side_ypos)
    
    tagXpos, tagYpos = a.coords(tag) 
    sameSquareFlag = False
         
    if(( mouseX == tagXpos)and(mouseY == tagYpos)):
            if(queensMatrix[matrixPosY][matrixPosX] == 1):
                snapXpos = lastqueensPositions[queentags_count][0]
                snapYpos = lastqueensPositions[queentags_count][1]
                sameSquareFlag = True
                
            moveby_Xpos = snapXpos - mouseX
            moveby_Ypos = snapYpos - mouseY
           
    else:
        moveby_Xpos, moveby_Ypos = 0, 0
        
    #Update the queen's new X and Y positions
    queensPositions[queentags_count][0] = tagXpos + moveby_Xpos
    queensPositions[queentags_count][1] = tagYpos + moveby_Ypos
    
    #Get the grid index from the queens last x and y positions
    OldXpos = (lastqueensPositions[queentags_count][0] - (GRIDUNIT_SIZE/2) - GRIDWIDTH_START)/GRIDUNIT_SIZE 
    OldYpos = (lastqueensPositions[queentags_count][1] - (GRIDUNIT_SIZE/2) - GRIDHEIGHT_START)/GRIDUNIT_SIZE 

    OldXpos, OldYpos = round(OldXpos), round(OldYpos)

    
    if(InsideGrid and (not sameSquareFlag)): 
        #Update the grid matrix with 1 for the queen current position
        queensMatrix[matrixPosY][matrixPosX] = 1
        
        #Update the grid matrix with 0 for the queen past position
        if(OldXpos in range(0, 8) and OldYpos in range(0, 8)):
            queensMatrix[OldYpos][OldXpos] = 0
            
        lastqueensPositions[queentags_count][0] = snapXpos
        lastqueensPositions[queentags_count][1] = snapYpos
     
    elif(not InsideGrid):
        if(OldXpos in range(0, 8) and OldYpos in range(0, 8)):
            queensMatrix[OldYpos][OldXpos] = 0
            
    
    a.move(tag,  moveby_Xpos, moveby_Ypos) 
    moveby_Xpos, moveby_Ypos = 0, 0
    queenSelectFlag = True
        
   
def Queen_selector(ex, ey):
    global queentags_count, queensPositions, queenSelectFlag
    if(queenSelectFlag):
        short_dist = distance = math.dist([ex, ey], [queensPositions[0][0], queensPositions[0][1]])
        selectedqueen_tag = 0
        for i in range(len(queensPositions)):
            distance = math.dist([ex, ey], [queensPositions[i][0], queensPositions[i][1]])
            if(distance < short_dist):
                 short_dist = distance
                 selectedqueen_tag = i 
        
        queentags_count = selectedqueen_tag
        queenSelectFlag = False
        
    
    
def Submit(a, gridXpos, gridYpos):
    
    userAns = tk.messagebox.askokcancel('Submit', 'Submit current solution?')
    if (userAns):
        if(Solution_check()):
            tk.messagebox.showinfo('SUCCESS', 'YOU WIN!')
        else:
            tk.messagebox.showwarning('Aww', 'Better luck next time!')
            userAns = tk.messagebox.askokcancel('Retry', 'Do you wish to try again?')
            
            if(userAns):
                Reset(a, gridXpos, gridYpos)
        
    
       
   
def Solution_check2():   
    print(2)
    global queensMatrix, SOLUTION
    num = 8
    skipFlag = False
    win = False
    foundFlag = False
    
    for j in range(0, num):
        if(skipFlag or foundFlag):
            break
        
        for k in range(0, num):
            if(queensMatrix[j][k] != SOLUTION[i][j][k]):
                skipFlag = True
                
            if(skipFlag):
                break
            
        if(not skipFlag):
            foundFlag = True
            
    # if(not skipFlag):
    #     win = True
    #     break 

    skipFlag = False

    
    
def Solution_check():
    global queensMatrix, SOLUTION
    num = 8
    skipFlag = False
    win = False
    foundFlag = False
  
    for i in range(0, len(SOLUTION)):
        if(foundFlag):
            break 
        
        for j in range(0, num):
            if(skipFlag or foundFlag):
                break
            
            for k in range(0, num):
                if(queensMatrix[j][k] != SOLUTION[i][j][k]):
                    skipFlag = True
                    
                if(skipFlag):
                    break
                
            if(not skipFlag):
                foundFlag = True
                
        if(not skipFlag):
            win = True
            break 
   
        skipFlag = False

    return(win)
                
                
def Hint():
    global queensMatrix
    print("Hint")    

def DisplayMatrix():
    global queensMatrix, queensPositions, lastqueensPositions
    print("==========================")
    print("GO!\n")
    print(queensMatrix)
    #print(lastqueensPositions)
   # print(queensPositions)
    
    
    
def Reset(a, gridXpos, gridYpos):
    global queen_Tags, queentags_count, queensPositions, queensMatrix, NUM_OF_QUEENS
    queentags_count = 0
    queensMatrix.fill(0)
   
    for i in range(0, NUM_OF_QUEENS):
            lastqueensPositions[i][0] = -1
            lastqueensPositions[i][1] = -1
            tag = queen_Tags[i]
            tagXpos, tagYpos = a.coords(tag) 
            
            moveby_Xpos = gridXpos - tagXpos
            moveby_Ypos = gridYpos - tagYpos
            
            queensPositions[i][0] = tagXpos + moveby_Xpos
            queensPositions[i][1] = tagYpos + moveby_Ypos
            
            a.move(tag,  moveby_Xpos, moveby_Ypos) 
            moveby_Xpos, moveby_Ypos = 0, 0


def CloseApp():
    DisplayMatrix()
    print("Closed\n")
    
       
    
def Chess_main(canvas):
    global SCREENWIDTH, SCREENHEIGHT, GRIDUNIT_SIZE, FRAMEGRIDUNIT_SIZE
    global wall_space, AnchorPos,queenList
    global queenimg_filepath, greenArrow_filepath, blueHelp_filepath, redArrow_filepath
    global closeButton_filepath,chessboardframe_filepath
    
    gridcolor = True
    bottombar_color = '#373737'
    x1 = 2.5
    
    frameGridWidthStart = int((SCREENWIDTH/2)-(4*FRAMEGRIDUNIT_SIZE))
    frameGridWidth = int((SCREENWIDTH/2)+(4*FRAMEGRIDUNIT_SIZE))
    frameGridHeightStart =int((SCREENHEIGHT/2)-(4*FRAMEGRIDUNIT_SIZE))
    frameGridHeight = int((SCREENHEIGHT/2)+(4*FRAMEGRIDUNIT_SIZE))
    
    frame_thickness = 350
    frame_xpos = ((frameGridWidth - frameGridWidthStart)/2) + frameGridWidthStart -10
    frame_ypos = ((frameGridHeight - frameGridHeightStart)/2) + frameGridHeightStart - 60
    frame_width = (frameGridWidth - frameGridWidthStart) + frame_thickness
    frame_height = (frameGridHeight - frameGridHeightStart) + frame_thickness

    buttonWidth, buttonHeight = GRIDUNIT_SIZE, GRIDUNIT_SIZE 
    
    canvas.delete('all')
    # window = tk.Tk()
    # window.geometry(f"{SCREENWIDTH}x{SCREENHEIGHT}")
    # canvas = tk.Canvas(window, height=SCREENHEIGHT, width= SCREENWIDTH, bg="black")
    # canvas.pack()
    
    top_height, grid_centers = Chess_grid(canvas, gridcolor)
    sidegrid_xpos, sidegrid_ypos = Chess_sidegrid(canvas, top_height, GRIDUNIT_SIZE )
    queen_sidegrid_xpos = sidegrid_xpos + (GRIDUNIT_SIZE/2)
    queen_sidegrid_ypos = sidegrid_ypos + (GRIDUNIT_SIZE/2)
    
    
    frame_Image = Image_preparer(chessboardframe_filepath, frame_width, frame_height, "frame")
    queen_Image = Image_preparer(queenimg_filepath,-wall_space , -wall_space , "image")
    greenArrow_Image = Image_preparer(greenArrow_filepath, buttonWidth, buttonHeight, "button")
    blueHelp_Image =  Image_preparer(blueHelp_filepath, buttonWidth, buttonHeight, "button")
    redArrow_Image = Image_preparer(redArrow_filepath, buttonWidth, buttonHeight, "button")
    closeButton_Image = Image_preparer(closeButton_filepath , buttonWidth, buttonHeight, "button")
    
    
    
    #Create frame image on canvas
    canvas.create_image(frame_xpos, frame_ypos,
                        anchor = AnchorPos, 
                        image = frame_Image)
   
    #Create queen image on canvas
    for i in range(0, NUM_OF_QUEENS):
        canvas.create_image( queen_sidegrid_xpos, queen_sidegrid_ypos,
                                        anchor = AnchorPos,
                                        image=queen_Image,
                                        tags = (queen_Tags[i]))
        
        queensPositions[i].append(queen_sidegrid_xpos)
        queensPositions[i].append(queen_sidegrid_ypos)
        lastqueensPositions[i].append(-1)
        lastqueensPositions[i].append(-1)
        
      
       
    
    #Create bottom side bar
    canvas.create_rectangle(0, SCREENHEIGHT - 1.5*GRIDUNIT_SIZE,
                            SCREENWIDTH , SCREENHEIGHT,
                            fill = bottombar_color, 
                            outline = '#FFD59A')       
    
    #Create submit, undo, and close buttons
    submit_Button = tk.Button(canvas,
                              image = greenArrow_Image,
                              width = buttonWidth,
                              height = buttonHeight,
                              activebackground =bottombar_color,
                              bg = bottombar_color,
                              bd = '0',
                              command = lambda:Submit(canvas, queen_sidegrid_xpos, queen_sidegrid_ypos))
    
    submit_Button.place(x =((SCREENWIDTH/2)+x1*GRIDUNIT_SIZE),
                        y = (SCREENHEIGHT - 1.375*GRIDUNIT_SIZE))
    
    canvas.create_text((SCREENWIDTH/2)+x1*GRIDUNIT_SIZE + 20 ,
                       (SCREENHEIGHT - 1.3125*GRIDUNIT_SIZE)+50, 
                       text="SUBMIT", fill="white",
                       font=("Helvetica", 7, "bold"))
    
    hint_Button = tk.Button(canvas,
                              image = blueHelp_Image,
                              width = buttonWidth,
                              height = buttonHeight,
                              activebackground =bottombar_color,
                              bg = bottombar_color,
                              bd = '0',
                              command = Hint())
    
    hint_Button.place(x =((SCREENWIDTH/2) - (blueHelp_Image.width()/2)),
                        y = (SCREENHEIGHT - 1.375*GRIDUNIT_SIZE))
    
    canvas.create_text((SCREENWIDTH/2),
                       (SCREENHEIGHT - 1.3125*GRIDUNIT_SIZE)+50, 
                       text="HELP", fill="white",
                       font=("Helvetica", 7, "bold"))
    
    reset_Button = tk.Button(canvas,
                            image = redArrow_Image,
                            width = buttonWidth,
                            height = buttonHeight,
                            activebackground =bottombar_color,
                            bg = bottombar_color,
                            bd = '0',
                            command = lambda:Reset(canvas, queen_sidegrid_xpos, queen_sidegrid_ypos))
    
    reset_Button.place(x = ((SCREENWIDTH/2)-x1*GRIDUNIT_SIZE - redArrow_Image.width()),
                      y = (SCREENHEIGHT - 1.375*GRIDUNIT_SIZE))
    
    canvas.create_text((SCREENWIDTH/2)-x1*GRIDUNIT_SIZE - redArrow_Image.width() + 20,
                       (SCREENHEIGHT - 1.3125*GRIDUNIT_SIZE)+50,
                       text="RESET", fill="white",
                       font=("Helvetica", 7,  "bold"))
    
    close_Button = tk.Button(canvas,
                             image = closeButton_Image,
                             width = buttonWidth, 
                             height = buttonHeight, 
                             activebackground =bottombar_color,
                             bg = bottombar_color, 
                             bd = '0', 
                             command = CloseApp)
    
    close_Button.place(x = GRIDUNIT_SIZE,
                       y = (SCREENHEIGHT - 1.375*GRIDUNIT_SIZE))
   
    canvas.create_text(GRIDUNIT_SIZE + 20,
                       (SCREENHEIGHT - 1.3125*GRIDUNIT_SIZE)+50, 
                       text="CLOSE", fill="white", 
                       font=("Helvetica", 7, "bold"))
    
    canvas.bind("<B1-Motion>", 
                lambda e: MoveQueen_image(e, a = canvas,
                                          gCenters = grid_centers,
                                          side_xpos = queen_sidegrid_xpos,
                                          side_ypos = queen_sidegrid_ypos))
                                                    

    canvas.mainloop()











NUM_OF_GRIDS = 64
NUM_OF_QUEENS = 64
AnchorPos = tk.CENTER
wall_space = 5
queentags_count = 0
widthShift = 5
heightShift = 30
moveMemoryIndex = 0
queenSelectFlag = False

SOLUTION = qs.get_data()
SCREENWIDTH, SCREENHEIGHT =1150, 720
GRIDUNIT_SIZE = int(math.ceil((47/ SCREENWIDTH )*(SCREENWIDTH)))
FRAMEGRIDUNIT_SIZE = int(math.ceil((80/ SCREENWIDTH )*(SCREENWIDTH)))

GRIDWIDTH_START = int((SCREENWIDTH/2)-(4*GRIDUNIT_SIZE)) - widthShift#382
GRID_WIDTH = int((SCREENWIDTH/2)+(4*GRIDUNIT_SIZE)) - widthShift#758
GRIDHEIGHT_START =int((SCREENHEIGHT/2)-(4*GRIDUNIT_SIZE)) -heightShift#142
GRID_HEIGHT = int((SCREENHEIGHT/2)+(4*GRIDUNIT_SIZE)) -heightShift#518'

queenimg_filepath = "References\\Queen_Icon.png"
greenArrow_filepath = "References\\GreenArrowTransparent.png"
blueHelp_filepath = "References\\BlueHelpTransparent.png"
redArrow_filepath = "References\\RedArrowTransparent.png"
closeButton_filepath = "References\\CloseButtonTransparent.png"
chessboardframe_filepath = "References\\Chessboard_GoldFrame.png"

queen_Tags = []
queensPositions = []
lastqueensPositions = []

if(NUM_OF_QUEENS > 0):
    gridlist = []
    for i in range(0, NUM_OF_QUEENS):
        queensPositions.append([])
        lastqueensPositions.append([])
        queen_Tags.append("Tag"+str(i))
        
    for i in range(0, NUM_OF_GRIDS):   
        gridlist.append(0)
    
    
    queensMatrix = np.reshape(gridlist, (8, 8))
   # Chess_main(canvas)
