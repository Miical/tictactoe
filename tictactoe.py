"""井字棋游戏"""
import pygame

######################
#   游戏参数/状态表示   #
######################

GAME_SIZE = 450   # 游戏窗口大小
GRID_SIZE = 150   # 网格大小
ROWS, COLS = 3, 3 # 游戏行列数

class Piece:
    """有两种棋子 "X" 和 "O"。"""
    X = 1
    O = 2

class Cell:
    """有三种棋盘格子状态，格子为空或放置了 "X", "O" 类型的棋子之一。 """
    Empty = 0
    X = Piece.X
    O = Piece.O

board = None         # 棋盘状态
current_piece = None # 当前棋子

##############
#  单元格操作  #
##############

def position(row, col):
    """获取 row 行, col 列的位置表示。 """

    assert(0 <= row < ROWS and 0 <= col < COLS)
    return [row, col]

def cell_at(pos):
    """获取 pos 位置的单元格。"""

    assert(board != None)
    return board[pos[0]][pos[1]]

def cell_at_pos(row, col):
    """获取 row 行, col 列的单元格。"""

    return cell_at(position(row, col))

def set_cell_at(pos, state):
    """将 pos 位置处的单元格设置为 state。"""

    assert(board != None)
    assert(state == Cell.Empty or state == Cell.X or state == Cell.O)
    board[pos[0]][pos[1]] = state

#############
#  游戏操作  #
#############

def game_init():
    """设置游戏初始状态，初始化游戏界面。"""

    global board, current_piece

    board = [[Cell.Empty for i in range(COLS)] for j in range(ROWS)]
    current_piece = Piece.X
    gui_init()

def place_chess_at(pos):
    """在 pos 处落子，落子类型由当前棋子 current_piece 指定。"""

    global current_piece
    assert(cell_at(pos) == Cell.Empty)
    assert(current_piece != None)

    set_cell_at(pos, current_piece)
    current_piece = Piece.X if current_piece == Piece.O else Piece.O

def available_positions():
    """获取可用位置，返回一个包含所有空单元格位置的列表。"""

    positions = []
    for row in range(ROWS):
        for col in range(COLS):
            if cell_at_pos(row, col) == Cell.Empty:
                positions.append(position(row, col))
    return positions

def winner():
    """获取胜者, 若游戏平局则返回 0, 若游戏未结束则返回 None。"""

    for row in range(ROWS):
        if cell_at_pos(row, 0) != Cell.Empty \
            and cell_at_pos(row, 0) == cell_at_pos(row, 1) == cell_at_pos(row, 2):
            return cell_at_pos(row, 0)

    for col in range(COLS):
        if cell_at_pos(0, col) != Cell.Empty \
            and cell_at_pos(0, col) == cell_at_pos(1, col) == cell_at_pos(2, col):
            return cell_at_pos(0, col)

    if cell_at_pos(0, 0) != Cell.Empty \
        and cell_at_pos(0, 0) == cell_at_pos(1, 1) == cell_at_pos(2, 2):
        return cell_at_pos(0, 0)

    if cell_at_pos(0, 2) != Cell.Empty \
        and cell_at_pos(0, 2) == cell_at_pos(1, 1) == cell_at_pos(2, 0):
        return cell_at_pos(0, 2)

    if available_positions == []:
        return 0

    return None

def final_value():
    """获取游戏的最终价值，若游戏未结束则返回 None。

    价值以 "X" 棋子角度来衡量：
        - 当 "X" 胜利时，价值为 1
        - 当 "O" 胜利时，价值为 -1
        - 当游戏平局时，价值为 0
    """
    win = winner()
    if (win == Piece.X):
        return 1
    elif (win == Piece.O):
        return -1
    elif (win == 0):
        return 0
    else:
        return None

def game_is_over():
    """判断游戏是否结束。若游戏结束则返回 True, 否则返回 False。"""

    return winner() != None

#############
#  GUI 实现  #
#############

screen = None  # 当前游戏绘制屏幕

def gui_init():
    """初始化游戏界面。"""

    global screen

    pygame.init()
    screen = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
    pygame.display.set_caption("Tic Tac Toe")
    display()

def draw_board():
    """绘制棋盘。"""

    assert(screen != None)

    for row in range(1, ROWS):
        pygame.draw.line(screen, (70, 70, 70),
            (row * GRID_SIZE, GAME_SIZE * 0.05),
            (row * GRID_SIZE, GAME_SIZE * 0.95), 8)
    for col in range(1, COLS):
        pygame.draw.line(screen, (70, 70, 70),
            (GAME_SIZE * 0.05, col * GRID_SIZE),
            (GAME_SIZE * 0.95, col * GRID_SIZE), 8)

def draw_piece(row, col, piece):
    """绘制位于 row 行, col 列类型为 piece 的棋子。"""

    assert(screen != None)
    assert(0 <= row < ROWS and 0 <= col < COLS)
    assert(piece == Piece.X or piece == Piece.O)

    x = col * GRID_SIZE + GRID_SIZE // 2
    y = row * GRID_SIZE + GRID_SIZE // 2
    if piece == Piece.X:
        l = GRID_SIZE // 8 * 2
        pygame.draw.line(screen, (70, 70, 70), (x - l, y - l), (x + l, y + l), 14)
        pygame.draw.line(screen, (70, 70, 70), (x + l, y - l), (x - l, y + l), 14)
    else:
        l = GRID_SIZE // 7 * 2
        pygame.draw.circle(screen, (70, 70, 70), (x, y), l, 10)

def draw_all_pieces():
    """绘制所有棋子。"""

    for row in range(ROWS):
        for col in range(COLS):
            if cell_at_pos(row, col) != Cell.Empty:
                draw_piece(row, col, cell_at_pos(row, col))

def display():
    """显示当前游戏状态。"""

    screen.fill((255, 255, 255))
    draw_board()
    draw_all_pieces()
    pygame.display.flip()

def game_main_loop(computer_drop = None, player_first = True):
    """游戏主循环，调用此函数开始游戏。

    computer_drop 指定了人机对战中机器的落子行为，每次调用会返回一个位置 position,
    表示机器在当前状态下的的落子位置。
        - 如果未指定 computer_drop, 则游戏为人人对战模式，轮流检测玩家的落子。
        - 如果指定了 computer_drop, 则游戏为人机对战模式，每次玩家落子后，会调用该函数，
          若 player_first 为 False, 则会在游戏开始时调用该函数。
    """

    if computer_drop != None and player_first == False:
        computer_drop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_is_over():
                x, y = pygame.mouse.get_pos()
                row, col = y // GRID_SIZE, x // GRID_SIZE
                if cell_at_pos(row, col) == Cell.Empty:
                    place_chess_at(position(row, col))
                    if computer_drop != None and not game_is_over():
                        place_chess_at(computer_drop())
                    display()
