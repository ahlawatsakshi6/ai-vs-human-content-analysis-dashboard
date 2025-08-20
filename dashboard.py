import sys
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st


def load_dataset(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Normalize and clean
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")

    if "Author_Type" in df.columns:
        df["Author_Type"] = df["Author_Type"].astype(str).str.strip().str.title()

    # Recompute engagement score if component metrics present
    if set(["Likes", "Comments", "Shares"]).issubset(df.columns):
        df["Engagement_Score"] = (
            df["Likes"].fillna(0)
            + df["Comments"].fillna(0) * 2
            + df["Shares"].fillna(0) * 3
        )

    # Drop duplicate rows if any
    df = df.drop_duplicates().reset_index(drop=True)
    return df


@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    # Resolve CSV path relative to this file for portability
    possible_paths: List[Path] = [
        Path(__file__).with_name("ai_vs_human_content_dataset.csv"),
        Path.cwd() / "ai_vs_human_content_dataset.csv",
        Path(r"ai_vs_human_content_dataset.csv"),
    ]
    csv_path = next((p for p in possible_paths if p.exists()), None)
    if csv_path is None:
        st.stop()
    return load_dataset(csv_path)


def format_big_number(value: float) -> str:
    if pd.isna(value):
        return "-"
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value/1_000:.2f}K"
    return f"{value:,.0f}"


def main() -> None:
    st.set_page_config(
        page_title="AI vs Human Content Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("AI vs Human Content Dashboard")
    st.caption("Interactive dashboard comparing engagement across AI-generated and human-written content.")

    df = get_data()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")

        # Date range
        min_date = pd.to_datetime(df["Date"]).min() if "Date" in df.columns else None
        max_date = pd.to_datetime(df["Date"]).max() if "Date" in df.columns else None
        if min_date is not None and pd.notna(min_date):
            start_date, end_date = st.date_input(
                "Date range",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date(),
            )
        else:
            start_date, end_date = None, None

        # Author type filter
        author_types = sorted(df["Author_Type"].dropna().unique().tolist()) if "Author_Type" in df.columns else []
        selected_author_types = st.multiselect(
            "Author type",
            options=author_types,
            default=author_types,
        )

        # Content type filter
        content_types = sorted(df["Content_Type"].dropna().unique().tolist()) if "Content_Type" in df.columns else []
        selected_content_types = st.multiselect(
            "Content type",
            options=content_types,
            default=content_types,
        )

    # Apply filters
    filtered = df.copy()
    if start_date and end_date and "Date" in filtered.columns:
        mask = (filtered["Date"] >= pd.Timestamp(start_date)) & (filtered["Date"] <= pd.Timestamp(end_date))
        filtered = filtered.loc[mask]

    if selected_author_types and "Author_Type" in filtered.columns:
        filtered = filtered[filtered["Author_Type"].isin(selected_author_types)]

    if selected_content_types and "Content_Type" in filtered.columns:
        filtered = filtered[filtered["Content_Type"].isin(selected_content_types)]

    if filtered.empty:
        st.warning("No data matches the current filters. Adjust filters to see results.")
        st.stop()

    # KPIs
    total_likes = float(filtered["Likes"].sum()) if "Likes" in filtered.columns else float("nan")
    avg_comments = float(filtered["Comments"].mean()) if "Comments" in filtered.columns else float("nan")
    total_shares = float(filtered["Shares"].sum()) if "Shares" in filtered.columns else float("nan")
    avg_engagement = float(filtered["Engagement_Score"].mean()) if "Engagement_Score" in filtered.columns else float("nan")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Likes", format_big_number(total_likes))
    with c2:
        st.metric("Avg Comments", f"{avg_comments:.2f}" if pd.notna(avg_comments) else "-")
    with c3:
        st.metric("Total Shares", format_big_number(total_shares))
    with c4:
        st.metric("Avg Engagement Score", f"{avg_engagement:.2f}" if pd.notna(avg_engagement) else "-")

    # Comparison chart: AI vs Human engagement (average)
    if set(["Author_Type", "Engagement_Score"]).issubset(filtered.columns):
        engagement_by_author = (
            filtered.groupby("Author_Type", as_index=False)["Engagement_Score"].mean().rename(columns={"Engagement_Score": "Avg Engagement"})
        )
        fig_bar = px.bar(
            engagement_by_author,
            x="Author_Type",
            y="Avg Engagement",
            color="Author_Type",
            title="Average Engagement Score: AI vs Human",
            text_auto=".2f",
        )
        fig_bar.update_layout(showlegend=False, xaxis_title="Author Type", yaxis_title="Avg Engagement Score")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Trendline over time by author type (average engagement)
    if set(["Date", "Author_Type", "Engagement_Score"]).issubset(filtered.columns):
        trend = (
            filtered.sort_values("Date").groupby(["Date", "Author_Type"], as_index=False)["Engagement_Score"].mean()
        )
        fig_trend = px.line(
            trend,
            x="Date",
            y="Engagement_Score",
            color="Author_Type",
            title="Engagement Trend Over Time",
        )
        fig_trend.update_layout(xaxis_title="Date", yaxis_title="Avg Engagement Score")
        st.plotly_chart(fig_trend, use_container_width=True)

    col_left, col_right = st.columns(2)
    with col_left:
        # Pie chart: % of total engagement by author type
        if set(["Author_Type", "Engagement_Score"]).issubset(filtered.columns):
            engagement_share = filtered.groupby("Author_Type", as_index=False)["Engagement_Score"].sum()
            fig_pie = px.pie(
                engagement_share,
                names="Author_Type",
                values="Engagement_Score",
                title="Share of Total Engagement by Author Type",
                hole=0.3,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Content type analysis: box plot of engagement by content type, colored by author type
        if set(["Content_Type", "Engagement_Score", "Author_Type"]).issubset(filtered.columns):
            fig_box = px.box(
                filtered,
                x="Content_Type",
                y="Engagement_Score",
                color="Author_Type",
                title="Engagement by Content Type (AI vs Human)",
            )
            fig_box.update_layout(xaxis_title="Content Type", yaxis_title="Engagement Score")
            fig_box.update_xaxes(tickangle=45)
            st.plotly_chart(fig_box, use_container_width=True)

    st.caption("Data source: ai_vs_human_content_dataset.csv. Engagement Score = Likes + 2×Comments + 3×Shares.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        # Ensure a readable error in Streamlit UI and CLI
        st.error(f"An error occurred: {exc}")
        print(f"Error: {exc}", file=sys.stderr)


