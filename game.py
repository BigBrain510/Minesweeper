import pygame
from menu import *


class Game(): #This is the program which coordinates the two program menu.py and minesweeper.py by puting them in relation (it takes the outputs from menu.py and runs the minesweeper when it is correct output). It also makes the menu visible to the user.
    def __init__(self): #Creating the game object 
        pygame.init()#gives us access to features of pygame
        self.running, self.playing = True, False # the loop self.running will be true when the game is running (used in main.py) and self.playing when the player is actually playing the game 
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False #fundamental idea of controls: If any of the buttons pushed => From False to True
        self.DISPLAY_W, self.DISPLAY_H = 480, 270 #Canvas Size - Rectangle
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H)) #Creating the actual Canvas of Main Menu
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H))) #Make the canvas visible to the user
        self.font_name = '8-BIT WONDER.TTF' #using font file
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255) #Remember RGB (Red, Blue, Green)
        self.main_menu = MainMenu(self)#the game is going to pass itself into the main menu class
        self.difficulty = DifficultyMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_start(self): 
        if self.playing: #Launch minesweeper.py if we have clicked on "Start game" in the menu.
            import minesweeper #import seperate game file minesweeper
            minesweeper.my_func()
            execfile('minesweeper.py') #execute the seperate game file

    def check_events(self): #this function checks for player input
        for event in pygame.event.get(): #Goes through list of potential player actions
            if event.type == pygame.QUIT: #Player wants to close the window
                self.running, self.playing = False, False #Stop the gameloop of the game in main.py
                self.curr_menu.run_display = False #Will stop whatever menu is being run from running
            if event.type == pygame.KEYDOWN: #Checking if player presses any preselected keys
                if event.key == pygame.K_RETURN: #If we press the Return key (Enter) sets the value of self.START_KEY as True
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:#Same but for Delete
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:#Same but for the Down arrow
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:#Same but for the Up arrow
                    self.UP_KEY = True

    def reset_keys(self): #In order to reset the values of player input
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ): #We create a function to drw text that we will use in menu.py. Self is reference so that we can have access to variables listed above
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE) #Actually Drawing text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)#Assigns x and y position to center of rectangle
        self.display.blit(text_surface,text_rect) #Text on Canvas





