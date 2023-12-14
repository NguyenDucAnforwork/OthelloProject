from othello import *
from Token import *
from computer_player import *
from grid import *
from utility_functions import *

if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()