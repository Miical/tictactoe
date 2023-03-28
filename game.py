from tictactoe import *
import random

INF = 10            # 游戏价值的极大值
PLAYER_FIRST = True # 玩家是否先手

def another(player):
    """返回 "Max" 和 "Min" 中另外一个角色"""

    return "Min" if player == "Max" else "Max"

def minimax_search(player):
    """极大极小搜索
    player 为当前角色 "Max" 或 "Min",
    返回最优价值和对应的位置。
    """

    if game_is_over():
        return (final_value(), None)

    if player == "Max":
        best_val, best_pos = -INF, None
        for pos in available_positions():
            place_chess_at(pos)
            sub_val, _ = minimax_search(another(player))
            if sub_val > best_val:
                best_val, best_pos = sub_val, pos
            undo_chess()
        return (best_val, best_pos)

    elif player == "Min":
        best_val, best_pos = INF, None
        for pos in available_positions():
            place_chess_at(pos)
            sub_val, _ = minimax_search(another(player))
            if sub_val < best_val:
                best_val, best_pos = sub_val, pos
            undo_chess()
        return (best_val, best_pos)

def computer_drop():
    """电脑落子决策函数。"""

    # pos = available_positions()[0]
    # pos = random.choice(available_positions())
    _, pos = minimax_search("Min" if PLAYER_FIRST else "Max")

    return pos

game_init()
game_main_loop(computer_drop, PLAYER_FIRST)