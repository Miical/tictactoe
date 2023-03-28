from tictactoe import *
import random

def computer_drop():
    """电脑落子决策函数。"""

    # pos = available_positions()[0]
    pos = random.choice(available_positions())

    return pos

game_init()
game_main_loop(computer_drop)
