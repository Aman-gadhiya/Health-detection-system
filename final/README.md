# 🧠 MindPulse — Student Social Media & Mental Health Analytics

A self-contained, ready-to-run Streamlit app built around a real trained
model (`models/final_model.pkl`, an ExtraTreesRegressor pipeline) and a
real dataset (`data/student_social_media_mental_health.csv`, 5,000
student self-reports). Nothing needs to be edited or reconfigured — the
model and data ship inside the project.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Pages

| Page | What it does |
|---|---|
| **Home** | Cohort-level headline stats and navigation |
| **Data Explorer** | Filter the dataset by country, platform, stress level, academic level, age; charts update live |
| **Predict** | Score a single student profile through the real model, with a gauge, a plain-language read-out, and CSV batch scoring |
| **Model Insights** | Held-out R²/RMSE/MAE, predicted-vs-actual plot, residuals, and Gini feature importance — all computed from the loaded `.pkl`, live |
| **About** | Data dictionary and project layout |

## What the model predicts

`Mental_Health_Score`, a self-reported wellbeing score from 0–10, from 14
features — 6 raw numeric columns, 2 engineered columns computed at
inference time, and 6 categorical columns. The exact contract is defined
once in `config.py` and `utils/engineer.py` so every page (single predict,
batch predict, and the evaluation on Model Insights) uses the same logic.

```
Productive_Hours   = Study_Hours + Physical_Activity_Hours
Lifestyle_Balance  = Sleep_Hours_Per_Night - Avg_Daily_Usage_Hours
Grouped_country    = Country if it's one of the top-15 training countries,
                      else "Other"
```

## Project structure

```
mental_health_app/
├── app.py                    # Home dashboard (entry point)
├── config.py                 # Paths, feature contract, design tokens
├── requirements.txt
├── .streamlit/config.toml    # Streamlit theme
├── data/
│   └── student_social_media_mental_health.csv
├── models/
│   └── final_model.pkl       # sklearn Pipeline: preprocessor + ExtraTreesRegressor
├── outputs/
│   └── prediction_history.csv   # created at runtime by the Predict page
├── pages/
│   ├── 1_Data_Explorer.py
│   ├── 2_Predict.py
│   ├── 3_Model_Insights.py
│   └── 4_About.py
└── utils/
    ├── data.py                # cached dataset + prediction-history I/O
    ├── engineer.py            # feature engineering (single source of truth)
    ├── model.py                # model loading + prediction helpers
    └── theme.py                # CSS + design system
```

## Notes

- `final_model.pkl` was originally saved under scikit-learn 1.9.0. If your
  installed scikit-learn is a different minor version, you may see an
  `InconsistentVersionWarning` on first load — this is expected, is
  silenced in `utils/model.py`, and does not affect prediction correctness
  (verified against the original project's own prediction logs).
- The two files that shipped in the source bundle under a "salary
  prediction" name (`app.py`'s old scaffold and
  `models/best_salary_prediction_pipeline.pkl`) were leftovers from an
  unrelated template — `best_salary_prediction_pipeline.pkl` is a
  byte-for-byte duplicate of `final_model.pkl`, and this project uses the
  correctly-named copy only.
