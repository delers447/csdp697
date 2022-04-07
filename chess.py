
#chess file module
from tkinter import*
import tkinter as tk
import math
from PIL import ImageTk, Image

#Creates Main Grid
def chess_grid(canvas, gridcolor):
   # grid_centers= [[], []] 
    widthShift = 5
    heightShift = 30
    GridWidthStart = int((ScreenWidth/2)-(4*GridUnit_Size)) - widthShift
    GridWidth = int((ScreenWidth/2)+(4*GridUnit_Size)) - widthShift
    GridHeightStart =int((ScreenHeight/2)-(4*GridUnit_Size)) -heightShift
    GridHeight = int((ScreenHeight/2)+(4*GridUnit_Size)) -heightShift
    
    print("gridwidthstart = ", GridWidthStart )
    print("gridwidth = ", GridWidth)
    print("gridheightstart = ", GridHeightStart )
    for j in range(GridHeightStart, GridHeight, GridUnit_Size):
        for i in range(GridWidthStart, GridWidth, GridUnit_Size):
            #grid_centers.append(GridWidth , GridHeightStart)
            gridcolor, fill_color = alt_Fill(gridcolor)
            canvas.create_rectangle(i, j, i+GridUnit_Size, j+GridUnit_Size, fill=fill_color)
        gridcolor, fill_color = alt_Fill(gridcolor)
    return chess_sidegrid(canvas, GridHeightStart, GridUnit_Size)

#Alternates Grid Colors           
def alt_Fill(gridcolor):
    if(gridcolor):
        gridcolor = False
        return gridcolor, '#FFD59A' #light brown
    else:
        gridcolor = True
        return gridcolor, '#654321'  #Dark brown
    
#Creates side grid            
def chess_sidegrid(canvas, top_height, sideGrid_Size):
    column = ScreenWidth - sideGrid_Size - wall_space 
    canvas.create_rectangle(column, top_height, column + sideGrid_Size, top_height + sideGrid_Size, fill = '#FFD59A' )       
    return column, top_height
    
#Prepares the image to be dispalyed on the canvas
#BorderSpaceX and BorderSpaceY govern the space between the image and the border it is in
def image_Preparer(filepath, BorderSpaceX, BorderSpaceY, objectForm):
    imgtemp = Image.open(filepath)
    
    if(objectForm == "button"):  
       imgtemp = imgtemp.resize((BorderSpaceX, BorderSpaceY))  
    elif(objectForm=="frame"):
        imgtemp = imgtemp.resize((BorderSpaceX, BorderSpaceY))  
    else:
        imgtemp = imgtemp.resize((GridUnit_Size + BorderSpaceX, GridUnit_Size + BorderSpaceY))
    
    #Creates the image object
    finalImage = ImageTk.PhotoImage(imgtemp)   
    return finalImage
  

def moveQueen_Image(e, a, tag):
    tagXpos, tagYpos =a.coords(tag)  
    a.move(tag,  e.x- tagXpos, e.y - tagYpos) 


  
    
def DoSomething():
    print("GO!\n")
   
def Undo():
    print("Undo\n")

def CloseApp():
    print("Closed\n")
    
       
    
