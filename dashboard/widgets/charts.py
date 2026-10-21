import streamlit as st
import altair as alt
import pandas as pd
from utils import calculator, OthelloLogic, evaluator
import json


def draw_trend_graph(record_list, my_color="black"):
    ev = evaluator.Evaluator()
    if not record_list:
        st.warning("グラフ表示用のデータがありません")
        return 

    chart_data = []
    
    for i, row in enumerate(record_list):

        board_raw = row.get('board')
        
        # 1. データ自体が存在しない、または空文字の場合はスキップ
        if not board_raw:
            print(f"警告: インデックス {i} 手目の board データが空です。スキップします。")
            continue
            
        try:
            board_list = json.loads(board_raw)
        except json.JSONDecodeError:
            # 2. JSONとして壊れている場合もスキップ（原因特定のために中身を表示）
            st.error(f"JSON解析エラー: {i}手目のデータが不正です -> {board_raw}")
            continue

        board_list = json.loads(row['board'])
        player = 1 if row['turn'] == my_color else -1
        moves = OthelloLogic.getMoves(board_list, player, len(board_list))
        score = ev.evaluate(board_list, 1, len(moves) * player)
        chart_data.append({
            "step": i,
            "score": score
        })
    
    df = pd.DataFrame(chart_data)

    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('step', title='手数'),
        y=alt.Y('score', scale=alt.Scale(domain=[0, 100]), title='優勢率(%)'),
        tooltip=['step', 'score']
    ).properties(
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

# 思考時間を計算する
def draw_time_graph(file_path):
    data = calculator.calculate_thinking_time(file_path)

    if not data:
        st.info("思考時間データが十分にありません")
        return
    
    df = pd.DataFrame(data)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('step', title='手数'),
        y=alt.Y('time', title='思考時間 (秒)'),
        color=alt.value("steelblue"), 
        tooltip=['step', 'time']
    ).properties(
        title=f"自AIの思考時間推移",
        height=300
    )

    st.altair_chart(chart, use_container_width=True)

