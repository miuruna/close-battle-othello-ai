import streamlit as st
from utils import data_loader, calculator
from widgets import charts, board_ui, summary_ui
import os

st.set_page_config(layout="wide", page_icon=":archive:")

st.title("LOG")
current_dir = os.path.dirname(os.path.abspath(__file__))
target_data_dir = os.path.join(current_dir, "../../data")
target_data_dir = os.path.normpath(target_data_dir)
all_files = data_loader.all_file_path(target_data_dir)

if not all_files:
    st.error("dataフォルダにファイルが見つかりません")
else:
    select_file = st.selectbox(
        "分析するファイルを選んでください",
        all_files,
        format_func=lambda x: os.path.basename(x[0])
    )
    my_color = data_loader.get_my_color(select_file[0])
    col1, col2 = st.columns(2)
    with col1:
        selected_step = summary_ui.record_table(select_file[0], enable_select=True)
    with col2:
        tab1, tab2, tab3 = st.tabs(["Board", "Phase Evaluation", "Thinking Time"])
        with tab1:
            if selected_step is not None:
                record_data = data_loader.get_record(select_file[0])
                black, white, rate, share = calculator.count_stones(record_data[selected_step]['board'], my_color)
                summary_ui.totalization(black, white, rate, share, my_color)
                board_ui.draw_board(record_data[selected_step]['board'], my_color)
            else:
                st.info("行をクリックすると, その時点の盤面が表示されます")
        with tab2:
            st.subheader("戦況推移")
            charts.draw_trend_graph(data_loader.get_record(select_file[0]), my_color)
        with tab3:
            st.subheader("思考時間の推移")
            charts.draw_time_graph(select_file[0])

