#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import random
from menu import *
pygame.init()#Open pygame


grid_color = (128, 128, 128) # Here we can choose the color of the cases


if level == "Easy":
    size = 10
    mine = 9
    bg_color = (39, 225, 14) # Here we can choose the color of the back screen
elif level == "Medium":
    size = 13
    mine = 20
    bg_color = (231, 240, 53)
elif level == "Hard":
    size = 16
    mine = 30
    bg_color = (240, 145, 58)
elif level == "Extreme":
    size = 20
    mine = 40
    bg_color = (240, 0, 0)


game_width = size  # Defines the size of game
game_height = size  # Defines the size of the game
numMine = mine  # Number of mines
grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)
border = 16  # Top border
top_border = 100  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0)) #means Calibri in black
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    def __init__(self, xGrid, yGrid, type): #it creates the variables we will use afterward and set there basic values
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)#it moves a rectangular form to the desired place
        self.val = type  # Value of the grid, -1 is mine

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked: #Triggers the function if we (left) click a case, i.e. if self.clicked = True
                if self.val == -1: #-1 means it is a mine
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0: #self.val corresponds to the number of mines in proximity
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag: #a right click has been done (flagged), i.e. self.flag = True
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True #A left click is done and it sets self.clicked as True. It will later be used in the function drawGrid(self)
        # Auto reveal if it's a 0
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < game_width: #Check whether the cases left and right of the one clicked belonged to the grid
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height: #Check whether the cases up and down of the one clicked belonged to the grid
                            if not grid[self.yGrid + y][self.xGrid + x].clicked: #If the adjacent case has not already been clicked
                                grid[self.yGrid + y][self.xGrid + x].revealGrid() #Restart the revealGrid() function as if the case had been clicked itself and that for all adjacent case. It is useful to "unlock" a large number of cases when there is no mine nearby
        elif self.val == -1:
            # Auto reveal all mines if it's a mine which is clicked
            for m in mines:
                if not grid[m[1]][m[0]].clicked: #it check all the other mines (i.e. the mines not clicked)
                    grid[m[1]][m[0]].revealGrid() #and reveals them

    def updateValue(self):
        # Update the value when all grid is generated
        if self.val != -1: #i.e. it is not a mine
            for x in range(-1, 2): #check the adjacent cases
                if self.xGrid + x >= 0 and self.xGrid + x < game_width:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < game_height:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1 #if there is a mine around the case increase the value by 1. After the loop is finished we thus have the correct number of mines around the case under self.val


def gameLoopMinesweeper():
    gameState = "Playing"  # Game state
    mineLeft = numMine  # Number of mine left
    global grid  # Access global var
    grid = []
    global mines
    t = 0  # Set time to 0

    # Generating mines randomly in the game space
    mines = [[random.randrange(0, game_width),
              random.randrange(0, game_height)]]#A first mine is created manually as it is the first there is no risk of superposition

    for c in range(numMine - 1):#numMine-1 because one was already used
        pos = [random.randrange(0, game_width),
               random.randrange(0, game_height)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:#check if the new mine position is the same as one already set
                    pos = [random.randrange(0, game_width), random.randrange(0, game_height)] #if it is the case it regenerates a new mine position
                    break
                if i == len(mines) - 1:#if all the position have been check we stop the (while) loop and add the new mine to the list
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(game_height):
        line = []
        for i in range(game_width):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))#if there is a mine at this position notes it as -1
            else:
                line.append(Grid(i, j, 0))#if there is no mine notes it as 0
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()#Use the above defined function to create the case 1,2,3,4,...

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:#a keyboard key is presses
                    if event.key == pygame.K_r:#and it is a "r"
                        gameState = "Exit"#finishes the game
                        gameLoopMinesweeper()#and starts it over
            else:
                if event.type == pygame.MOUSEBUTTONUP:#either left or right click
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    j.revealGrid()
                                    # Toggle flag off
                                    if j.flag:
                                        mineLeft += 1
                                        j.flag = False
                                    # If it's a mine
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.clicked:
                                        if j.flag: #i.e. if there was already a flag
                                            j.flag = False
                                            mineLeft += 1
                                        else: 
                                            j.flag = True 
                                            mineLeft -= 1

        # Check if won
        w = True
        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked: #i.e. it is not a mine and it as not been clicked
                    w = False
        if w and gameState != "Exit": #if w is True it means that all non mine cases have been discovered which is the condition for winning
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            t += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50)
            drawText("R to restart", 35, 50)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1: #all the false flag are discovered
                        j.mineFalse = True
        else:
            drawText("You WON!", 50)
            drawText("R to restart", 35, 50)
        # Draw time
        s = str(t // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        screen_text = pygame.font.SysFont("Calibri", 50).render(level.__str__(), True, (0, 0, 0))
        screen_text_rect = screen_text.get_rect(center=(display_width/2, 2*border))
        gameDisplay.blit(screen_text, screen_text_rect)
        
        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps


gameLoopMinesweeper()
pygame.quit()
quit()


# In[ ]:




