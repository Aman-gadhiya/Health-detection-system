"""Cached data access for the training dataset and prediction history."""

import pandas as pd
import streamlit as st

import config
from utils.engineer import add_engineered_features, add_grouped_country


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(config.DATA_PATH)
    df = add_grouped_country(df, source_col="Country")
    df = add_engineered_features(df)
    return df


def load_history() -> pd.DataFrame:
    if config.HISTORY_PATH.exists():
        return pd.read_csv(config.HISTORY_PATH)
    return pd.DataFrame(
        columns=config.MODEL_FEATURE_ORDER + ["Country", "Predicted_Mental_Health_Score", "Timestamp"]
    )


def append_history(row: dict) -> None:
    history = load_history()
    history = pd.concat([history, pd.DataFrame([row])], ignore_index=True)
    history.to_csv(config.HISTORY_PATH, index=False)
