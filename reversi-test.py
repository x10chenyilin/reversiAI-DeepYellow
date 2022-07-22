#!/usr/bin/env python3

# DO NOT MODIFY THE CODE BELOW
import sys, os
from turtle import goto
from typing import List, Tuple

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["USE_SIMPLE_THREADED_LEVEL3"] = "1"
# DO NOT MODIFY THE CODE ABOVE

# add your own imports below
# import numpy as np
from random import randint

# define your helper functions here

def coord_to_index(x, y):
    '''
    将坐标 (x,y) 点转换为数组下标
    '''
    assert x >= 0 and x < 8 and y >= 0 and y < 8
    return (x << 3) + y

def index_to_coord(i: int) -> Tuple[int, int]:
    '''
    将数组下标转换为坐标
    '''
    assert i >= 0 and i < 64
    return i >> 3, i & 7

def count_my_piece(player: int, board: List[int]) -> int:
    '''
    统计棋盘上属于当前玩家的子的数量
    参数：player: 当前玩家编号（0 或者 1）
        board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
    返回值：属于player的棋子数
    '''
    count = 0
    for i in board:
        if i == player:
            count += 1
        else:
            pass
    return count

def is_end_of_game(board):
    if (not True in ask_next_pos(board, 0)) and (not True in ask_next_pos(board, 1)):
        return True
    else:
        return False

def flip(player: int, board: List[int], vertex: Tuple[int, int], direction: str) -> List[int]:
    '''
    翻转vertex所夹的子
    参数：player: 当前玩家编号（0 或者 1）
        board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
        vertex：两个属于player的棋子位置（0~63的整数）
        direction：方向，vertex所夹的方向，为gap中的key
    返回值：翻转后的棋盘
    '''
    gap = {"lu": -9, "ru": -7, "ld": 7, "rd": 9, "l": -1, "r": 1, "u": -8, "d": 8}

    now_fliping = vertex[0] + gap[direction]
    while now_fliping != vertex[1]:
        board[now_fliping] = player
        now_fliping += gap[direction]

    return board

def check_act_legality(player: int, board: List[int], pos: int) -> bool:
    '''
    模拟一次落子
    参数：player: 当前玩家编号（0 或者 1）
        board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
        pos：落子位置，0~63的整数
    返回值：落子后的棋盘
    '''
    opponent = 1 if player == 0 else 0
    # search in 8 directions for fliping pieces
    # 4 inclined directions
    gap_inclined = {"lu": -9, "ru": -7, "ld": 7, "rd": 9}
    condition_para_inclined = {"lu": 7, "ru": 0, "ld": 7, "rd": 0}
    for direction in gap_inclined:
        aim = pos + gap_inclined[direction]
        if aim >= 0 and aim < 64 and aim & 7 != condition_para_inclined[direction]:
            if board[aim] != opponent:
                continue
        else:
            continue
        aim += gap_inclined[direction]
        while aim >= 0 and aim < 64 and aim & 7 != condition_para_inclined[direction]:
            if board[aim] == player:
                return True
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_inclined[direction]
    # 2 vertical directons
    gap_vertical = {"l": -1, "r": 1}
    for direction in gap_vertical:
        aim = pos + gap_vertical[direction]
        if aim >= 0 and aim < 64 and aim >> 3 == pos >> 3:
            if board[aim] != opponent:
                continue
        else:
            continue
        aim += gap_vertical[direction]
        while aim >= 0 and aim < 64 and aim >> 3 == pos >> 3:
            if board[aim] == player:
                return True
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_vertical[direction]
    # 2 horizontal directions
    gap_horizontal = {"u": -8, "d": 8}
    for direction in gap_horizontal:
        aim = pos + gap_horizontal[direction]
        if aim >= 0 and aim < 64:
            if board[aim] != opponent:
                continue
        else:
            continue
        aim += gap_horizontal[direction]
        while aim >= 0 and aim < 64:
            if board[aim] == player:
                return True
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_horizontal[direction]
    return False

