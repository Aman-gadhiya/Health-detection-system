"""Model Insights — feature importance and held-out evaluation of final_model.pkl."""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import config
from utils.data import load_dataset
from utils.model import load_model
from utils.theme import inject_css, masthead

st.set_page_config(
    page_title=f"Model Insights · {config.APP_NAME}",
    page_icon="📈",
    layout=config.LAYOUT,
)
inject_css()

with st.sidebar:
    st.markdown(f"### {config.PAGE_ICON} {config.APP_NAME}")
    st.caption(config.APP_TAGLINE)

df = load_dataset()
model = load_model()

masthead("Model Insights", "What the model actually learned.", "final_model.pkl is a scikit-learn Pipeline: a ColumnTransformer (log+scale, ordinal, one-hot) feeding an ExtraTreesRegressor with 300 trees.")

# ---------------------------------------------------------------------------
# Feature contract card
# ---------------------------------------------------------------------------

st.markdown('<span class="mp-eyebrow">Feature contract</span>', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.markdown(
        '<div class="mp-card"><h4>Numeric</h4><p>Age, Avg_Daily_Usage_Hours, Daily_Unlocks, '
        'Study_Hours, Physical_Activity_Hours, Sleep_Hours_Per_Night — standardized. '
        'Study_Hours is additionally log(1+x)-transformed to correct right-skew.</p></div>',
        unsafe_allow_html=True,
    )
with fc2:
    st.markdown(
        '<div class="mp-card"><h4>Engineered</h4><p><b>Productive_Hours</b> = Study_Hours + '
        'Physical_Activity_Hours.<br><b>Lifestyle_Balance</b> = Sleep_Hours_Per_Night − '
        'Avg_Daily_Usage_Hours.</p></div>',
        unsafe_allow_html=True,
    )
with fc3:
    st.markdown(
        '<div class="mp-card"><h4>Categorical</h4><p>Stress_Level (ordinal, Low→Very High), '
        'Gender, Academic_Level, Most_Used_Platform, Purpose_Of_Use, Grouped_country — one-hot '
        'encoded (unseen categories fall back to "Other"-style zero vectors).</p></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Held-out evaluation (re-split from the same dataset the model was trained on)
# ---------------------------------------------------------------------------

st.markdown('<span class="mp-eyebrow">Held-out evaluation</span>', unsafe_allow_html=True)
st.caption(
    "Scored on an 80/20 split of the full dataset. Because the shipped model was already "
    "trained on this same file, this re-split almost certainly overlaps with its training "
    "rows — treat the numbers below as an upper bound on accuracy, not a true held-out test."
)

X = df[config.MODEL_FEATURE_ORDER]
y = df[config.TARGET_COLUMN]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
mae = mean_absolute_error(y_test, y_pred)

e1, e2, e3, e4 = st.columns(4)
e1.metric("R²", f"{r2:.3f}")
e2.metric("RMSE", f"{rmse:.3f}")
e3.metric("MAE", f"{mae:.3f}")
e4.metric("Test rows", f"{len(X_test):,}")

st.write("")
ev1, ev2 = st.columns(2)

with ev1:
    st.markdown('<span class="mp-eyebrow">Predicted vs. actual</span>', unsafe_allow_html=True)
    scatter_df = pd.DataFrame({"Actual": y_test.values, "Predicted": y_pred})
    fig = px.scatter(scatter_df, x="Actual", y="Predicted", opacity=0.55, color_discrete_sequence=[config.COLOR_TEAL])
    lo, hi = float(y.min()), float(y.max())
    fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", line=dict(color=config.COLOR_CORAL, dash="dash"), name="Perfect prediction"))
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=360, showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

with ev2:
    st.markdown('<span class="mp-eyebrow">Residual distribution</span>', unsafe_allow_html=True)
    residuals = y_test.values - y_pred
    fig2 = px.histogram(residuals, nbins=30, color_discrete_sequence=[config.COLOR_SAGE])
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=360, showlegend=False,
        xaxis_title="Actual − Predicted", yaxis_title="Count",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------

st.write("")
st.markdown('<span class="mp-eyebrow">Feature importance (Gini, from the fitted trees)</span>', unsafe_allow_html=True)

try:
    pre = model.named_steps["preprocessor"]
    feature_names = pre.get_feature_names_out()
    importances = model.named_steps["model"].feature_importances_
    imp_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    imp_df["feature"] = imp_df["feature"].str.replace(r"^(Skewed|Numeric|Ordinal|Nominal)__", "", regex=True)
    imp_df = imp_df.groupby("feature", as_index=False)["importance"].sum()
    imp_df = imp_df.sort_values("importance", ascending=True).tail(15)

    fig3 = go.Figure(go.Bar(x=imp_df["importance"], y=imp_df["feature"], orientation="h", marker_color=config.COLOR_TEAL))
    fig3.update_layout(
        plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
        font_family=config.FONT_BODY, height=460,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Relative importance",
    )
    st.plotly_chart(fig3, use_container_width=True)
except Exception as e:
    st.info(f"Feature importance couldn't be extracted from this pipeline build ({e}).")

st.caption(
    "Importance is computed directly from the loaded final_model.pkl — nothing here is "
    "simulated or hard-coded."
)
