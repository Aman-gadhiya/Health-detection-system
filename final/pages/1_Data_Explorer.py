"""Data Explorer — filterable view of the training dataset."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import config
from utils.data import load_dataset
from utils.theme import inject_css, masthead

st.set_page_config(
    page_title=f"Data Explorer · {config.APP_NAME}",
    page_icon="📊",
    layout=config.LAYOUT,
)
inject_css()

with st.sidebar:
    st.markdown(f"### {config.PAGE_ICON} {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)

df = load_dataset()

masthead("Data Explorer", "Filter the cohort.", "Slice the 5,000-student dataset and watch every chart update in place.")

# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

f1, f2, f3, f4 = st.columns(4)
with f1:
    levels = st.multiselect("Academic level", sorted(df["Academic_Level"].unique()), default=list(sorted(df["Academic_Level"].unique())))
with f2:
    platforms = st.multiselect("Platform", sorted(df["Most_Used_Platform"].unique()), default=list(sorted(df["Most_Used_Platform"].unique())))
with f3:
    stress = st.multiselect("Stress level", config.STRESS_LEVELS, default=config.STRESS_LEVELS)
with f4:
    age_range = st.slider("Age", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

fdf = df[
    df["Academic_Level"].isin(levels)
    & df["Most_Used_Platform"].isin(platforms)
    & df["Stress_Level"].isin(stress)
    & df["Age"].between(*age_range)
]

st.caption(f"**{len(fdf):,}** of {len(df):,} students match the current filters.")
st.write("")

if fdf.empty:
    st.warning("No students match this combination of filters — widen your selection.")
    st.stop()

palette = [config.COLOR_TEAL, config.COLOR_SAGE, config.COLOR_AMBER, config.COLOR_CORAL, "#7C93B0", "#B08FC7"]

# ---------------------------------------------------------------------------
# Row 1 — usage vs mental health, stress distribution
# ---------------------------------------------------------------------------

r1c1, r1c2 = st.columns([3, 2])

with r1c1:
    st.markdown('<span class="mp-eyebrow">Daily usage vs. mental health score</span>', unsafe_allow_html=True)
    fig = px.scatter(
        fdf, x="Avg_Daily_Usage_Hours", y="Mental_Health_Score",
        color="Stress_Level", category_orders={"Stress_Level": config.STRESS_LEVELS},
        color_discrete_sequence=[config.COLOR_SAGE, config.COLOR_TEAL, config.COLOR_AMBER, config.COLOR_CORAL],
        opacity=0.65,
        labels={"Avg_Daily_Usage_Hours": "Avg. daily usage (hrs)", "Mental_Health_Score": "Mental health score"},
    )
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.markdown('<span class="mp-eyebrow">Stress level distribution</span>', unsafe_allow_html=True)
    counts = fdf["Stress_Level"].value_counts().reindex(config.STRESS_LEVELS).fillna(0)
    fig2 = go.Figure(
        go.Bar(
            x=counts.values, y=counts.index, orientation="h",
            marker_color=[config.COLOR_SAGE, config.COLOR_TEAL, config.COLOR_AMBER, config.COLOR_CORAL],
        )
    )
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Students",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 2 — sleep vs score, platform breakdown
# ---------------------------------------------------------------------------

r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown('<span class="mp-eyebrow">Sleep vs. mental health score</span>', unsafe_allow_html=True)
    fig3 = px.scatter(
        fdf, x="Sleep_Hours_Per_Night", y="Mental_Health_Score",
        color="Academic_Level", opacity=0.65,
        color_discrete_sequence=palette,
        labels={"Sleep_Hours_Per_Night": "Sleep (hrs/night)", "Mental_Health_Score": "Mental health score"},
    )
    fig3.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.markdown('<span class="mp-eyebrow">Avg. score by platform</span>', unsafe_allow_html=True)
    by_platform = fdf.groupby("Most_Used_Platform")["Mental_Health_Score"].mean().sort_values()
    fig4 = go.Figure(
        go.Bar(
            x=by_platform.values, y=by_platform.index, orientation="h",
            marker_color=config.COLOR_TEAL,
        )
    )
    fig4.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Avg. mental health score",
    )
    st.plotly_chart(fig4, use_container_width=True)

st.write("")
st.markdown('<span class="mp-eyebrow">Filtered rows</span>', unsafe_allow_html=True)
st.dataframe(
    fdf.drop(columns=["Grouped_country", "Productive_Hours", "Lifestyle_Balance"]),
    use_container_width=True, hide_index=True,
)

