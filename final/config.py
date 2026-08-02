"""
===============================================================================
MindPulse — Student Social Media & Mental Health Analytics
-------------------------------------------------------------------------------
Central configuration. Every path is resolved relative to this file's
location, so the app runs the same way regardless of the working directory
it is launched from (local machine, Docker, or Streamlit Community Cloud).
===============================================================================
"""

from pathlib import Path

# =============================================================================
# BASE PATHS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "student_social_media_mental_health.csv"
MODEL_PATH = BASE_DIR / "models" / "final_model.pkl"
OUTPUTS_DIR = BASE_DIR / "outputs"
HISTORY_PATH = OUTPUTS_DIR / "prediction_history.csv"

OUTPUTS_DIR.mkdir(exist_ok=True)

# =============================================================================
# APPLICATION INFO
# =============================================================================

APP_NAME = "MindPulse"
APP_TAGLINE = "Student Social Media & Mental Health Analytics"
PAGE_ICON = "🧠"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"
VERSION = "1.0.0"

# =============================================================================
# MODEL FEATURE CONTRACT
# -------------------------------------------------------------------------------
# final_model.pkl is an sklearn Pipeline (ColumnTransformer + ExtraTreesRegressor,
# 300 trees) trained to predict Mental_Health_Score (0-10 self-reported scale)
# from the 14 columns below. Two of them — Productive_Hours and
# Lifestyle_Balance — are engineered at inference time, not collected directly.
# See utils/engineer.py for the exact formulas.
# =============================================================================

TARGET_COLUMN = "Mental_Health_Score"

RAW_NUMERIC_FEATURES = [
    "Age",
    "Avg_Daily_Usage_Hours",
    "Daily_Unlocks",
    "Study_Hours",
    "Physical_Activity_Hours",
    "Sleep_Hours_Per_Night",
]

ENGINEERED_FEATURES = ["Productive_Hours", "Lifestyle_Balance"]

CATEGORICAL_FEATURES = [
    "Stress_Level",
    "Gender",
    "Academic_Level",
    "Most_Used_Platform",
    "Purpose_Of_Use",
    "Grouped_country",
]

MODEL_FEATURE_ORDER = [
    "Study_Hours",
    "Age",
    "Avg_Daily_Usage_Hours",
    "Daily_Unlocks",
    "Physical_Activity_Hours",
    "Sleep_Hours_Per_Night",
    "Productive_Hours",
    "Lifestyle_Balance",
    "Stress_Level",
    "Gender",
    "Academic_Level",
    "Most_Used_Platform",
    "Purpose_Of_Use",
    "Grouped_country",
]

STRESS_LEVELS = ["Low", "Medium", "High", "Very High"]
TOP_COUNTRIES = [
    "India", "USA", "Canada", "Australia", "UK", "Germany", "Mexico",
    "Turkey", "France", "Spain", "Ireland", "Japan", "Denmark",
    "Switzerland", "Nepal",
]
COUNTRY_OPTIONS = TOP_COUNTRIES + ["Other"]

# =============================================================================
# DESIGN TOKENS
# -------------------------------------------------------------------------------
# A calm, clinical-but-warm palette built for a wellbeing subject: deep
# teal for trust/focus, sage for balance, amber/coral reserved strictly for
# rising stress signal — color itself carries meaning on the Predict page.
# =============================================================================

COLOR_INK = "#132623"          # near-black, warm-green undertone (headings)
COLOR_BG = "#F4F7F5"           # cool porcelain background
COLOR_SURFACE = "#FFFFFF"      # card surface
COLOR_TEAL = "#0F5257"         # primary — deep teal
COLOR_TEAL_SOFT = "#DCEAE8"    # teal tint for chips / highlights
COLOR_SAGE = "#6FA287"         # secondary — balance / good scores
COLOR_AMBER = "#E3A23D"        # caution — medium stress
COLOR_CORAL = "#DD6B54"        # alert — high stress
COLOR_LINE = "#D8E2DE"         # hairline borders

FONT_DISPLAY = "'Fraunces', serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"
