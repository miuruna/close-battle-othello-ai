import streamlit as st
import matplotlib.pyplot as plt
import json


def draw_board(board_data, my_color):
    try:
        board = json.loads(board_data)
    except (json.JSONDecodeError, KeyError):
        return

    SIZE = len(board)

    if my_color == "white":
        black, white = -1, 1
    else:
        black, white = 1, -1

    # 図(figure)と軸(ax)を作る
    # facecolor='k' (黒背景), axの背景を 'g' (緑) に設定
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('k') # type: ignore # 外側の背景色（黒）
    ax.set_facecolor('green')    # 盤面の色（緑）

    # 軸のメモリ文字色などを白にする設定
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    line_width = 2

    for y in range(SIZE):
        plt.axhline(y-0.5, color='k', lw=line_width)
        for x in range(SIZE):
            plt.axvline(x-0.5, color='k', lw=line_width)
            if board[y][x] == black:
                plt.plot(x, y, 'o', color='k', ms=30)
            elif board[y][x] == white:
                plt.plot(x, y, 'o', color='w', ms=30)
    
    # 範囲設定など
    ax.set_xlim([-0.5, SIZE - 0.5]) # type: ignore
    ax.set_ylim([SIZE - 0.5, -0.5]) # type: ignore # 上下を逆にして、配列の見た目(上=0)と合わせる
    ax.set_aspect('equal', adjustable='box')

    # 余計なメモリを消す
    ax.set_xticks([])
    ax.set_yticks([])

    # st.pyplot を使う
    st.pyplot(fig)