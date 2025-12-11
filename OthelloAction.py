import random
import OthelloLogic
from utils.game_logger import GameLogger

# ロガーをグローバル変数として保持（プログラム実行中ずっと維持するため）
_logger = None
_my_color = None
_opp_color = None

def getAction(board, moves):
    global _logger
    global _my_color
    global _opp_color
    
    # 1. ロガーの初期化（初回のみ）
    if _logger is None:
        _logger = GameLogger(board)
        _my_color, _opp_color = _logger.initial_save(board)
    else:
        pass
    
    stone_count = sum(1 for row in board for cell in row if cell != 0)
    current_step = stone_count - 4 + 1
    
	# 相手ターンの保存

	# 差分を求める 相手が何を打ったのか
    opp_action = [0, 0]
    _logger.save(_step, _opp_color, "MOVED", board, opp_action)

	# 
	if _my_color == "white":
		_step += 1
    
    # 3. 思考中のログ保存 (THINKING)
    # Play.pyから渡されるboardは正規化(自分が1)されているためそのまま記録
	_logger.save(_step, _my_color, "THINKING", board)

    # --- AIの思考ロジック (ここは変更なし) ---
	index = random.randrange(len(moves))
	action = moves[index]
    # -------------------------------------

    # OthelloLogicを使って手を反映させる (playerは常に1)
    # execute(board, action, player, size)
	next_board = OthelloLogic.execute(board, action, 1, len(board))

    # 5. 決定したログ保存 (MOVED)
	_logger.save(_step, _my_color, "MOVED", next_board, action)

	return action