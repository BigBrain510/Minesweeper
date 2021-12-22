import pygame 


class Menu(): #Menu Base Class - Which we will be able to access through our other classes
    def __init__(self, game): #+Reference to our game object
        self.game = game #Access to all references from game object in other file
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 #define the middle of the interface
        self.run_display = True #Will tell our menu to keep on running
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) #(x, y, width, height) of cursor
        self.offset = - 100 #We want cursor to be to the left and not on top of our main menu options

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)#(asterix, font size, x position, y position). draw_text has been defined in game.py

    def blit_screen(self): #Function makes our lives easier because we won't have to rewrite these three lines of code
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()#Reset keys at the beginning of every frame

class MainMenu(Menu): #Because of (Menu) we have access to the values of the base class menu
    def __init__(self, game):
        Menu.__init__(self, game) #Accessing the def __init__(self, game) from the base class "Menu"
        self.state = "Start" #When we open the menu the cursor is at "Start" (codingwise not visually)
        self.startx, self.starty = self.mid_w, self.mid_h + 30 #Setting position of where the menu option "Start" will be placed in the main menu screen
        self.difficultyx, self.difficultyy = self.mid_w, self.mid_h + 50 #Setting position of where the menu option "Difficulty" will be placed in the main menu screen
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70 #Setting position of where the menu option "Credits" will be placed in the main menu screen
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)#Assigning starting position of cursor (visually)

    def display_menu(self): #function to display main menu
        self.run_display = True #A bit surpurfluous since it's already set to True in base class. Just to be sure.
        while self.run_display:
            self.game.check_events()#in order to ensure logic of cursor
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)#drawing menu items
            self.game.draw_text("Start Game", 20, self.startx, self.starty)#drawing menu items
            self.game.draw_text("Difficulty", 20, self.difficultyx, self.difficultyy)#drawing menu items
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)#drawing menu items
            self.draw_cursor()#drawing cursor
            self.blit_screen()


    def move_cursor(self): #function that enables cursor movement
        #The fundamental logic of cursor movement is that we have to clearly define for each input (up/down) for every item the cursor might be at
        if self.game.DOWN_KEY:#value from game.py
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
                self.state = 'Difficulty'
                #Logic: If the cursor is @start and we press the down key then the cursor goes to the menu item under start - in this case difficulty
            elif self.state == 'Difficulty':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:#value from game.py
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Difficulty':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.difficultyx + self.offset, self.difficultyy)
                self.state = 'Difficulty'

    def check_input(self):
        self.move_cursor()#will check if player wanted to move cursor (i.e. if he clicked on the down or up key) If it is the case the above function will be run normally. However if he did not clicked on the arrows but on "Enter" we have:
        if self.game.START_KEY: #value from game.py
            if self.state == 'Start':
                self.game.playing = True #Set the value as True which will be used in game.py. It means that the game has started.
            elif self.state == 'Difficulty':
                self.game.curr_menu = self.game.difficulty #Open the Difficulty sub-menu
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False #Will quit display menu by stoping the while loop of the function display_menu() if player presses start (in order to charge a new one (defined below)) 

level = "Hard" #We predefined the global variable "level" as equal to Hard (in order to be able to launch the game without going to the difficulty menu
class DifficultyMenu(Menu):#Define the sub-menu once we have a clicked on Difficulty
    def __init__(self, game): #Same reasoning as for the main menu
        Menu.__init__(self, game)
        self.state = 'Easy'
        self.easyx, self.easyy = self.mid_w, self.mid_h + 20 #lets us know where to put the submenu text for the difficulty "easy"
        self.mediumx, self.mediumy = self.mid_w, self.mid_h + 40 #Formerly: control & #lets us know where to put the submenu text for the difficulty "medium"
        self.hardx, self.hardy = self.mid_w, self.mid_h + 60 #lets us know where to put the submenu text for the difficulty "hard"
        self.extremex, self.extremey = self.mid_w, self.mid_h + 80 #lets us know where to put the submenu text for the difficulty "extreme"
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy) #Starting position for cursor - start with easy

    def display_menu(self): #Same reasoning as for the main menu
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input() #check player input
            self.game.display.fill((0, 0, 0))#RGB
            self.game.draw_text('Difficulty', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Easy", 15, self.easyx, self.easyy)
            self.game.draw_text("Medium", 15, self.mediumx, self.mediumy)
            self.game.draw_text("Hard", 15, self.hardx, self.hardy)
            self.game.draw_text("Extreme", 15, self.extremex, self.extremey)
            self.draw_cursor()
            self.blit_screen()#All text and cursor information displayed on screen

    def check_input(self): #Same reasoning as for the main menu however this time we included the "move_cursor" function directly
        global level #importing the variable in the class
        if self.game.BACK_KEY:#goes back to main menu if we click on Back (Delete key)
            self.game.curr_menu = self.game.main_menu #Bringing back to main menu
            self.run_display = False

        if self.game.DOWN_KEY:#Need to display all possible actions (same as before) #value from game.py
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
                #Logic: If the cursor is @start and we press the down key then the cursor goes to the menu item under start - in this case Medium
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.extremex + self.offset, self.extremey)
                self.state = 'Extreme'
            elif self.state == 'Extreme':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
        elif self.game.UP_KEY:#value from game.py
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.extremex + self.offset, self.extremey)
                self.state = 'Extreme'
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
            elif self.state == 'Extreme':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'
            
        elif self.game.START_KEY: #If we press on "Enter" this time it is different as it brings us back to the main menu but also change the value of the variable "level" so that when we run the program minesweeper.py it knows which level to play. #value from game.py
            if self.state == 'Easy':
                level = "Easy"
                self.game.curr_menu = self.game.main_menu #Bringing back to main menu
                self.run_display = False #Stops our sub-menu (by stoping the while loop) in order to recreate the main one
            elif self.state == 'Medium':
                level = "Medium"
                self.game.curr_menu = self.game.main_menu #Bringing back to main menu
                self.run_display = False
            elif self.state == 'Hard':
                level = "Hard"
                self.game.curr_menu = self.game.main_menu #Bringing back to main menu
                self.run_display = False
            elif self.state == 'Extreme':
                level = "Extreme"
                self.game.curr_menu = self.game.main_menu #Bringing back to main menu
                self.run_display = False
                    
class CreditsMenu(Menu):#Same reasonning that the two precedent one but much more easier as we can just see the credits ans leave
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY: #Both options are possible to leave (Enter or Delete)
                self.game.curr_menu = self.game.main_menu
                self.run_display = False #Stops the loop and quits the sub-menu (to go back to the main menu)
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by Alexander and Clement', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()








