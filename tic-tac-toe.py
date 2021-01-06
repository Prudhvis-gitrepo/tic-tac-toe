#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import cv2

#This function checks if the game has ended and returns the winner respectively
def is_end(board):
    #checking if a player put three in a row of board matrix row.
    for i in range(0, 3):
        if (board[0][i] == board[1][i] == board[2][i] !="-"):
            return board[0][i]

    #checking if a player put three in a row of board matrix column.
    for i in range(0, 3):
        if (board[i] == ['X', 'X', 'X']):
            return 'X'
        elif (board[i] == ['O', 'O', 'O']):
            return 'O'

    #checking if a player put three in a row of board matrix diagonal.
    if (board[1][1] == board[0][0] == board[2][2] !="-"):
        return board[0][0]

    #checking if a player put three in a row of board matrix diagonal.
    if (board[0][2] == board[1][1] == board[2][0] !="-"):
        return board[0][2]

    #Checking for the empty box to continue the game
    for i in range(0, 3):
        for j in range(0, 3):
            #Checking if there's an empty field to continue the game
            if (board[i][j] == '-'):
                return None

    #Checking if it's a tie!
    return '-'
   
#This function is utility function to find other player mark easily
def rev(mark):
    if mark=='X':
        return 'O'
    else:
        return 'X'
    
#This function is utility function to find number of tiles is filled with X and O
def noftiles(board):
    tileo=0
    tilex=0
    for i in range(0, 3):
        for j in range(0, 3):
            #counting number of X filled tiles.
            if (board[i][j] == 'X'):
                tilex=tilex+1

            #counting number of O filled tiles.
            elif(board[i][j]=='O'):
                tileo=tileo+1
    return(tileo,tilex)

#This function helps to choose an option to min
def take_choice(board,mark):
    temp,x1,y1=max(board,mark,10)
    print("Next move for the",mark,"symbol using player is (",x1,y1,")")

def print_board(board):
    print("Given Present state of tic-tac-toe board:")
    for line in board:
        linetxt = ""
        for tile in line:
            linetxt = linetxt + " | " + tile
        print(linetxt+" |")
    print()

#minimising strategy
def min(board,mark,value):
    #initialising with 2
    minv = 2
    
    #Cordinates initialising with none
    qx = None
    qy = None
    
    #print("At min")
    #print_board(board)
    
    #checking is if game is ended or not
    result = is_end(board)
    #As this is minimising strategy if the given mark player won we return negative value
    if result == mark:
        return (-value, 0, 0)
    #As this is minimising strategy if the given mark player lose we return positive value
    elif result == rev(mark):
        return (value, 0, 0)
    #if there is tie or any we would return neutral value
    elif result == '-':
        return (0, 0, 0)
    
    #checking for every possible moves in the given board
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '-':
                #taking the possible move temporarily
                board[i][j] = mark
                #checking the optimal by taking temporary move
                (m, max_i, max_j) = max(board,rev(mark),value-1)
                
                #choosing optimal min value and it's appropriate coordinates
                if m < minv:
                    minv = m
                    qx = i
                    qy = j
                
                #reverting back the temporary move
                board[i][j] = '-'
    return (minv, qx, qy)
        
#maximising strategy
def max(board,mark,value):
    #initialising with -2
    maxv = -2
    
    #Cordinates initialising with none
    px = None
    py = None
    
    #print("At max")
    #print_board(board)
    
    #checking is if game is ended or not
    result = is_end(board)
    #As this is maximising strategy if the given mark player won we return positive value
    if result == mark:
        return (value, 0, 0)
    #As this is maximising strategy if the given mark player lose we return negative value
    elif result == rev(mark):
        return (-value, 0, 0)
    #if there is tie or any we would return neutral value
    elif result == '-':
        return (0, 0, 0)

    #checking for every possible moves in the given board
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == '-':
                #taking the possible move temporarily
                board[i][j] = mark
                (m, min_i, min_j) = min(board,rev(mark),value-1)
                #Choosing optimal max value and it's appropriate coordinates
                if m > maxv:
                    maxv = m
                    px = i
                    py = j
                
                #reverting back the temporary move
                board[i][j] = '-'
    return (maxv, px, py)

#creating 2d array to save the state of game
board = [["-","-","-"],["-","-","-"],["-","-","-"]]

#Loading a colour image 
image = cv2.imread('tic o move.jpg')
cv2.imshow("Given Image",image)

#getting original image width.
image_width = image.shape[0]
#getting original image height.
image_height = image.shape[1]

#converting BGR colour image into grayscale image
image_gscale =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#converting into thresholded binary
ret,opening = cv2.threshold(image_gscale,127,255,cv2.THRESH_BINARY)

#kernel going to be used for removal of noise.
kernel =  np.ones((7,7),np.uint8)

#removing the noise.
opening = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)

#Extracting the contours from the image.
#RETR_EXTERNAL retrieves only the extreme outer contours
contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#draws all contours
#-1 signifies drawing all contours.
cv2.drawContours(image, contours, -1, (0,255,0), 15)
#cv2.imshow("im",image)

d=0 #used to track tile count
for cnt in contours:
        #ignoring small contours that are not tiles
        #e=e+1
        if cv2.contourArea(cnt) > 5000: 
                #To get coordinates of each tile
                x,y,w,h = cv2.boundingRect(cnt)
                d=d+1
                
                # create new image from binary, for further analysis. Trim off the edge that has a line
                tile = opening[x+40:x+w-80,y+40:y+h-80]
                
                # create new image from main image, so we can draw the contours easily
                imageTile = image[x+40:x+w-80,y+40:y+h-80]

                #determine the array indexes of the tile
                tileX = round((x/image_width)*3)
                tileY = round((y/image_height)*3)     

                # find contours in the tile image. RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours.
                cont, hierarchy = cv2.findContours(tile, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
                for con in cont:
                        #to prevent the tile finding itself as contour
                        if cv2.contourArea(con) < 18000:
                                cv2.drawContours(imageTile, [con], -1, (255,0,0), 15)
                                #calculating the full area
                                area = cv2.contourArea(con)
                                #calculating the hull area
                                hull = cv2.convexHull(con)
                                hull_area = cv2.contourArea(hull)
                                #calculating the solidity
                                solidity = float(area)/hull_area

                                #getting the signs of tic-tac-toe in game in each tile 
                                if(solidity > 0.5 ):
                                        board[tileX][tileY] = "X"
                                        
                                elif(solidity<0.5): 
                                        board[tileX][tileY] = "O"

tileo,tilex=noftiles(board)
#print(tileo,tilex)                
print_board(board)
if tilex==tileo or tileo==tilex+1 or tileo+1==tilex:
    print("The provided state of tic-tac-toe board is valid.\n")
    temp=is_end(board)
    if temp!=None and temp!="-":
        print("Player played with",temp,"symbol won game.")
    else:
        print("No player has won the game until now.\n")
        if(tileo==tilex+1):
            take_choice(board,'X')
        elif(tileo+1==tilex):
            take_choice(board,'O')
        else:
            temp=input("first player symbol:")
            take_choice(board,temp)
            #if(temp=='X'):
             #   take_choice(board,'X')
            #elif(temp=='O'):
             #   take_choice(board,'O')
else:
    print("The provided state of tic-tac-toe board is invalid.")
cv2.imshow('image1',image)
cv2.waitKey(0)
cv2.destroyAllWindows()