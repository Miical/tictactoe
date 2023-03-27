from tictactoe import *
import random

def computer_drop():
    return random.choice(available_positions())

game_init()
game_main_loop(computer_drop, False)
