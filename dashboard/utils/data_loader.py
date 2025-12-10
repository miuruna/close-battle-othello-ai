import os
from glob import glob
import csv
import json

# 更新が最新のファイルパスを返す変数
def get_latest_modified_file_path(dirname):
    files = all_file_path(dirname)
    if not files:
        return None
    latest_modified_file_tuple = sorted(files, key=lambda files: files[1])[-1]
    return latest_modified_file_tuple[0]

# ディレクトリ内のファイルを全て返す変数
def all_file_path(dirname):
    target = os.path.join(dirname, '*')
    files = [(f, os.path.getmtime(f)) for f in glob(target)]
    return files

# CSVファイルを読み込んで辞書化して返す
def csv_read(file_path):
    try:
        with open (file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            l = [row for row in reader]
        return l
    except Exception:
        return []

# 棋譜を返す関数
def get_record(file_path):
    if file_path is None:
        return None
    data_list = csv_read(file_path)
    if len(data_list) == 0:
        return None
    record = []
    for row in data_list:
        if row['status'] == 'THINKING' or row['turn'] == 'SYSTEM':
            continue
        else:
            record_row = {'step':row['step'], 'turn': row['turn'], 'action': row['action'], 'board': row['board']}
            record.append(record_row)
    return record

# 自分の色を特定する
def get_my_color(file_path):
    if file_path is None:
        return None
    raw_data = csv_read(file_path)
    # THINKING は 自分の手番にしか出現しないためその行から色を導き出す
    for row in reversed(raw_data):
        if row['status'] == 'THINKING':
            return row['turn']
    # THINKING の 行がみつからなかった場合
    board = raw_data[-1]['board']
    if isinstance(board, str):
        try:
            board = json.loads(board)
        except:
            return "black"
    # 石を数える
    stone_count = 0
    for row in board:
        for cell in row:
            if cell != 0:
                stone_count += 1
    # (石の数 - 4) が偶数か奇数かで判定
    if (stone_count - 4) % 2 == 0:
        return "black"
    else:
        return "white"

def safe_parse_board(board_data):
    if isinstance(board_data, list):
        return board_data
    try:
        parsed = json.loads(board_data)
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
        return parsed
    except Exception as e:
        return []