#自分の手の評価値、均衡になるように,ある定数に近づけたい
#自分の手が多い→正の値
#相手の手が多い→負の値
#1 = 自分の手
#-1 = 相手の手
#0 = 空マス
#次の一手を選ぶ考え方
#打てる手をすべて列挙、その手を打った「仮の盤面」を作る
#評価値を計算、目標評価値に一番近い手を選ぶ

import OthelloAction
import OthelloLogic
import math
from utils import bayes_player
import copy

TARGET_MID = 100      # 中盤：接戦を作る目標評価値
TARGET_END = 1000     # 終盤：勝利を目指す目標評価値
ENDGAME_TURN = 36    # 終盤とみなすターン数
MAX_DEPTH = 3        # 探索の深さ



def simulate_move(board, move, player):
    new_board = [row[:] for row in board]
    x, y = move

    new_board[x][y] = player
    # 本当はここで挟んだ石を反転する処理を書く

    return new_board

def bayes_even(board, moves, turn, opponent_model, bayes_player, evaluate_func):
    best_diff = math.inf
    best_move = None

    for move in moves:
        tmp_board = copy.deepcopy(board)
        next_board = OthelloLogic.execute(tmp_board, move, 1, len(board))
        predict_score = search (next_board, MAX_DEPTH, False, turn + 1, opponent_model, bayes_player, evaluate_func)
        
        if turn >= ENDGAME_TURN:
            target = TARGET_END
        else:
            target = TARGET_MID
        
        diff = abs(predict_score - target)

        if diff < best_diff:
            best_diff = diff
            best_move = move

    return best_move

def search(board, depth, is_my_turn: bool, turn, opponent_model, bayes_player, evaluate_func):
    
    
    player = 1 if is_my_turn else -1
    
    
    size = len(board)
    moves = OthelloLogic.getMoves(board, player, size)

    if depth == 0 or OthelloAction.stone_counter(board) > 63:
        target_color = 1
        mobility = len(moves) if is_my_turn else -len(moves)
        return evaluate_func(board, target_color, mobility)
    
    if len(moves) == 0:
        return search(board, depth-1, not is_my_turn, turn+1, opponent_model, bayes_player, evaluate_func)
    
    if is_my_turn:
        # 自分のターン
        if turn >= 50:
            target = 1000
        else:
            target = 100

        #接戦にしたい評価値
        #評価値が0~100の時

        best_diff = float("inf")
        best_score = None

        
        for move in moves:
            tmp_board = copy.deepcopy(board)
            new_board = OthelloLogic.execute(tmp_board, move, player, len(board))
            score = search(new_board, depth-1, False, turn + 1, opponent_model, bayes_player, evaluate_func)
            diff = abs(score - target) # type: ignore

            if diff < best_diff:
                best_diff = diff
                best_score = score

        return best_score

    else:
        # 相手のターン
        probabilities = bayes_player.get_moves_predict(moves, board, opponent_model, evaluate_func)
        expected_score = 0
        for i in range(len(moves)):
            move = moves[i]
            if probabilities[i] <= 0:
                continue
            tmp_board = copy.deepcopy(board)
            next_board = OthelloLogic.execute(tmp_board, move, player, len(board))
            score = search(next_board, depth-1, True, turn + 1, opponent_model, bayes_player, evaluate_func)

            expected_score += probabilities[i] * score
        return expected_score
