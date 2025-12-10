# Othello Areana AI with Streamlit Dashboard

Othello Arena 用の Python プログラムに監視システムを追加したもの

Othello Arena用のPythonプログラム: https://github.com/KousukeIshii/OthelloArenaPython

## 実行方法
インストールが必要なライブラリは`requirments.txt`にあるため仮想環境を作成してインストールすること

### オセロAIのみを実行する
```bash
python othello_arena/Play.py
```
### ダッシュボードのみを実行する
```bash
streamlit run dashboard/live.py
```
### オセロAIを実行しリアルタイムで実行状況を監視する
```bash
python run.py
```

## ディレクトリ・ファイル構成

### dashboard
#### `live.py`
ダッシュボードで最初に実行されるファイル
#### `pages`
このディレクトリ内にあるファイルがページを表す
ダッシュボードのページをふやしたい場合はここにファイルを追加してコードを書く
#### `widgets`

#### `utils`
必要な関数が入ったディレクトリです

### othello_arena
#### `OthelloAction.py`
AIオセロでは基本的にこの部分を操作することになる
##### `getAction(board, moves, step, my_turn, logger:GameLogger)`
| 列名 | 概要 |
| --- | --- |
| board | 盤面に関するデータ |
| moves | 自分が石を置ける場所のリスト |
| step | 何ターン目か |
| my_turn | black or white |
| logger | GameLoggerオブジェクト |

呼び出された時点で`logger.save(...)`によって思考を開始したことを記録
次の盤面まで求めた時点で`logger.save(...)`によって決定したことを記録

返り値として次に打つ手`next_move`とそれを打った後の盤面`next_board`を返却する

### data
オセロAIが実行した結果をCSVデータで保存する
ダッシュボードはここからファイルを読み出し分析する
CSVの構成は以下の通り

| 列名 | 概要 |
| --- | --- |
| timestamp | 時刻 |
| step | ターン数を記録 |
| turn | どちらの手番かを記録 "black", "white", "SYSTEM" |
| status | "MOVED", "THINKING", "INITIAL", "GAMEOVER" |
| board | 盤面データを記録 |
| action | 動かした最新の手を記録 (NULLを許す) |