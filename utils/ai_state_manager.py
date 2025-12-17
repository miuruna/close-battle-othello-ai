import os
import json

INITIAL_MODEL = [0, 0, 0, 0.125, 0.125, 0.125, 0.125, 0.5]

class GameInfo:
    def __init__(self):
        self.turn_count: int = 0
        self.my_color: str | None = None
        self.board: list[list[int]] | None = None

class AiStateManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(base_dir, "ai_state.json")
        self.game_info = GameInfo()
        self.opponent_model = []

    def new_game(self, board:list, my_color:str):
        self.game_info.board = self.get_initial_board(board, my_color)
        self.game_info.my_color = my_color
        self.opponent_model = INITIAL_MODEL[:]
        self.save_json()

    def continue_game(self):
        d = self.read_json()
        self.game_info.turn_count = d['game_info']['turn_count']
        self.game_info.my_color = d['game_info']['my_color']
        self.game_info.board = d['game_info']['board']
        self.opponent_model = d['opponent_model']

    def read_json(self):
        with open(self.json_path) as f:
            d = json.loads(f.read())
        return d
    
    def save_json(self):
        info_dict = {}
        info_dict['turn_count'] = self.game_info.turn_count
        info_dict['my_color'] = self.game_info.my_color
        info_dict['board'] = self.game_info.board
        d = {}
        d['game_info'] = info_dict
        d['opponent_model'] = self.opponent_model
        with open(self.json_path, 'w') as f:
            json.dump(d, f, indent=4)

    def get_initial_board(self, board, my_color):
        size = len(board)
        initial_board = []
        for i in range(size):
            row = []
            for j in range(size):
                mid = size // 2
                if i == mid - 1 and j == mid - 1: # 左上
                    row.append(1 if my_color == "white" else -1) # 白番なら自分(1)が白、つまり左上は白
                elif i == mid and j == mid:     # 右下
                    row.append(1 if my_color == "white" else -1)
                elif i == mid - 1 and j == mid: # 右上
                    row.append(-1 if my_color == "white" else 1)
                elif i == mid and j == mid - 1: # 左下
                    row.append(-1 if my_color == "white" else 1)
                else:
                    row.append(0)
            initial_board.append(row)
        return initial_board