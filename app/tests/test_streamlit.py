"""Tests for Streamlit UI logic."""

import pandas as pd
import streamlit as st
from app.visualization.ui_components import apply_config_button
from app.visualization.ui_results import render_run_sentiment_button
from app.visualization.pages.page_results import load_sentiment_df


# ------------------
# Apply config test
# ------------------


def test_apply_config_button(monkeypatch):
    """Ensure apply_config_button sets session_state correctly."""

    # simulate clicking the button
    monkeypatch.setattr("streamlit.button", lambda *a, **k: True)
    st.session_state.clear()

    apply_config_button("reddit", "BTC", "day", enabled=True)

    assert st.session_state["cfg_platform"] == "reddit"
    assert st.session_state["cfg_coin"] == "BTC"
    assert st.session_state["cfg_period"] == "day"
    assert st.session_state["config_applied"] is True


# ---------------------------
# Fake sentiment run testing
# ---------------------------

# @generated "partially" ChatGPT 5.1
def test_render_run_sentiment_button(monkeypatch, tmp_path):
    """Simulates full sentiment pipeline and checks session state updates."""

    # imitate fake streamlit UI calls
    monkeypatch.setattr("streamlit.button", lambda *a, **k: True)
    monkeypatch.setattr("streamlit.info", lambda *a, **k: None)
    monkeypatch.setattr("streamlit.success", lambda *a, **k: None)
    monkeypatch.setattr("streamlit.error", lambda *a, **k: None)
    monkeypatch.setattr("streamlit.rerun", lambda *a, **k: None)

    # set sentiment to always be 0
    monkeypatch.setattr(
        "app.src.sentiment.total_sentiment",
        lambda *a, **k: 0,
    )

    st.session_state.clear()

    # fake the prerequisites and pass them to the sentiment runner
    def fake_run_telegram(*a, **k):
        return "raw.csv"

    def fake_collect_data(*a, **k):
        return "raw2.csv"

    def fake_preprocess(*a, **k):
        return "soft.csv"

    def fake_analyze(*a, **k):
        return "test.csv"

    result = render_run_sentiment_button(
        platform="telegram",
        coin="BTC",
        period="day",
        run_telegram=fake_run_telegram,
        collect_platform_data=fake_collect_data,
        run_preprocessing=fake_preprocess,
        analyze_sentiment=fake_analyze,
        processed_dir=str(tmp_path),
    )

    # because sentiment is biased by test to 0,
    # it must work regardless of input
    assert result is True
    assert st.session_state["sentiment_score"] == 0
    assert st.session_state["sentiment_csv_path"] == "test.csv"


# ------------------------
# Test load_sentiment_df
# ------------------------


def test_load_sentiment_df(tmp_path):
    """Ensure load_sentiment_df handles missing/valid file paths correctly."""

    # nonexistent CSV should return None
    assert load_sentiment_df("test.csv") is None

    df = pd.DataFrame({"col1": [1], "col2": [2]})

    path = tmp_path / "test.csv"
    df.to_csv(path, index=False)

    df = load_sentiment_df(str(path))

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]
    assert len(df) == 1
