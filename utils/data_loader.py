import os
from glob import glob
import csv

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
    
# 試合が実行中かどうかを返す関数
def is_playing(file_path) -> bool:
    if file_path is None:
        return False
    data_list = csv_read(file_path)
    if len(data_list) == 0:
        return True
    return data_list[-1]['status'] != "GAMEOVER"