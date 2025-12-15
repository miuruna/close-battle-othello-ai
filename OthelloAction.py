import random
import OthelloLogic
from utils.ai_state_manager import AiStateManager
from utils.game_logger import GameLogger

# ロガーをグローバル変数として保持（プログラム実行中ずっと維持するため）
_logger = None
_my_color = None
_opp_color = None
_ai_memory = None

def getAction(board:list, moves):
    global _logger
    global _my_color
    global _opp_color
    global _ai_memory

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

    # ひとつ前の盤面を取得
    prev_board = _ai_memory.game_info.board

    if stone_count != 4:
        # 相手の打った手を取得
        opp_move = get_opp_action(prev_board, board)
        _logger.save(stone_count - 4, _opp_color, "MOVED", board, opp_move, _ai_memory.opponent_model)

    _logger.save(stone_count - 3, _my_color, "THINKING", board, None, _ai_memory.opponent_model)

    # 自分の手を決定する
    next_move = random.choice(moves)

    # 盤面を取得
    next_board = OthelloLogic.execute(board, next_move, 1, len(board))

    _logger.save(stone_count - 3, _my_color, "MOVED", next_board, next_move, _ai_memory.opponent_model)
    
    _ai_memory.game_info.board = next_board
    _ai_memory.game_info.turn_count = stone_count - 3
    _ai_memory.save_json()

    return next_move

def stone_counter(board:list):
	count = 0
	for row in board:
		for cell in row:
			if cell != 0:
				count += 1
	return count

def is_new(board):
	return not (stone_counter(board) > 5)

def get_opp_action(prev_board, board):
    if stone_counter(board) - stone_counter(prev_board) != 1:
        opp_move = None
    else:
        for r in range(len(board)):
            for c in range(len(board[r])):
                if prev_board[r][c] == 0 and board[r][c] != 0:
                    opp_move = [r, c]
                    break
    return opp_move