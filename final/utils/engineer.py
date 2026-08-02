"""
Feature engineering — reproduces exactly the two derived columns the
training pipeline was fit on, plus the country-grouping rule, so that
live predictions see the same feature contract as final_model.pkl.

    Productive_Hours   = Study_Hours + Physical_Activity_Hours
    Lifestyle_Balance  = Sleep_Hours_Per_Night - Avg_Daily_Usage_Hours
    Grouped_country    = Country if Country in the top-15 training
                          countries, else "Other"

(Verified by reproducing batch_predictions.csv row-for-row from the
 original project bundle.)
"""

import pandas as pd

import config


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add Productive_Hours and Lifestyle_Balance to a copy of df."""
    out = df.copy()
    out["Productive_Hours"] = out["Study_Hours"] + out["Physical_Activity_Hours"]
    out["Lifestyle_Balance"] = out["Sleep_Hours_Per_Night"] - out["Avg_Daily_Usage_Hours"]
    return out


def group_country(country: str) -> str:
    return country if country in config.TOP_COUNTRIES else "Other"


def add_grouped_country(df: pd.DataFrame, source_col: str = "Country") -> pd.DataFrame:
    out = df.copy()
    if source_col in out.columns:
        out["Grouped_country"] = out[source_col].apply(group_country)
    return out


def build_model_row(inputs: dict) -> pd.DataFrame:
    """Turn a dict of raw form inputs into the single-row, correctly
    ordered DataFrame the pipeline expects."""
    row = dict(inputs)
    row["Productive_Hours"] = row["Study_Hours"] + row["Physical_Activity_Hours"]
    row["Lifestyle_Balance"] = row["Sleep_Hours_Per_Night"] - row["Avg_Daily_Usage_Hours"]
    row["Grouped_country"] = group_country(row.pop("Country"))
    return pd.DataFrame([row])[config.MODEL_FEATURE_ORDER]
