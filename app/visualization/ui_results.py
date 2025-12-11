import streamlit as st
import pandas as pd
from app.visualization.ui_components import render_review_card, sentiment_face
from config.config import SENTIMENT_THRESHOLD

def reset_analysis_state():
    """Clear all sentiment-related session data."""
    st.session_state.pop("analysis_started", None)
    st.session_state.pop("sentiment_score", None)
    st.session_state.pop("sentiment_csv_path", None)
    st.session_state.pop("review_index", None)
    st.session_state["page"] = "config"

def render_back_button_after_analysis():
    if st.button("⬅ Back to configuration"):
        reset_analysis_state()
        st.rerun()

def render_run_sentiment_button(platform, coin, period,
                                run_telegram, collect_platform_data,
                                run_preprocessing, analyze_sentiment,
                                processed_dir):
    """UI + logic for the complete sentiment pipeline."""

    if st.button("🚀 Run sentiment analysis", type="primary", use_container_width=True):
        st.session_state["analysis_started"] = True
        st.info("Collecting data...")

        # collect raw data first
        raw_csv = run_telegram(coin, period) if platform == "telegram" \
                  else collect_platform_data(platform, coin, period)

        if not raw_csv:
            st.error("Failed to collect data.")
            return False

        st.info("Preprocessing...")
        soft_csv = run_preprocessing(raw_csv, platform)

        st.info("Analyzing sentiment...")
        sentiment_csv = analyze_sentiment(
            soft_csv, processed_root=processed_dir, source=platform
        )

        from app.src.sentiment import total_sentiment
        score = total_sentiment(sentiment_csv, platform)

        # Save state
        st.session_state["sentiment_score"] = score
        st.session_state["sentiment_csv_path"] = sentiment_csv

        st.success("Sentiment analysis complete!")
        st.rerun()

    return True


def render_sentiment_summary(score):
    """Summary box: emoji + sentiment interpretation."""
    face = sentiment_face(score)

    if score >= SENTIMENT_THRESHOLD:
        label = "positive"
    elif score <= SENTIMENT_THRESHOLD:
        label = "negative"
    else:
        label = "neutral"

    left, right = st.columns([1, 2])

    with left:
        st.markdown(
            f"<div style='font-size:64px; text-align:center;'>{face}</div>",
            unsafe_allow_html=True)

    with right:
        st.write(f"**Sentiment score:** `{score:.3f}`")
        st.write(f"**Interpretation:** {label.capitalize()} market mood.")
        st.write("Weighted VADER sentiment using engagement as weights.")

    return face


def render_reviews_section(df: pd.DataFrame):
    """Display a single review + previous/next buttons."""
    if "review_index" not in st.session_state:
        st.session_state["review_index"] = 0

    idx = st.session_state["review_index"]
    idx = max(0, min(idx, len(df) - 1))
    st.session_state["review_index"] = idx

    row = df.iloc[idx]
    render_review_card(row, index=idx, total=len(df))

    st.caption(f"Post {idx + 1} / {len(df)}")