def simulate_action(player: int, ori_board: List[int], pos: int) -> List[int]:
    '''
    模拟一次落子
    参数：player: 当前玩家编号（0 或者 1）
        board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
        pos：落子位置，0~63的整数
    返回值：落子后的棋盘
    '''
    if not ori_board[pos] == 2:
        exit(1)
    opponent = 1 if player == 0 else 0
    board = ori_board.copy()
    board[pos] = player
    # search in 8 directions for fliping pieces
    # 4 inclined directions
    gap_inclined = {"lu": -9, "ru": -7, "ld": 7, "rd": 9}
    condition_para_inclined = {"lu": 7, "ru": 0, "ld": 7, "rd": 0}
    for direction in gap_inclined:
        aim = pos + gap_inclined[direction]
        while aim >= 0 and aim < 64 and aim & 7 != condition_para_inclined[direction]:
            if board[aim] == player:
                flip(player, board, (pos, aim), direction)
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_inclined[direction]
    # 2 vertical directons
    gap_vertical = {"l": -1, "r": 1}
    for direction in gap_vertical:
        aim = pos + gap_vertical[direction]
        while aim >= 0 and aim < 64 and aim >> 3 == pos >> 3:
            if board[aim] == player:
                flip(player, board, (pos, aim), direction)
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_vertical[direction]
    # 2 horizontal directions
    gap_horizontal = {"u": -8, "d": 8}
    for direction in gap_horizontal:
        aim = pos + gap_horizontal[direction]
        while aim >= 0 and aim < 64:
            if board[aim] == player:
                flip(player, board, (pos, aim), direction)
            elif board[aim] == opponent:
                pass
            else:
                break
            aim += gap_horizontal[direction]

    return board

def ask_next_pos(board, player):
    '''
    可能比API更快的返回合法落子点的函数
    参数：player: 当前玩家编号（0 或者 1）
         board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
    返回值：玩家可落子的位置（bool格式）
    '''
    next_pos = []
    for i in range(0, 64):
        if not board[i] == 2: # 如果位置非空，肯定不合法
            pass
        else: # 如果位置空
            if check_act_legality(player, board, i): # 再严格地检查该位置
                next_pos.append(i) # 合法即插入
    return [i in next_pos for i in range(0, 64)]

