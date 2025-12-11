import streamlit as st
import pandas as pd
from config.config import SENTIMENT_THRESHOLD
from app.cli.telegram_auth import is_telegram_logged_in
from config.config import (
    PLATFORM_LABELS,
    PLATFORM_MAP,
    COIN_OPTIONS,
    PERIOD_LABELS,
    PERIOD_MAP,
)
from app.visualization.plots import (
    plot_sentiment_distribution,
    plot_sentiment_by_source,
    plot_sentiment_pie,
    plot_post_timeline,
)


def show_config_summary():
    if not st.session_state.get("config_applied"):
        return

    st.markdown("---")
    st.markdown("### ⚙️ Current configuration")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**🌐 Platform**")
        st.markdown(
            f"<h3 style='margin-top:-10px'> \
            {st.session_state['cfg_platform'].capitalize()}</h3>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown("**🪙 Coin**")
        st.markdown(
            f"<h3 style='margin-top:-10px'> \
            {st.session_state['cfg_coin']}</h3>",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown("**📆 Period**")
        st.markdown(
            f"<h3 style='margin-top:-10px'> \
            {st.session_state['cfg_period']}</h3>",
            unsafe_allow_html=True,
        )


def sentiment_face(score: float):
    if score >= SENTIMENT_THRESHOLD:
        return "😄"
    if score <= -SENTIMENT_THRESHOLD:
        return "😞"
    return "😐"


def select_platform():
    st.subheader("1. Choose platform")

    prev = st.session_state.get("cfg_platform", "reddit")
    default_label = next(
        (label for label, key in PLATFORM_MAP.items() if key == prev),
        PLATFORM_LABELS[0],
    )

    label = st.radio(
        "Platform",
        PLATFORM_LABELS,
        horizontal=True,
        index=PLATFORM_LABELS.index(default_label),
    )

    key = PLATFORM_MAP[label]

    if key == "telegram" and not is_telegram_logged_in():
        st.warning("You need to login using CLI first.")
        st.stop()

    return key


def select_coin():
    st.subheader("2. Choose coin")

    prev = st.session_state.get("cfg_coin", "BTC")

    if prev not in COIN_OPTIONS:
        idx = COIN_OPTIONS.index("Custom")
        default_custom = prev
    else:
        idx = COIN_OPTIONS.index(prev)
        default_custom = ""

    choice = st.radio("Coin", COIN_OPTIONS, horizontal=True, index=idx)

    if choice == "Custom":
        val = st.text_input(
            "Enter custom coin:", value=default_custom
        ).upper().strip()
        return val, bool(val)

    return choice, True


def select_period():
    st.subheader("3. Choose period")

    prev = st.session_state.get("cfg_period", "day")
    default_label = next(
        (label for label, key in PERIOD_MAP.items() if key == prev),
        PERIOD_LABELS[0],
    )

    label = st.radio(
        "Time window",
        PERIOD_LABELS,
        horizontal=True,
        index=PERIOD_LABELS.index(default_label),
    )

    return PERIOD_MAP[label]


def apply_config_button(platform, coin, period, enabled=True):
    st.markdown("---")
    if st.button(
        "✅ Apply configuration",
        disabled=not enabled,
        use_container_width=True,
    ):
        st.session_state["cfg_platform"] = platform
        st.session_state["cfg_coin"] = coin
        st.session_state["cfg_period"] = period
        st.session_state["config_applied"] = True
        st.success("Configuration applied!")


def render_review_card(row, index, total):
    """Small, reusable card."""
    author = row.get("author") or row.get("channel") or "Unknown"
    title = row.get("title") or "(no title)"
    text = row.get("text") or "(no text)"
    score = float(row.get("compound", 0))
    label = row.get("sentiment", "neutral")

    st.markdown(f"**{author}**")

    left, mid, right = st.columns([1, 4, 1])

    with left:
        if st.button("◀", key=f"prev_{index}"):
            st.session_state["review_index"] = (index - 1) % total
            st.rerun()

    with mid:
        st.markdown(
            f"<div style='text-align:center; \
            font-weight:bold;'>{title}</div>",
            unsafe_allow_html=True,
        )

    with right:
        if st.button("▶", key=f"next_{index}"):
            st.session_state["review_index"] = (index + 1) % total
            st.rerun()

    st.write(text)
    st.markdown(f"*Sentiment:* **{label}** · Score `{score:.3f}`")


def has_enough_data(df: pd.DataFrame, min_count: int = 10):
    return df is not None and len(df) >= min_count


def visualize_graphs(df, platform, period):
    st.markdown("---")
    st.subheader("📈 Sentiment Visualizations")

    if not has_enough_data(df):
        st.info("Not enough data for visualization (need at least 10 posts).")
        return

    st.markdown("### 1. Sentiment Distribution")
    plot_sentiment_distribution(df)

    st.markdown("### 2. Sentiment by Source")
    plot_sentiment_by_source(df, platform)

    st.markdown("### 3. Sentiment Breakdown")
    plot_sentiment_pie(df)

    st.markdown("### 4. Posting Activity Timeline")
    plot_post_timeline(df, period)
