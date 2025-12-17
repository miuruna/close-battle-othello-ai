#自分の手の評価値、均衡になるように,ある定数に近づけたい
#自分の手が多い→正の値
#相手の手が多い→負の値
#1 = 自分の手
#-1 = 相手の手
#0 = 空マス
#次の一手を選ぶ考え方
#打てる手をすべて列挙、その手を打った「仮の盤面」を作る
#評価値を計算、目標評価値に一番近い手を選ぶ

def simulate_move(board, move, player):
    new_board = [row[:] for row in board]
    x, y = move

    new_board[x][y] = player
    # 本当はここで挟んだ石を反転する処理を書く

    return new_board


def select_move(board, next_moves, player):

    #board = 現在の盤面
    #next_moves = 打てる手のリスト [(x, y), ...]
    #player = 自分の石 (1 or -1)
    
    #turn はターン

    if turn >= 70:
        target = 100
    else:
        target = 10

    #接戦にしたい評価値
    #評価値が0~100の時

    best_move = None
    best_diff = float("inf")

    

    for move in next_moves:
        new_board = simulate_move(board, move, player)
        score = evaluate(new_board)

        diff = abs(score - target)

        if diff < best_diff:
            best_diff = diff
            best_move = move

    return best_move