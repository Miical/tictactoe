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

def print_values_of_available_positions():
    """打印出当前可用位置对应的价值。"""

    if game_is_over():
        print("The game is over.")
        return

    player = "Min" if len(available_positions())&1 else "Max"

    vals = [[None for i in range(COLS)] for j in range(ROWS)]
    for pos in available_positions():
        place_chess_at(pos)
        val, _ = alphabeta(player, -INF, INF)
        vals[pos[0]][pos[1]] = val
        undo_chess()

    print("---------")
    print_board()
    print("---------")
    for vals_line in vals:
        for val in vals_line:
            if (val == None):
                print(".", end="  ")
            elif (val == -1):
                print(val, end=" ")
            else:
                print(val, end="  ")
        print()
    print("---------")

def print_status(pos):
    """打印当前局面状态信息, pos 为电脑将要落子的位置。"""

    print("Computer perspective:")
    print_values_of_available_positions()

    print("Player perspective:")
    place_chess_at(pos)
    print_values_of_available_positions()
    undo_chess()

def computer_drop():
    """电脑落子决策函数。"""

    # pos = available_positions()[0]
    # pos = random.choice(available_positions())
    # _, pos = minimax_search("Min" if PLAYER_FIRSR else "Max")
    _, pos = alphabeta("Min" if PLAYER_FIRST else "Max", -INF, INF)

    print_status(pos)

    return pos

game_init()
game_main_loop(computer_drop, PLAYER_FIRST)
