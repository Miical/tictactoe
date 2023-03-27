from tictactoe import *
import random

INF = 10

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
    _, pos = minimax_search("Min")
    return pos

game_init()
game_main_loop(computer_drop, True)
