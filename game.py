from tictactoe import *
import random

INF = 10
PLAYER_FIRST = True

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

def alphabeta(player, alpha, beta):
    """极大极小搜索，带有 alphabeta 剪枝优化。"""

    if game_is_over():
        return (final_value(), None)

    best_pos = None
    for pos in available_positions():
        place_chess_at(pos)
        sub_val, _ = alphabeta(another(player), alpha, beta)
        if player == "Max":
            if sub_val > alpha:
                alpha, best_pos = sub_val, pos
        elif player == "Min":
            if sub_val < beta:
                beta, best_pos = sub_val, pos
        undo_chess()

        if beta <= alpha:
            break

    best_val = alpha if player == "Max" else beta
    return (best_val, best_pos)

def computer_drop():
    # pos = available_positions()[0]
    # pos = random.choice(available_positions())
    # _, pos = minimax_search("Min" if PLAYER_FIRSR else "Max", -INF, INF)
    _, pos = alphabeta("Min" if PLAYER_FIRST else "Max", -INF, INF)

    return pos

game_init()
game_main_loop(computer_drop, PLAYER_FIRST)
