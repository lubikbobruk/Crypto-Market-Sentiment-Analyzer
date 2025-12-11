import streamlit as st
import pandas as pd
from pathlib import Path

from app.cli.actions import (
    run_telegram,
    collect_platform_data,
    run_preprocessing)
from app.src.sentiment import analyze_sentiment
from config.config import PROCESSED_DIR
from app.visualization.ui_results import (
    render_back_button_after_analysis,
    render_run_sentiment_button,
    render_sentiment_summary,
    render_reviews_section)
from app.visualization.ui_components import visualize_graphs


def load_sentiment_df(path_str: str):
    if not path_str:
        return None
    path = Path(path_str)
    if not path.exists():
        return None
    return pd.read_csv(path)


def render_results_page():
    """Page 2: Run sentiment & browse results."""
    st.title("📊 Sentiment Results")

    if not st.session_state.get("config_applied"):
        st.warning("No configuration applied yet.")
        if st.button("⬅ Back"):
            st.session_state["page"] = "config"
            st.rerun()
        return

    platform = st.session_state["cfg_platform"]
    coin = st.session_state["cfg_coin"]
    period = st.session_state["cfg_period"]

    # If sentiment has already started, show back button only
    if st.session_state.get("analysis_started"):
        render_back_button_after_analysis()
    else:
        cols = st.columns([1, 3])
        with cols[0]:
            if st.button("⬅ Back to configuration"):
                st.session_state["page"] = "config"
                st.rerun()

        with cols[1]:
            st.write(
                f"**Platform:** {platform.capitalize()}  •  "
                f"**Coin:** {coin}  •  **Period:** {period}")

        st.markdown("---")

        render_run_sentiment_button(
            platform,
            coin,
            period,
            run_telegram,
            collect_platform_data,
            run_preprocessing,
            analyze_sentiment,
            PROCESSED_DIR)
        return

    score = st.session_state.get("sentiment_score")
    sentiment_path = st.session_state.get("sentiment_csv_path")

    if score is None or sentiment_path is None:
        st.info("Run sentiment analysis to continue.")
        return

    st.markdown("## Overall sentiment")
    render_sentiment_summary(score)

    st.markdown("---")
    st.subheader("Sample posts")

    df = load_sentiment_df(sentiment_path)
    if df is None or df.empty:
        st.info("No posts available.")
        return

    render_reviews_section(df)
    visualize_graphs(df, platform, period)
