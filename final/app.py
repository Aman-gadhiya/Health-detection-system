"""
===============================================================================
MindPulse — Student Social Media & Mental Health Analytics
-------------------------------------------------------------------------------
Home page: dataset overview + navigation into the rest of the app.
Run with:  streamlit run app.py
===============================================================================
"""

import streamlit as st

import config
from utils.data import load_dataset
from utils.model import load_model
from utils.theme import inject_css, masthead

st.set_page_config(
    page_title=f"{config.APP_NAME} · {config.APP_TAGLINE}",
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state=config.SIDEBAR_STATE,
)

inject_css()

with st.sidebar:
    st.markdown(f"### {config.PAGE_ICON} {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)
    st.divider()
    st.caption(f"v{config.VERSION} · ExtraTreesRegressor · 300 trees")

df = load_dataset()
model = load_model()  # warm the cache on first load

masthead(
    "Overview",
    "Reading the room, one student at a time.",
    "5,000 self-reported profiles link daily social-media habits — usage, "
    "unlocks, sleep, study, and activity — to a 0–10 Mental Health Score. "
    "This dashboard explores that data and puts the trained model to work.",
)

# ---------------------------------------------------------------------------
# Headline stats
# ---------------------------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="mp-card"><div class="mp-stat">{len(df):,}</div>'
        f'<div class="mp-stat-label">Student profiles</div></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="mp-card"><div class="mp-stat">{df["Mental_Health_Score"].mean():.2f}</div>'
        f'<div class="mp-stat-label">Avg. health score/10</div></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f'<div class="mp-card"><div class="mp-stat">{df["Avg_Daily_Usage_Hours"].mean():.1f}h</div>'
        f'<div class="mp-stat-label">Avg. daily social-media use</div></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f'<div class="mp-card"><div class="mp-stat">{df["Sleep_Hours_Per_Night"].mean():.1f}h</div>'
        f'<div class="mp-stat-label">Avg. sleep / night</div></div>',
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# ---------------------------------------------------------------------------
# Navigation cards
# ---------------------------------------------------------------------------

st.markdown('<span class="mp-eyebrow">Where to next</span>', unsafe_allow_html=True)
n1, n2, n3 = st.columns(3)
with n1:
    st.markdown(
        '<div class="mp-card"><h4>📊 Data Explorer</h4>'
        '<p>Filter by country, platform, and academic level. See how usage, '
        'sleep, and stress relate to mental health across the cohort.</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Data_Explorer.py", label="Open Data Explorer →")
with n2:
    st.markdown(
        '<div class="mp-card"><h4>🧠 Predict</h4>'
        '<p>Enter a student profile and get an instant, model-scored '
        'Mental Health Score with a plain-language read-out.</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Predict.py", label="Open Predict →")
with n3:
    st.markdown(
        '<div class="mp-card"><h4>📈 Model Insights</h4>'
        '<p>What the ExtraTreesRegressor actually learned: feature '
        'importance, held-out accuracy, and residual behavior.</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Model_Insights.py", label="Open Model Insights →")

st.write("")
st.markdown('<span class="mp-eyebrow">A first look at the data</span>', unsafe_allow_html=True)
st.dataframe(df.drop(columns=["Grouped_country", "Productive_Hours", "Lifestyle_Balance"]).head(12), use_container_width=True, hide_index=True)

st.caption(
    "Grouped_country, Productive_Hours, and Lifestyle_Balance are engineered "
    "at inference time for the model and are hidden here to match the raw "
    "source file — see Model Insights for the full feature contract."
)
