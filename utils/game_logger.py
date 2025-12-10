import csv
import json
from datetime import datetime
import os
import random
import string
from glob import glob
from . import data_loader

# 保存先のディレクトリ名
LOG_DIR_NAME = "data"


class GameLogger:
    def __init__(self):
        # TO DO 1: このファイルがある場所のパスを取得する
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # TO DO 2: 保存先フォルダの絶対パスをつくる
        self.log_dir = os.path.join(base_dir, "..", "..",LOG_DIR_NAME)

        # TO DO 3: フォルダが存在しなかったら作成する
        os.makedirs(self.log_dir, exist_ok=True)

        # 途中だった場合に前のファイルから続ける
        latest_file = data_loader.get_latest_modified_file_path(self.log_dir)
        if data_loader.is_playing(latest_file):
            self.filepath = latest_file
            return

        # TO DO 4: ファイル名を決める
        now = datetime.now()
        now_str = now.strftime('%Y-%m-%d_%H%M%S')
        rand_str = ''.join([random.choice(string.ascii_letters) for i in range(4)])
        filename = f"log_{now_str}_{rand_str}.csv"
        self.filepath = os.path.join(self.log_dir, filename)

        # TO DO 5: ヘッダーのリストを定義
        self.headers = ["timestamp", "step", "turn", "status", "board", "action"]

        # TO DO 6: ファイルを新規作成してヘッダーを書き込むメソッドを呼ぶ
        self._init_csv()
    
    # ファイルを生成しヘッダーを書き込む
    def _init_csv(self):
        # TO DO 7: self.filepath を "w" で開き self.headers を書き込む
        with open(self.filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def save(self, step, turn, status, board, action=None):
        """
        対戦状況を1行追記する
        
        :param step: 手数
        :param turn: "black" or "white"
        :param status: "THINKING" or "MOVED"
        :param board: 盤面の2次元配列
        :param action: 打った場所[x, y] (ない場合はNone)
        """

        # TO DO 8 現在時刻の文字列を取得する
        now_timestamp = datetime.now().strftime('%H:%M:%S.%f')

        # TO DO 9 盤面データをJSON形式の文字列に変換
        board_str = json.dumps(board)

        # TO DO 10 action もあれば JSON文字列に変換する なければ空文字にする
        if action:
            action_str = json.dumps(action)
        else:
            action_str = ""

        # TO DO 11 self.filepath を "a"で開き1行書き込む
        with open(self.filepath, 'a') as f:
            writer = csv.writer(f)
            row = [now_timestamp, step, turn, status, board_str, action_str]
            writer.writerow(row)

        print(f"Log saved: Step{step} ({status})")

    def initial_save(self, board, action=None):
        # 先攻か後攻か
        count = 0
        for row in board:
            for cell in row:
                if cell != 0:
                    count += 1
        if count % 2 == 0:
            my_turn, opp_turn = "black", "white"
        else:
            my_turn, opp_turn = "white", "black"
        
        initial_board = self.get_initial_board(board, my_turn)

        # 初期データの保存
        self.save(0, "SYSTEM", "INITIAL", initial_board)

        if count % 2 != 0:
            # action を探す
            action = self.get_action(initial_board, board)
            self.save(1, "black", "MOVED", board, action)
        
        return my_turn, opp_turn

    def get_initial_board(self, board, my_turn):
        size = len(board)
        initial_board = []
        for i in range(size):
            row = []
            for j in range(size):
                mid = size // 2
                if i == mid - 1 and j == mid - 1: # 左上
                    row.append(1 if my_turn == "white" else -1) # 白番なら自分(1)が白、つまり左上は白
                elif i == mid and j == mid:     # 右下
                    row.append(1 if my_turn == "white" else -1)
                elif i == mid - 1 and j == mid: # 右上
                    row.append(-1 if my_turn == "white" else 1)
                elif i == mid and j == mid - 1: # 左下
                    row.append(-1 if my_turn == "white" else 1)
                else:
                    row.append(0)
            initial_board.append(row)
        return initial_board
    
    def get_action(self, prev_board, new_board):
        action = None
        for r in range(len(new_board)):
            for c in range(len(new_board)):
                if prev_board[r][c] == 0 and new_board[r][c] != 0:
                    action = [r, c]
        return action





