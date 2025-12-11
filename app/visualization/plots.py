import pandas as pd
import streamlit as st
import plotly.express as px


def has_enough_data(df: pd.DataFrame, min_count: int = 10):
    return df is not None and len(df) >= min_count


def plot_sentiment_distribution(df: pd.DataFrame):
    fig = px.histogram(
        df,
        x="compound",
        nbins=30,
        title="Distribution of Sentiment Scores",
        labels={"compound": "VADER Compound Score"},
        opacity=0.75)
    fig.update_layout(bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)


def plot_engagement_vs_sentiment(df: pd.DataFrame, platform: str):
    weight_col = "score" if platform == "reddit" else "views"

    if weight_col not in df.columns:
        st.info(f"No engagement data ('{weight_col}') available.")
        return

    fig = px.scatter(
        df,
        x=weight_col,
        y="compound",
        title="Engagement vs Sentiment",
        labels={
            weight_col: weight_col.capitalize(),
            "compound": "Sentiment score",
        },
        trendline="ols")
    st.plotly_chart(fig, use_container_width=True)


def plot_sentiment_by_source(df: pd.DataFrame, platform: str):
    source_col = "channel" if platform == "telegram" else "subreddit"

    if source_col not in df.columns:
        st.info(f"No per-source data ('{source_col}') available.")
        return

    agg = df.groupby(source_col)["compound"].mean().reset_index()

    fig = px.bar(
        agg,
        x=source_col,
        y="compound",
        title="Average Sentiment by Source",
        labels={"compound": "Sentiment Score"},
        color="compound",
        color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)


def plot_sentiment_pie(df: pd.DataFrame):
    # classify sentiment
    def classify(c):
        if c >= 0.05:
            return "Positive"
        elif c <= -0.05:
            return "Negative"
        return "Neutral"

    df["label"] = df["compound"].apply(classify)

    counts = df["label"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]

    fig = px.pie(
        counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Breakdown",
        color="Sentiment",
        color_discrete_map={
            "Positive": "green",
            "Neutral": "gray",
            "Negative": "red"})
    st.plotly_chart(fig, use_container_width=True)


def plot_post_timeline(df: pd.DataFrame, period: str):
    """Plot posting activity.

    - If period == 'day' → group by hour
    - Else → group by date
    """

    import plotly.express as px

    if "datetime" not in df.columns:
        st.info("No datetime information available.")
        return

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    if df["datetime"].isna().all():
        st.info("Datetime values are invalid or missing.")
        return

    if period == "day":
        df["hour"] = df["datetime"].dt.hour

        hourly = (
            df.groupby("hour")
            .size()
            .reset_index(name="count")
            .sort_values("hour"))

        fig = px.line(
            hourly,
            x="hour",
            y="count",
            markers=True,
            title="Hourly Posting Activity (Last 24h)",
            labels={"hour": "Hour of day", "count": "Posts"})
        fig.update_xaxes(dtick=1)

        st.plotly_chart(fig, use_container_width=True)
        return

    df["date"] = df["datetime"].dt.date

    daily = (
        df.groupby("date")
        .size()
        .reset_index(name="count")
        .sort_values("date")
    )

    fig = px.line(
        daily,
        x="date",
        y="count",
        markers=True,
        title="Posting Activity Over Time",
        labels={"date": "Date", "count": "Posts per day"})

    st.plotly_chart(fig, use_container_width=True)
