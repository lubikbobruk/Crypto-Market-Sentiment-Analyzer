import streamlit as st
from app.visualization.ui_components import *
from app.visualization.ui_results import *

def render_config_page():
    st.title("🧠 Crypto Sentiment Analyzer")
    st.write("Select data source, coin, and time period.")

    platform = select_platform()
    coin, valid = select_coin()
    period = select_period()

    apply_config_button(platform, coin.upper(), period, enabled=valid)

    show_config_summary()

    if st.session_state.get("config_applied"):
        if st.button("Next ▶", use_container_width=True):
            st.session_state["page"] = "results"
            st.rerun()
