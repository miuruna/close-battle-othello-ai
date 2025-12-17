import OthelloLogic
from utils import bayes_even, data_loader
from utils.ai_state_manager import AiStateManager
from utils.bayes_player import BayesPlayer
from utils.game_logger import GameLogger
from utils.Evaluator import Evaluator
import copy

# ロガーをグローバル変数として保持（プログラム実行中ずっと維持するため）
_logger = None
_my_color = None
_opp_color = None
_ai_memory = None
_bayes_player = None
_evaluator = None

def getAction(board:list[list[int]], moves:list[list[int]]):
    """
    次に打つ手を取得する関数
    
    :param board: 現在の盤面
    :type board: list[list[int]]
    :param moves: 現在の盤面における合法手のリスト
    :type moves: list[list[int]]
    """
    
    global _logger
    global _my_color
    global _opp_color
    global _ai_memory
    global _bayes_player
    global _evaluator

    stone_count = stone_counter(board)

    # 初回のみ実施される
    if _logger is None:
        _logger = GameLogger()
        if is_new(board):
            _logger.finalize_previous_log()
            _logger.create_new_log()
            if stone_count == 4:
                _my_color, _opp_color = "black", "white"
            else:
                _my_color, _opp_color = "white", "black"
            _logger.initial_save(board, _my_color)
        else:
            file_path = data_loader.get_latest_modified_file_path("data/")
            _logger.resume_log(file_path)

    # 初回のみ実施される
    if _ai_memory is None:
        _ai_memory = AiStateManager()
        if is_new(board):
            if _my_color is None:
                _my_color = "black" if stone_count % 2 == 0 else "white"
            _ai_memory.new_game(board, _my_color)
        else:
            _ai_memory.continue_game()
            _my_color = _ai_memory.game_info.my_color
            if _my_color == "black":
                _opp_color  = "white"
            else:
                _opp_color = "black"

    # 初回のみ実施される
    if _bayes_player is None:
        _bayes_player = BayesPlayer()

    if _evaluator is None:
        _evaluator = Evaluator()

    # ひとつ前の盤面を取得
    prev_board:list[list[int]] | None = _ai_memory.game_info.board
    print("ひとつ前の盤面")
    print(prev_board)

    opp_move = None

    if stone_count != 4 and prev_board is not None:
        # 相手の打った手を取得
        opp_move = get_opp_action(prev_board, board)

    print("相手が打った手")
    print(opp_move)
    if opp_move is None:
        print("相手の手を取得できませんでした")

    if opp_move is not None and prev_board is not None:
        # 相手のモデルを更新
        _ai_memory.opponent_model = _bayes_player.update_opponent_model(copy.deepcopy(prev_board), opp_move, _ai_memory.opponent_model, _evaluator.evaluate)

    # 更新されたモデル
    print(_ai_memory.opponent_model)

    # CSVに相手の手を書き込む
    _logger.save(stone_count - 4, _opp_color, "MOVED", board, opp_move, _ai_memory.opponent_model)

    # CSVに思考開始を記録する
    _logger.save(stone_count - 3, _my_color, "THINKING", board, None, _ai_memory.opponent_model)

    # -----自分の手を決定する-----
    next_move = bayes_even.bayes_even(copy.deepcopy(board), moves, stone_count - 3, _ai_memory.opponent_model, _bayes_player, _evaluator.evaluate)
    # ---------------------------

    # 盤面を取得
    next_board = OthelloLogic.execute(board, next_move, 1, len(board))

    # 自分の手をCSVに保存する
    _logger.save(stone_count - 3, _my_color, "MOVED", next_board, next_move, _ai_memory.opponent_model)
    
    # JSONにバックアップをとる
    _ai_memory.game_info.board = copy.deepcopy(next_board)
    _ai_memory.game_info.turn_count = stone_count - 3
    _ai_memory.save_json()

    return next_move

def stone_counter(board:list[list[int]]):
    """
    盤上にある石の数を数える
    
    :param board: 盤面
    :type board: list[list[int]]
    """
    count = 0
    for row in board:
        for cell in row:
            if cell != 0:
                count += 1
    return count

def is_new(board):
	return not (stone_counter(board) > 5)

def get_opp_action(prev_board:list[list[int]], board:list[list[int]]):
    """
    前の盤面と現在の盤面の差分から相手の打った手を取得する
    
    :param prev_board: 前の盤面
    :type prev_board: list[list[int]]
    :param board: 現在の盤面
    :type board: list[list[int]]
    """
    if stone_counter(board) - stone_counter(prev_board) != 1:
        opp_move = None
    else:
        for r in range(len(board)):
            for c in range(len(board[r])):
                if prev_board[r][c] == 0 and board[r][c] != 0:
                    opp_move = [r, c]
                    break
    return opp_move
