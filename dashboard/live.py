import streamlit as st
from utils import data_loader, calculator
from widgets import summary_ui, charts
import time
import os

st.set_page_config(layout="wide", page_icon=":browse_activity:")

st.title("LIVE")
current_dir = os.path.dirname(os.path.abspath(__file__))
target_data_dir = os.path.join(current_dir, "../data")
target_data_dir = os.path.normpath(target_data_dir)
file_path = data_loader.get_latest_modified_file_path(target_data_dir)

if calculator.is_playing(file_path):
    my_color = data_loader.get_my_color(file_path)
    black, white, rate, share = calculator.get_latest_score(file_path)
    summary_ui.totalization(black, white, rate, share, my_color)
    summary_ui.progress(rate)
    col1, col2 = st.columns(2)
    with col1:
        summary_ui.record_table(file_path)
    with col2:
        st.subheader("戦況推移")
        charts.draw_trend_graph(data_loader.get_record(file_path), my_color)
    time.sleep(2)
    st.rerun()
else:
    st.write("実行中の試合はありません")