def assess_situation(player: int, board: List[int], allow_player, allow_opponent) -> int:
    '''
    局面评估函数
    参数：player: 当前玩家编号（0 或者 1）
         board:  当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
         allow_player, allow_opponent: 允许落子的位置（bool格式）
    返回值：对当前局面的评估值，是一个整数
    '''
    # 对于局面的评估原则，可以参见reversi-tutorial.md

    opponent = 1 if player == 0 else 0
    total_piece = len([p for p in board if not p == 2]) # 棋盘上总的棋子数，用来评估棋局进行的阶段
    allow_p_player = [p for p in range(0, 64) if allow_player[p]]
    allow_p_opponent = [p for p in range(0, 64) if allow_opponent[p]]

    value = 0

    # 参数重要性指标，是这个AI的主要参数。
    SWEET16_INDEX= 1 # 开局指标
    EDGE_INDEX = 10 # 边界指标
    MOBILITY_PLAYER_INDEX, MOBILITY_OPPONENT_INDEX = 10, -79 # 行动力指标
    C_X_FORCED_INDEX = 358 # C位压迫指标，星位压迫指标
    C_PLAYER_INDEX, C_OPPONENT_INDEX = -68, 104 # C位指标
    X_PLAYER_INDEX, X_OPPONENT_INDEX = -83, 130 # 星位指标
    CORNER_PLAYER_INDEX, CORNER_OPPONENT_INDEX = 600, -821 # 角指标
    BEGINNING_OF_END, PIECE_INDEX = 57, 24 # 终局指标

    # 开局
    beginning = True
    around_sweet16 = board[9:15] + board[9:57:8] + board[14:62:8] + board[49:55]
    for p in around_sweet16:
        if not p == 2:
            beginning = False
            break
    
    if beginning:
        sweet16 = board[18:22] + board[26:30] + board[34:38] + board[42:46]
        for p in sweet16:
            if p == player:
                value += SWEET16_INDEX
            else:
                pass
    else:
        # 占据边
        edge = board[1:7] + board[8:56:8] + board[15:63:8] + board[57:63]
        for p in edge:
            if p == player:
                value += EDGE_INDEX
            elif p == opponent:
                value -= EDGE_INDEX
            else:
                pass

        # 争夺角的归属：尽量不占据C位和X位，将对手逼到C位、X位和角
        hasCorner = False
        corner = [board[0], board[7], board[56], board[63]]
        C_square, X_square = [], []
        C_X_square_coord = []
        if board[0] == 2:
            C_square += [board[1], board[8]]
            X_square += [board[9]]
            C_X_square_coord += [1, 8, 9]
        if board[7] == 2:
            C_square += [board[6], board[15]]
            X_square += [board[14]]
            C_X_square_coord += [4, 14, 15]
        if board[56] == 2:
            C_square += [board[48], board[57]]
            X_square += [board[49]]
            C_X_square_coord += [48, 49, 57]
        if board[63] == 2:
            C_square += [board[55], board[62]]
            X_square += [board[54]]
            C_X_square_coord += [54, 55, 62]

        for p in corner:
            if p == player:
                hasCorner = True
                value += CORNER_PLAYER_INDEX
            elif p == opponent:
                value += CORNER_OPPONENT_INDEX
            else:
                pass
        for p in C_square:
            if p == player:
                value += C_PLAYER_INDEX
            elif p == opponent:
                value += C_OPPONENT_INDEX
            else:
                pass
        for p in X_square:
            if p == player:
                value += X_PLAYER_INDEX
            elif p == opponent:
                value += X_OPPONENT_INDEX
            else:
                pass

        # 降低对手行动力
        mobility_player = len(allow_p_player)
        mobility_opponent = len(allow_p_opponent)
        value += MOBILITY_PLAYER_INDEX * mobility_player + MOBILITY_OPPONENT_INDEX * mobility_opponent
        # 特别地，如果压迫成功，有额外奖励
        if mobility_player < 2 and [p for p in allow_p_player if p in C_X_square_coord] != []:
            value -= C_X_FORCED_INDEX
        if mobility_opponent < 2 and [p for p in allow_p_opponent if p in C_X_square_coord] != []:
            value += C_X_FORCED_INDEX

        # 终局，尽可能多地占据子
        if hasCorner and total_piece > BEGINNING_OF_END:
            for p in board:
                if p == player:
                    value += PIECE_INDEX
                elif p == opponent:
                    value -= PIECE_INDEX
                else:
                    pass

    return value

def minimax_search(player: int, depth: int, max_depth: int,
                     board: List[int], alpha: int, beta: int) -> Tuple[int, int]:
    '''
    极大极小树搜索函数
    参数：player: 调用玩家编号（0 或者 1）
         depth: 调用深度
         max_depth: 最大调用深度
         board: 当前棋盘，长度为 64，0 表示 player0 的子, 1 表示 player1 的子, 2 表示没有落子
         alpha, beta: α-β剪枝算法的参数，初次调用时置为-inf和inf
    返回值：(选择值，选择落子地点)
    '''
    opponent = 1 if player == 0 else 0

    allow_player = ask_next_pos(board, player)
    allow_opponent = ask_next_pos(board, opponent)
    # 此处参考了wiki的伪代码：https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    if depth > max_depth or ((not True in allow_player) and (not True in allow_opponent)):
        return (assess_situation(player, board, allow_player, allow_opponent), 0)

    if depth % 2 == 0:
        value = -1145141919810 # -inf
        if not True in allow_player:
            return (assess_situation(player, board, allow_player, allow_opponent), 0)
        # for each feasible positions
        for p in [i for i in range(0, 64) if allow_player[i]]:
            new_board = simulate_action(player, board, p)
            n_value = minimax_search(player, depth + 1, max_depth, new_board, alpha, beta)[0]
            if value < n_value:
                value = n_value
                choice = p
            else:
                pass
            alpha = max(alpha, value)
            if value >= beta:
                break
            else:
                pass
        return (value, choice)
    else:
        value = 1145141919810 # +inf
        if not True in allow_opponent:
            return (assess_situation(player, board, allow_player, allow_opponent), 0)
        # for each feasible positions
        for p in [i for i in range(0, 64) if allow_opponent[i]]:
            new_board = simulate_action(opponent, board, p)
            n_value = minimax_search(player, depth + 1, max_depth, new_board, alpha, beta)[0]
            if value > n_value:
                value = n_value
                choice = p
            beta = min(beta, value)
            if value <= alpha:
                break
            else:
                pass
        return (value, choice)

