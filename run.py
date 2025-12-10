import subprocess
import time

dashboard_process = None
othello_arena_process = None

try: 
    # コマンドの定義
    othello_arena_command = ["python", "othello_arena/Play.py"]
    dashboard_command = ["streamlit", "run", "dashboard/live.py"]

    # ダッシュボードの起動
    dashboard_process = subprocess.Popen(dashboard_command, shell=True)
    time.sleep(3)

    # Play.pyの起動
    othello_arena_process = subprocess.Popen(othello_arena_command, shell=True)

    while True:
        if dashboard_process.poll() is not None:
            print("ダッシュボードが終了しました")
            break
        if othello_arena_process.poll() is not None:
            print("オセロAIが終了しました")
        time.sleep(1)
except KeyboardInterrupt:
    print("停止します")
finally:
    print("プロセスを終了しています")
    if othello_arena_process:
        othello_arena_process.terminate()
        try:
            othello_arena_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            othello_arena_process.kill()
        print("- AI Stopped")
    
    if dashboard_process:
        dashboard_process.terminate()
        try:
            dashboard_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            dashboard_process.kill()
        print("- Dashboard Stopped")

