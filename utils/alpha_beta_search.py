import copy
import math
import OthelloAction
import OthelloLogic


def alpha_beta_search(board, depth, alpha, beta, is_maximizing, target_color, evaluate_func):
    # 手番の決定
    # 最大化プレイヤーであれば現在のターンは評価対象の色
    current_player = target_color if is_maximizing else target_color * -1

    # 合法手の生成
    moves = OthelloLogic.getMoves(board, current_player, len(board))

    # 終了条件
    if depth == 0 or OthelloAction.stone_counter(board) > 63:
        mobility = len(moves) if current_player == target_color else -len(moves)
        return evaluate_func(board, target_color, mobility)
    
    # pass の場合
    if len(moves) == 0:
        return alpha_beta_search(board, depth - 1, alpha, beta, not is_maximizing, target_color, evaluate_func)
    
    # 最大化
    if is_maximizing:
        max_evaluation_value = - math.inf

        for move in moves:
            tmp_board = copy.deepcopy(board)
            next_board = OthelloLogic.execute(tmp_board, move, current_player, len(tmp_board))
            evaluation_value = alpha_beta_search(copy.deepcopy(next_board), depth-1, alpha, beta, False, target_color, evaluate_func)
            
            if evaluation_value > max_evaluation_value: # type: ignore
                max_evaluation_value = evaluation_value
                alpha = max(alpha, evaluation_value) # type: ignore

            if beta <= alpha:
                break
        
        return max_evaluation_value
    # 最小化
    else:
        min_evaluation_value = math.inf

        for move in moves:
            tmp_board = copy.deepcopy(board)
            next_board = OthelloLogic.execute(tmp_board, move, current_player, len(tmp_board))

            evaluation_value = alpha_beta_search(copy.deepcopy(next_board), depth - 1, alpha, beta, True, target_color, evaluate_func)

            if evaluation_value < min_evaluation_value: # type: ignore
                min_evaluation_value = evaluation_value
                beta = min(beta, evaluation_value) # type: ignore
            
            if beta <= alpha:
                break
        
        return min_evaluation_value





