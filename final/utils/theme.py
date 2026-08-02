"""Injects the app's visual identity: fonts, palette, card system, and the
signature 'pulse' rule motif used across page headers."""

import streamlit as st

import config


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: {config.FONT_BODY};
            color: {config.COLOR_INK};
        }}

        .stApp {{
            background: {config.COLOR_BG};
        }}

        h1, h2, h3 {{
            font-family: {config.FONT_DISPLAY};
            font-weight: 600;
            color: {config.COLOR_INK};
            letter-spacing: -0.01em;
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background: {config.COLOR_INK};
        }}
        section[data-testid="stSidebar"] * {{
            color: #EAF3F0 !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown p {{
            color: #9FC3BA !important;
        }}

        /* ---- Signature masthead rule ---- */
        .mp-masthead {{
            display: flex;
            align-items: baseline;
            gap: 0.85rem;
            margin-bottom: 0.15rem;
        }}
        .mp-masthead .pulse {{
            font-family: {config.FONT_MONO};
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            color: {config.COLOR_TEAL};
            text-transform: uppercase;
        }}
        .mp-rule {{
            height: 3px;
            background: linear-gradient(90deg, {config.COLOR_TEAL} 0%, {config.COLOR_SAGE} 45%, {config.COLOR_AMBER} 75%, {config.COLOR_CORAL} 100%);
            border-radius: 2px;
            margin: 0.35rem 0 1.6rem 0;
            width: 100%;
        }}
        .mp-eyebrow {{
            font-family: {config.FONT_MONO};
            font-size: 0.72rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: {config.COLOR_TEAL};
            margin-bottom: 0.3rem;
        }}

        /* ---- Cards ---- */
        .mp-card {{
            background: {config.COLOR_SURFACE};
            border: 1px solid {config.COLOR_LINE};
            border-radius: 14px;
            padding: 1.35rem 1.5rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            transition: all 0.25s ease;
        }}
        .mp-card h4 {{
            font-family: {config.FONT_DISPLAY};
            margin: 0 0 0.35rem 0;
            font-size: 1.05rem;
        }}
        .mp-card p {{
            color: #4B5F5A;
            font-size: 0.9rem;
            margin: 0;
            line-height: 1.5;
        }}

        .mp-stat {{
            font-family: {config.FONT_MONO};
            font-size: 2.1rem;
            font-weight: 500;
            color: {config.COLOR_TEAL};
            line-height: 1.1;
        }}
        .mp-stat-label {{
            font-size: 0.78rem;
            color: #5E7570;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.2rem;
        }}

        .mp-chip {{
            display: inline-block;
            font-family: {config.FONT_MONO};
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            background: {config.COLOR_TEAL_SOFT};
            color: {config.COLOR_TEAL};
            letter-spacing: 0.04em;
        }}

        /* ---- Buttons ---- */
        .stButton > button, .stFormSubmitButton > button {{
            background: {config.COLOR_TEAL};
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.55rem 1.4rem;
            font-weight: 600;
            transition: transform 0.08s ease, background 0.15s ease;
        }}
        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            background: #0C4247;
            transform: translateY(-1px);
        }}

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab"] {{
            font-family: {config.FONT_BODY};
            font-weight: 600;
        }}

        /* ---- Metric widgets ---- */
        div[data-testid="stMetric"] {{
            background: {config.COLOR_SURFACE};
            border: 1px solid {config.COLOR_LINE};
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
        }}

        footer {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def masthead(eyebrow: str, title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="mp-masthead">
            <span class="pulse">◍ MINDPULSE</span>
            <span class="mp-eyebrow">{eyebrow}</span>
        </div>
        <h1 style="margin-bottom:0.1rem;">{title}</h1>
        {f'<p style="color:#4B5F5A;font-size:1.02rem;max-width:60ch;">{subtitle}</p>' if subtitle else ''}
        <div class="mp-rule"></div>
        """,
        unsafe_allow_html=True,
    )
