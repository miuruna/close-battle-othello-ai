import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import data_loader

def record_table(file_path, enable_select=False):
    data = data_loader.get_record(file_path)  # type: ignore
    record = [
        {'step': row['step'], 'turn': row['turn'], 'action': row['action']} 
        for row in data
    ]

    select_mode = "rerun" if enable_select else "ignore"

    event = st.dataframe(
        data = record,
        use_container_width = True,
        hide_index= True,
        on_select=select_mode,
        selection_mode="single-row"
    )

    if enable_select and len(event.selection.rows) > 0: # type: ignore
        selected_index = event.selection.rows[0] # type: ignore
        return selected_index
    return None

def totalization(black, white, progress, evaluation_value, my_color="black"):
    col1, col2, col3, col4 = st.columns(4)
    black_delta = "自分のAI" if my_color == "black" else None
    white_delta = "自分のAI" if my_color == "white" else None
    col1.metric("黒の個数", f"{black}個", delta=black_delta)
    col2.metric("白の個数", f"{white}個", delta=white_delta)
    col3.metric("進捗", f"{round(progress, 2)}%")
    if black + white != 0:
        col4.metric("自AIの優勢率", f"{round(evaluation_value)}%")
    else:
        col4.metric("自AIの優勢率", f"0.00 %")

def progress(rate):
    status_text = st.empty()
    status_text.text(f"盤面占有状況: {rate}%")
    progress_bar = st.progress(int(rate))

