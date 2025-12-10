import json
from . import data_loader
from datetime import datetime

def count_stones(board_input, my_color="black"):
    if board_input is None:
        return 0, 0, 0, 0
    
    if isinstance(board_input, str):
        try:
            board = json.loads(board_input)
        except:
            return 0, 0, 0, 0
    elif isinstance(board_input, list):
        board = board_input
    else:
        return 0, 0, 0, 0
    
    empty, my_count, opp_count, share = 0, 0, 0, 0
    for row in board:
        for cell in row:
            if cell == 0:
                empty += 1
            elif cell == 1:
                my_count += 1
            elif cell == -1:
                opp_count += 1
    
    if my_count + opp_count == 0:
        share = 50
    else:
        share = my_count / (my_count + opp_count) * 100
    
    if my_color == "black":
        black = my_count
        white = opp_count
    else:
        black = opp_count
        white = my_count

    total = black + white + empty
    if total == 0:
        return 0, 0, 0, 0
    
    rate = ((black + white) / total) * 100
    return black, white, rate, share

def get_latest_score(file_path):
    if file_path is None:
        return 0, 0, 0, 0
    
    data_list = data_loader.get_record(file_path)

    if not data_list:
        return 2, 2, (4/60)*100, 50
    
    latest_data = data_list[-1]
    my_color = data_loader.get_my_color(file_path)
    return count_stones(latest_data['board'], my_color)

# 試合が実行中かどうかを返す関数
def is_playing(file_path) -> bool:
    if file_path is None:
        return False
    data_list = data_loader.csv_read(file_path)
    if len(data_list) == 0:
        return True
    return data_list[-1]['status'] != "GAMEOVER"


def calculate_thinking_time(file_path):
    raw_data = data_loader.csv_read(file_path)
    
    if not raw_data:
        return []
    
    time_data = []
    start_time = None

    time_fmt = "%H:%M:%S.%f"

    for row in raw_data:
        try:
            current_time = datetime.strptime(row['timestamp'], time_fmt)
        except ValueError:
            continue

        status = row['status']

        if status == "THINKING":
            start_time = current_time
        elif status == "MOVED":
            if start_time is not None:
                duration = (current_time - start_time).total_seconds()
                time_data.append({
                    "step": int(row['step']),
                    "time": duration,
                    "turn": row['turn']
                })
                start_time = None
    return time_data

def calculate_metric(board_data, my_color):
    black, white, rate, share = count_stones(board_data, my_color)
    return share