def output(board: List[int], isdebug, depth=0):
    if isdebug:
        for i in range(0, 8):
            for j in range(0, depth):
                print("   ", end="")
            print(f"    {board[8 * i : 8 * (i + 1)]}")
    else:
        for i in range(0, 8):
            for j in range(0, 8):
                if board[i * 8 + j] == 0:
                    print("● ", end="")
                elif board[i * 8 + j] == 1:
                    print("o ", end="")
                else:
                    print(". ", end="")
            print(" ")
        print(" ")

if __name__ == '__main__':

    # board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    # output(board, False)
    # now_acting = 0


    # best_para = (1, 10, 10, -30, 400, -75, 100, -100, 125, 600, -800, 50, 50)
    # new_para = (1, best_para[1] + randint(-10, 10), best_para[2] + randint(-10, 10)
    #             , best_para[3] + randint(-10, 10), best_para[4] + randint(-10, 10), best_para[5] + randint(-10, 10)
    #             , best_para[6] + randint(-10, 10), best_para[7] + randint(-10, 10), best_para[8] + randint(-10, 10)
    #             , 600, best_para[10] + randint(-10, 10), randint(48, 63), best_para[12] + randint(-10, 10))
    
    # ROUND = 10000
    # count = ROUND
    # win_count, best_win_count = 0, 0
    # best_best_para = best_para
    # with open(f"TEST_ROUND{ROUND}.txt", 'w', encoding='utf-8') as output_file:
    #     output_file.write("BEGIN\n")
    #     while count > 0:
    #         print(count)
    #         output_file.write(f"ROUND-{str(ROUND - count).zfill(4)}: best_para = {best_para}\n")
    #         output_file.write(f"            new_para = {new_para}.\n")
    #         best_para_win_count = 0

    #         board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    #         now_acting = 0 # best_para first
    #         while not is_end_of_game(board):
    #             now_acting = 1 if now_acting == 0 else 0
    #             if now_acting == 1:
    #                 p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, best_para)[1]
    #             else:
    #                 p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, new_para)[1]
    #             board = simulate_action(now_acting, board, p)
    #         if count_my_piece(1, board) > count_my_piece(0, board):
    #             best_para_win_count += 1

    #         board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    #         now_acting = 1 # new_para first
    #         while not is_end_of_game(board):
    #             now_acting = 1 if now_acting == 0 else 0
    #             if now_acting == 1:
    #                 p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, best_para)[1]
    #             else:
    #                 p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, new_para)[1]
    #             board = simulate_action(now_acting, board, p)
    #         if count_my_piece(1, board) > count_my_piece(0, board):
    #             best_para_win_count += 1
            
    #         if best_para_win_count == 0: # best_para lose. Update best_para
    #             output_file.write(f"            new_para wins. best_para keeps {win_count}\n")
    #             if win_count > best_win_count:
    #                 best_best_para = best_para
    #                 best_win_count = win_count
    #                 output_file.write(f"            best_best_para updates!\n")
    #             best_para = new_para
    #             win_count = 0
    #         else:
    #             output_file.write(f"            new_para don't win. best_para wins {best_para_win_count}/2. best_para keeps {win_count}\n")
    #             win_count += 1
            
    #         new_para = (1, best_para[1] + randint(-10, 10), best_para[2] + randint(-10, 10)
    #                 , best_para[3] + randint(-10, 10), best_para[4] + randint(-10, 10), best_para[5] + randint(-10, 10)
    #                 , best_para[6] + randint(-10, 10), best_para[7] + randint(-10, 10), best_para[8] + randint(-10, 10)
    #                 , 600, best_para[10] + randint(-10, 10), randint(48, 63), best_para[12] + randint(-10, 10))
    #         while new_para[10] > 0:
    #             new_para = (1, best_para[1] + randint(-10, 10), best_para[2] + randint(-10, 10)
    #                 , best_para[3] + randint(-10, 10), best_para[4] + randint(-10, 10), best_para[5] + randint(-10, 10)
    #                 , best_para[6] + randint(-10, 10), best_para[7] + randint(-10, 10), best_para[8] + randint(-10, 10)
    #                 , 600, best_para[10] + randint(-10, 10), randint(48, 63), best_para[12] + randint(-10, 10))
            
    #         count -= 1
    #     if win_count > best_win_count:
    #         best_best_para = best_para
    #         output_file.write(f"            best_best_para updates!\n")
    #         best_win_count = win_count
    #     output_file.write("END\n")
    #     output_file.write(f"best_para: {best_para}\n")
    #     output_file.write(f"best_best_para: {best_best_para} with {best_win_count}\n")
    
    # para1 = (1, 10, 10, -30, 400, -75, 100, -100, 125, 600, -800, 50, 50)
    # para2 = (1, 10, 10, -79, 358, -68, 104, -83, 130, 600, -821, 57, 24)
    # while not is_end_of_game(board):
    #     now_acting = 1 if now_acting == 0 else 0
    #     allow_now = ask_next_pos(board, now_acting)
    #     print([p for p in range(0, 64) if allow_now[p]])
    #     if now_acting == 1:
    #         p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, para1)[1]
    #     else:
    #         p = minimax_search(now_acting, 0, 2, board, -1145141919810, 1145141919810, para2)[1]
    #     board = simulate_action(now_acting, board, p)
    #     output(board, False)
    # if count_my_piece(1, board) > count_my_piece(0, board):
    #     win_para1 = 1
    # board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    # now_acting = 1
    # while not is_end_of_game(board):
    #     now_acting = 1 if now_acting == 0 else 0
    #     if now_acting == 1:
    #         p = minimax_search(now_acting, 0, 1, board, -1145141919810, 1145141919810, para1)[1]
    #     else:
    #         p = minimax_search(now_acting, 0, 1, board, -1145141919810, 1145141919810, para2)[1]
    #     board = simulate_action(now_acting, board, p)
    #     output(board, False)
    # if count_my_piece(1, board) > count_my_piece(0, board):
    #     win_para1 = 2
    # print(f"{win_para1}/2")

    board = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    now_acting = 1
    output(board, False)
    while not is_end_of_game(board):
        now_acting = 1 if now_acting == 0 else 0
        if now_acting == 0: # human
            allow_now = ask_next_pos(board, 0)
            print(f"Your(●) turn: {[p for p in range(0, 64) if allow_now[p]]}")
            pos = int(input())
            while True:
                if pos in [p for p in range(0, 64) if allow_now[p]]:
                    board = simulate_action(0, board, pos)
                    break
                else:
                    print("Invalid input. Try again.")
                    pos = int(input())
        else: # AI
            allow_now = ask_next_pos(board, 1)
            v, p = minimax_search(1, 0, 3, board, -1145151919810, 1145141919810)
            print(f"AI decides to act at {p}.")
            if p in [x for x in range(0, 64) if allow_now[x]]:
                board = simulate_action(1, board, p)
            else:
                print("AI ERROR!")
                exit(1)
        output(board, False)
