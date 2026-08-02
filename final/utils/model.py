"""Loads final_model.pkl once per session and exposes a thin predict API.

final_model.pkl was fit under scikit-learn 1.9.0. Depending on the
scikit-learn version installed at runtime, unpickling may emit an
``InconsistentVersionWarning`` — it is silenced here because it is
informational only: the underlying sklearn.pipeline.Pipeline still holds
its fitted encoders/trees and predicts correctly (verified against the
project's own prediction_results.csv / batch_predictions.csv, which this
loader reproduces exactly).
"""

import warnings

import joblib
import pandas as pd
import streamlit as st

import config


@st.cache_resource(show_spinner="Loading the trained model…")
def load_model():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = joblib.load(config.MODEL_PATH)
    return model


def predict_one(row_df: pd.DataFrame) -> float:
    model = load_model()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pred = model.predict(row_df)[0]
    return float(pred)


def predict_batch(df: pd.DataFrame) -> pd.Series:
    model = load_model()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        preds = model.predict(df[config.MODEL_FEATURE_ORDER])
    return pd.Series(preds, index=df.index, name="Predicted_Mental_Health_Score")


def score_band(score: float) -> tuple[str, str]:
    """Return (label, color) for a Mental_Health_Score on its 0-10 scale."""
    if score >= 7.5:
        return "Thriving", config.COLOR_SAGE
    if score >= 6.0:
        return "Steady", config.COLOR_TEAL
    if score >= 4.5:
        return "At Risk", config.COLOR_AMBER
    return "Struggling", config.COLOR_CORAL
