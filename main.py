from game import Game

g = Game() #create a game named g based on class we defined in game.py

while g.running:#True by definition of the game
    g.curr_menu.display_menu()#displaying menu => self.playing can be set to true in menu which would then activate the core game loop of minesweeper
    g.game_start()
