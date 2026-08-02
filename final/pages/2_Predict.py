"""Predict — score a single student profile with the trained pipeline."""

from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import config
from utils.data import append_history, load_dataset
from utils.engineer import build_model_row
from utils.model import predict_one, score_band
from utils.theme import inject_css, masthead

st.set_page_config(
    page_title=f"Predict · {config.APP_NAME}",
    page_icon="🧠",
    layout=config.LAYOUT,
)
inject_css()

with st.sidebar:
    st.markdown(f"### {config.PAGE_ICON} {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)

df = load_dataset()

masthead("Predict", "Score a student profile.", "Fill in a habit profile and the ExtraTreesRegressor (300 trees) returns an instant Mental Health Score, 0–10.")

left, right = st.columns([2, 3], gap="large")

with left:
    with st.form("predict_form"):
        st.markdown('<span class="mp-eyebrow">Demographics</span>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        age = d1.number_input("Age", min_value=16, max_value=30, value=20)
        gender = d2.selectbox("Gender", ["Male", "Female"])
        d3, d4 = st.columns(2)
        academic_level = d3.selectbox("Academic level", ["High School", "Undergraduate", "Graduate"], index=1)
        country = d4.selectbox("Country", config.COUNTRY_OPTIONS, index=config.COUNTRY_OPTIONS.index("USA"))

        st.markdown('<span class="mp-eyebrow">Social media habits</span>', unsafe_allow_html=True)
        platform = st.selectbox(
            "Most-used platform",
            ["Instagram", "TikTok", "YouTube", "Facebook", "Snapchat", "Twitter",
             "WhatsApp", "LinkedIn", "WeChat", "LINE", "KakaoTalk", "VKontakte"],
        )
        purpose = st.selectbox("Primary purpose of use", ["Entertainment", "Networking", "Education", "News"])
        u1, u2 = st.columns(2)
        usage_hours = u1.slider("Avg. daily usage (hrs)", 0.0, 12.0, 4.0, 0.1)
        unlocks = u2.slider("Daily phone unlocks", 20, 300, 120, 1)

        st.markdown('<span class="mp-eyebrow">Lifestyle</span>', unsafe_allow_html=True)
        l1, l2 = st.columns(2)
        study_hours = l1.slider("Study hours / day", 0.0, 10.0, 3.0, 0.1)
        activity_hours = l2.slider("Physical activity (hrs/day)", 0.0, 5.0, 1.5, 0.1)
        l3, l4 = st.columns(2)
        sleep_hours = l3.slider("Sleep (hrs/night)", 3.0, 11.0, 7.0, 0.1)
        stress_level = l4.selectbox("Self-rated stress level", config.STRESS_LEVELS, index=1)

        submitted = st.form_submit_button("Score this profile", use_container_width=True)

with right:
    if not submitted:
        st.markdown(
            '<div class="mp-card" style="text-align:center;padding:3.5rem 1.5rem;">'
            '<h4>Waiting on a profile</h4>'
            '<p>Fill in the form and select <b>Score this profile</b> — '
            'the predicted score, its band, and a plain-language read-out '
            'will appear here.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        inputs = {
            "Age": age, "Gender": gender, "Academic_Level": academic_level, "Country": country,
            "Most_Used_Platform": platform, "Purpose_Of_Use": purpose,
            "Avg_Daily_Usage_Hours": usage_hours, "Daily_Unlocks": unlocks,
            "Study_Hours": study_hours, "Physical_Activity_Hours": activity_hours,
            "Sleep_Hours_Per_Night": sleep_hours, "Stress_Level": stress_level,
        }
        row = build_model_row(inputs)
        score = predict_one(row)
        score = max(0.0, min(10.0, score))
        band_label, band_color = score_band(score)

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=round(score, 2),
                number={"suffix": " / 10", "font": {"family": config.FONT_MONO, "size": 44, "color": config.COLOR_INK}},
                gauge={
                    "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": config.COLOR_LINE},
                    "bar": {"color": band_color, "thickness": 0.28},
                    "bgcolor": "white",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 4.5], "color": "#FBEBE6"},
                        {"range": [4.5, 6.0], "color": "#FCF2E1"},
                        {"range": [6.0, 7.5], "color": "#E4EEEA"},
                        {"range": [7.5, 10], "color": "#E1EEE7"},
                    ],
                },
            )
        )
        gauge.update_layout(
            height=260, margin=dict(l=20, r=20, t=30, b=10),
            paper_bgcolor="rgba(0,0,0,0)", font_family=config.FONT_BODY,
        )
        st.plotly_chart(gauge, use_container_width=True)

        st.markdown(
            f'<div class="mp-card" style="text-align:center;">'
            f'<span class="mp-chip" style="background:{band_color}22;color:{band_color};">{band_label.upper()}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.write("")
        cohort_mean = df["Mental_Health_Score"].mean()
        delta = score - cohort_mean
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted score", f"{score:.2f}")
        m2.metric("Vs. cohort average", f"{delta:+.2f}")
        m3.metric("Productive hours/day", f"{study_hours + activity_hours:.1f}")

        st.write("")
        notes = []
        if usage_hours >= 6:
            notes.append("Daily usage is high relative to the cohort — usage above ~6h/day tracks with lower scores in this dataset.")
        if sleep_hours < 6:
            notes.append("Sleep is under 6 hours — short sleep is one of the strongest downward signals in the model.")
        if stress_level in ("High", "Very High"):
            notes.append(f"Self-rated stress is **{stress_level}**, which the model weights heavily toward a lower score.")
        if activity_hours < 1:
            notes.append("Physical activity is under 1 hour/day — low activity pairs with lower predicted scores here.")
        if not notes:
            notes.append("This profile's habits fall in ranges the model associates with stable, mid-to-high scores.")

        st.markdown('<span class="mp-eyebrow">What is driving this number</span>', unsafe_allow_html=True)
        for n in notes:
            st.markdown(f"- {n}")

        append_history(
            {
                **{k: inputs[k] for k in ["Age", "Gender", "Academic_Level", "Country", "Most_Used_Platform",
                                            "Purpose_Of_Use", "Avg_Daily_Usage_Hours", "Daily_Unlocks",
                                            "Study_Hours", "Physical_Activity_Hours", "Sleep_Hours_Per_Night",
                                            "Stress_Level"]},
                "Predicted_Mental_Health_Score": round(score, 3),
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
            }
        )

st.write("")
st.write("")
st.markdown('<span class="mp-eyebrow">Batch scoring</span>', unsafe_allow_html=True)
st.caption(
    "Upload a CSV with columns: " + ", ".join(
        ["Age", "Gender", "Academic_Level", "Country", "Most_Used_Platform", "Purpose_Of_Use",
         "Avg_Daily_Usage_Hours", "Daily_Unlocks", "Study_Hours", "Physical_Activity_Hours",
         "Sleep_Hours_Per_Night", "Stress_Level"]
    )
)
upload = st.file_uploader("Upload student profiles", type=["csv"], label_visibility="collapsed")
if upload is not None:
    from utils.engineer import add_engineered_features, add_grouped_country
    from utils.model import predict_batch

    batch = pd.read_csv(upload)
    required = ["Age", "Gender", "Academic_Level", "Country", "Most_Used_Platform", "Purpose_Of_Use",
                "Avg_Daily_Usage_Hours", "Daily_Unlocks", "Study_Hours", "Physical_Activity_Hours",
                "Sleep_Hours_Per_Night", "Stress_Level"]
    missing = [c for c in required if c not in batch.columns]
    if missing:
        st.error(f"Missing required column(s): {', '.join(missing)}")
    else:
        batch = add_grouped_country(batch, source_col="Country")
        batch = add_engineered_features(batch)
        batch["Predicted_Mental_Health_Score"] = predict_batch(batch).round(3)
        st.success(f"Scored {len(batch):,} rows.")
        st.dataframe(batch.drop(columns=["Grouped_country", "Productive_Hours", "Lifestyle_Balance"]), use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download scored CSV",
            batch.drop(columns=["Grouped_country", "Productive_Hours", "Lifestyle_Balance"]).to_csv(index=False),
            file_name="mindpulse_batch_predictions.csv",
            mime="text/csv",
        )

from utils.data import load_history
hist_df = load_history()
if not hist_df.empty:
    st.write("")
    st.markdown('<span class="mp-eyebrow">This session\'s prediction log</span>', unsafe_allow_html=True)
    st.dataframe(hist_df.tail(10), use_container_width=True, hide_index=True)