def chess_main():
    global ScreenWidth, ScreenHeight, GridUnit_Size, wall_space
    ScreenWidth = 1150
    ScreenHeight =720
    #GridUnit_Size = int(math.ceil((0.13)*(ScreenWidth)))
    GridUnit_Size = int(math.ceil((47/ ScreenWidth )*(ScreenWidth)))
    frameGridUnit_Size = int(math.ceil((80/ ScreenWidth )*(ScreenWidth)))
    AnchorPos = tk.CENTER
    wall_space = 5
    print("Grid size =", GridUnit_Size)
    
    window = tk.Tk()
    window.geometry(f"{ScreenWidth}x{ScreenHeight}")

    canvas = tk.Canvas(window, height=ScreenHeight, width= ScreenWidth, bg="black")
    canvas.pack()
    
    gridcolor = True
    bottombar_color = '#373737'
    
    queenimg_filepath = "References\\Queen_Icon.png"
    greenArrow_filepath = "References\\GreenArrowTransparent.png"
    redArrow_filepath = "References\\RedArrowTransparent.png"
    closeButton_filepath = "References\\closeButtonTransparent.png"
    chessboardframe_filepath = "References\\Chessboard_GoldFrame.png"
    
    frameGridWidthStart = int((ScreenWidth/2)-(4*frameGridUnit_Size))
    frameGridWidth = int((ScreenWidth/2)+(4*frameGridUnit_Size))
    frameGridHeightStart =int((ScreenHeight/2)-(4*frameGridUnit_Size))
    frameGridHeight = int((ScreenHeight/2)+(4*frameGridUnit_Size))
    
    frame_thickness = 350
    frame_xpos = ((frameGridWidth - frameGridWidthStart)/2) + frameGridWidthStart -10
    frame_ypos = ((frameGridHeight - frameGridHeightStart)/2) + frameGridHeightStart - 60
    frame_width = (frameGridWidth - frameGridWidthStart) + frame_thickness
    frame_height = (frameGridHeight - frameGridHeightStart) + frame_thickness
    
    buttonWidth = GridUnit_Size 
    buttonHeight = GridUnit_Size 
    
    queen_Image = image_Preparer(queenimg_filepath,-wall_space , -wall_space , "image")
    
    frame_Image = image_Preparer(chessboardframe_filepath, frame_width, frame_height, "frame")
    greenArrow_Image = image_Preparer(greenArrow_filepath, buttonWidth, buttonHeight, "button")
    redArrow_Image = image_Preparer(redArrow_filepath, buttonWidth, buttonHeight, "button")
    closeButton_Image = image_Preparer(closeButton_filepath , buttonWidth, buttonHeight, "button")
    
    #Create frame image on canvas
    canvas.create_image(frame_xpos, frame_ypos, anchor = AnchorPos, image = frame_Image)
    sidegrid_xpos, sidegrid_ypos = chess_grid(canvas, gridcolor)
    #Create queen image on canvas
    canvas.create_image( sidegrid_xpos +(GridUnit_Size/2), sidegrid_ypos+(GridUnit_Size/2), anchor = AnchorPos , image=queen_Image, tags = ('queenImage'))
    
    #Create bottom side bar
    canvas.create_rectangle(0, ScreenHeight - 1.5*GridUnit_Size, ScreenWidth , ScreenHeight, fill = bottombar_color, outline = '#FFD59A')       
    
    #Create submit, undo, and close buttons
    submit_Button = tk.Button(window, image = greenArrow_Image , width = buttonWidth, height = buttonHeight, activebackground =bottombar_color, bg = bottombar_color, bd = '0', command = DoSomething)
    submit_Button.place(x =((ScreenWidth/2)+GridUnit_Size), y = (ScreenHeight - 1.375*GridUnit_Size))
    canvas.create_text((ScreenWidth/2)+GridUnit_Size + 20 , (ScreenHeight - 1.3125*GridUnit_Size)+50, text="SUBMIT", fill="white", font=("Helvetica", 7, "bold"))
    
    undo_Button = tk.Button(window, image = redArrow_Image , width = buttonWidth, height = buttonHeight, activebackground =bottombar_color, bg = bottombar_color, bd = '0', command = Undo)
    undo_Button.place(x = ((ScreenWidth/2)-2*GridUnit_Size), y = (ScreenHeight - 1.375*GridUnit_Size))
    canvas.create_text((ScreenWidth/2)-2*GridUnit_Size + 20 , (ScreenHeight - 1.3125*GridUnit_Size)+50, text="UNDO", fill="white", font=("Helvetica", 7,  "bold"))
    
    close_Button = tk.Button(window, image = closeButton_Image, width = buttonWidth, height = buttonHeight, activebackground =bottombar_color, bg = bottombar_color, bd = '0', command = CloseApp)
    close_Button.place(x = GridUnit_Size, y = (ScreenHeight - 1.375*GridUnit_Size))
    canvas.create_text(GridUnit_Size + 20, (ScreenHeight - 1.3125*GridUnit_Size)+50, text="CLOSE", fill="white", font=("Helvetica", 7, "bold"))
    
    canvas.bind("<B1-Motion>", lambda e: moveQueen_Image(e, a = canvas, tag = 'queenImage'))
    
    window.mainloop()


 

chess_main()
