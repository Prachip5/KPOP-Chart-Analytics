
import html
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="K-Pop Chart Analytics",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

C = {
    "navy": "#111329",
    "navy_2": "#171936",
    "purple_dark": "#44206A",
    "purple": "#6D35B1",
    "purple_mid": "#8A52D1",
    "purple_light": "#B68AE8",
    "lavender": "#EEE7F8",
    "bg": "#F7F4FB",
    "surface": "#FFFFFF",
    "line": "#E4DDF0",
    "text": "#17152A",
    "muted": "#6D6680",
    "white": "#FFFFFF",
}

SCALE = [
    [0.00, "#E7D9F6"],
    [0.25, "#C9A9EA"],
    [0.50, "#A475DA"],
    [0.75, "#8148C2"],
    [1.00, "#5B238E"],
]


# ============================================================
# CSS
# ============================================================

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --navy: #111329;
    --navy2: #171936;
    --purple: #6D35B1;
    --purple2: #8A52D1;
    --lavender: #EEE7F8;
    --bg: #F7F4FB;
    --surface: #FFFFFF;
    --line: #E4DDF0;
    --text: #17152A;
    --muted: #6D6680;
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: "DM Sans", sans-serif;
}

body {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stAppViewContainer"] {
    background: var(--bg);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding: 1.4rem 2.0rem 2.5rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101226 0%, #171936 100%) !important;
    border-right: 1px solid #292B4D !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.3rem 1rem 2rem !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}

.sidebar-brand {
    text-align: center;
    padding: 12px 4px 22px;
}

.brand-title {
    color: #FFFFFF;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: .01em;
}

.brand-sub {
    color: #C9C4DB;
    font-size: .67rem;
    letter-spacing: .17em;
    font-weight: 700;
    margin-top: 6px;
}

.nav-caption,
.sidebar-label {
    color: #AAA5C1 !important;
    font-size: .67rem !important;
    font-weight: 800 !important;
    letter-spacing: .13em;
    text-transform: uppercase;
}

.sidebar-divider {
    height: 1px;
    background: #343650;
    margin: 14px 0 18px;
}

section[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 5px !important;
}

section[data-testid="stSidebar"] .stRadio [role="radio"] {
    min-height: 40px !important;
    padding: 0 12px !important;
    border-radius: 9px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #F6F4FB !important;
}

section[data-testid="stSidebar"] .stRadio [role="radio"] * {
    color: #F6F4FB !important;
}

section[data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"] {
    background: linear-gradient(90deg, #7B3FC6, #6A32AD) !important;
    border-color: #925BD6 !important;
    box-shadow: 0 8px 20px rgba(93, 43, 145, .25);
}

section[data-testid="stSidebar"] .stMultiSelect > div,
section[data-testid="stSidebar"] .stSelectbox > div {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #15172E !important;
    border: 1px solid #4A4D70 !important;
    border-radius: 9px !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] label {
    color: #FFFFFF !important;
}

.sidebar-note {
    color: #BDB7CF;
    font-size: .78rem;
    line-height: 1.55;
    margin-top: 22px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 0 0 26px 26px;
    min-height: 205px;
    padding: 38px 42px;
    color: white;
    background:
        radial-gradient(circle at 82% 18%, rgba(208,164,255,.30), transparent 24%),
        radial-gradient(circle at 66% 80%, rgba(146,74,215,.28), transparent 35%),
        linear-gradient(105deg, #3E1B5B 0%, #6A35A1 55%, #8B50D0 100%);
    box-shadow: 0 18px 35px rgba(74, 37, 103, .18);
}

.hero:after {
    content: "";
    position: absolute;
    width: 390px;
    height: 390px;
    right: -110px;
    top: -225px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,.18);
    box-shadow:
        0 0 0 48px rgba(255,255,255,.035),
        0 0 0 98px rgba(255,255,255,.025);
}

.hero-kicker {
    position: relative;
    z-index: 2;
    font-size: .72rem;
    letter-spacing: .18em;
    font-weight: 800;
    text-transform: uppercase;
}

.hero-title {
    position: relative;
    z-index: 2;
    margin-top: 9px;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.4rem);
    line-height: 1.02;
    font-weight: 800;
    letter-spacing: -.035em;
}

.hero-title span {
    color: #D4AEFF;
}

.hero-subtitle {
    position: relative;
    z-index: 2;
    max-width: 780px;
    margin-top: 12px;
    font-size: .98rem;
    line-height: 1.55;
    color: #F6F0FF;
}

/* Section */
.section-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    margin: 24px 0 11px;
}

.section-title {
    color: var(--text);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.08rem;
    font-weight: 800;
}

.section-note {
    color: var(--muted);
    font-size: .72rem;
}

/* KPI */
.kpi {
    min-height: 92px;
    background: white;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 17px 18px;
    box-shadow: 0 5px 18px rgba(48, 32, 73, .055);
}

.kpi-value {
    color: var(--text);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.55rem;
    line-height: 1.1;
    font-weight: 800;
}

.kpi-label {
    margin-top: 7px;
    color: var(--muted);
    font-size: .76rem;
}

/* Album cards */
.song-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 5px 18px rgba(48, 32, 73, .055);
}

.song-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
    display: block;
    background: linear-gradient(135deg, #E9DDF5, #D6C0EC);
}

.song-placeholder {
    width: 100%;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #E9DDF5, #D6C0EC);
    color: #7441A8;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
}

.song-info {
    position: relative;
    padding: 14px 14px 13px;
}

.rank {
    position: absolute;
    top: -19px;
    left: 12px;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6B25A9, #9148D2);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: .82rem;
    box-shadow: 0 5px 12px rgba(90, 35, 142, .30);
}

.song-name {
    margin-top: 5px;
    color: var(--text);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: .94rem;
    font-weight: 800;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.song-artist {
    margin-top: 4px;
    color: #57516A;
    font-size: .73rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.score-row {
    display: flex;
    justify-content: space-between;
    margin-top: 13px;
    font-size: .67rem;
}

.score-label { color: #8A8398; }
.score-value { color: #6330A2; font-weight: 800; }

.score-track {
    height: 5px;
    margin-top: 7px;
    background: #E6DDF1;
    border-radius: 99px;
    overflow: hidden;
}

.score-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #5D2795, #9759D9);
}

/* Chart cards */
.chart-card {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 12px 12px 8px;
    box-shadow: 0 5px 18px rgba(48, 32, 73, .045);
}

.chart-heading {
    color: var(--text);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: .98rem;
    font-weight: 800;
    padding: 5px 8px 0;
}

/* Insight cards */
.info-card {
    height: 100%;
    background: white;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 17px 18px;
}

.info-title {
    color: var(--text);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: .9rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.info-text, .info-card li {
    color: #5D576D;
    font-size: .77rem;
    line-height: 1.6;
}

/* Native Streamlit cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    box-shadow: 0 5px 18px rgba(48, 32, 73, .045);
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: 14px !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    border: 1px solid #D8C9EA !important;
    background: #F3ECFB !important;
    color: #5A278F !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
}

.stDownloadButton > button {
    border-radius: 9px !important;
    border: 1px solid #D8C9EA !important;
}

/* Selects on main page */
[data-baseweb="select"] > div {
    border-radius: 9px !important;
}

/* Mobile */
@media (max-width: 900px) {
    .block-container {
        padding: 1rem !important;
    }

    .hero {
        padding: 28px 24px;
    }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# PROJECT PATHS
# ============================================================

THIS_DIR = Path(__file__).resolve().parent

# This file is intended to live in project/dashboard/app.py.
PROJECT_ROOT = THIS_DIR.parent if THIS_DIR.name.lower() == "dashboard" else THIS_DIR

SEARCH_DIRS = [
    THIS_DIR,
    PROJECT_ROOT,
    PROJECT_ROOT / "outputs",
    PROJECT_ROOT / "data",
    PROJECT_ROOT / "data" / "processed",
    PROJECT_ROOT / "dashboard",
    PROJECT_ROOT / "dashboard" / "assets",
]

# De-duplicate paths while preserving order.
SEARCH_DIRS = list(dict.fromkeys(p.resolve() for p in SEARCH_DIRS if p.exists()))


def find_file(filename):
    for directory in SEARCH_DIRS:
        candidate = directory / filename
        if candidate.exists():
            return candidate
    return None


@st.cache_data(show_spinner=False)
def read_csv_file(path_string):
    if not path_string:
        return None
    try:
        return pd.read_csv(path_string)
    except Exception:
        return None


def load_csv(filename):
    path = find_file(filename)
    return read_csv_file(str(path)) if path else None


# ============================================================
# DATA
# ============================================================

integrated = load_csv("phase7_integrated_kpop_analysis.csv")
if integrated is None:
    integrated = load_csv("KPOP_FINAL_DASHBOARD_DATA.csv")

momentum = load_csv("phase4_comeback_momentum_events.csv")
fandom = load_csv("phase5_fandom_intensity_song_analysis.csv")
sustainability = load_csv("phase6_chart_sustainability_analysis.csv")
artist_sustainability = load_csv("phase6_artist_sustainability_analysis.csv")

cleaned = load_csv("Atlantic_South_Korea_Cleaned.csv")
raw = load_csv("Atlantic_South_Korea.csv")


def make_numeric(df, columns):
    if df is None:
        return
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


NUMERIC_COLUMNS = [
    "overall_performance_score",
    "average_momentum_score",
    "fandom_intensity_score",
    "sustainability_score",
    "total_reentries",
    "average_gap_days",
    "longest_gap_days",
    "best_reentry_position",
    "average_reentry_position",
    "gap_days",
    "reentry_position",
    "momentum_score",
    "fandom_score",
]

for frame in [
    integrated,
    momentum,
    fandom,
    sustainability,
    artist_sustainability,
    cleaned,
    raw,
]:
    make_numeric(frame, NUMERIC_COLUMNS)


# ============================================================
# HELPERS
# ============================================================

def normalize(value):
    value = "" if value is None else str(value)
    value = value.lower().strip()
    value = re.sub(r"[\(\)\[\]\{\}:,'\".!?]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def fmt(value, decimals=1):
    if value is None:
        return "—"
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.{decimals}f}"
    except Exception:
        return str(value)


def first_existing(df, candidates):
    if df is None:
        return None
    for col in candidates:
        if col in df.columns:
            return col
    return None


def apply_filters(df, selected_artists, selected_categories):
    if df is None:
        return None

    result = df.copy()

    if selected_artists and "artist" in result.columns:
        result = result[
            result["artist"].astype(str).isin([str(x) for x in selected_artists])
        ]

    if selected_categories and "fandom_category" in result.columns:
        result = result[
            result["fandom_category"].astype(str).isin(
                [str(x) for x in selected_categories]
            )
        ]

    return result


def section(title, note=""):
    note_html = (
        f'<span class="section-note">{html.escape(str(note))}</span>'
        if note else ""
    )
    markup = (
        '<div class="section-row">'
        f'<div class="section-title">{html.escape(str(title))}</div>'
        f'{note_html}'
        '</div>'
    )
    st.markdown(markup, unsafe_allow_html=True)


def page_header(kicker, title, subtitle):
    title_html = html.escape(str(title))
    subtitle_html = html.escape(str(subtitle))
    kicker_html = html.escape(str(kicker))

    markup = (
        '<div class="hero">'
        f'<div class="hero-kicker">{kicker_html}</div>'
        f'<div class="hero-title">K-Pop Chart <span>Analytics</span></div>'
        f'<div class="hero-subtitle">{subtitle_html}</div>'
        '</div>'
    )
    st.markdown(markup, unsafe_allow_html=True)


def kpi(value, label):
    return (
        '<div class="kpi">'
        f'<div class="kpi-value">{html.escape(str(value))}</div>'
        f'<div class="kpi-label">{html.escape(str(label))}</div>'
        '</div>'
    )


def show_kpis(items):
    cols = st.columns(len(items))
    for col, (value, label) in zip(cols, items):
        with col:
            st.markdown(kpi(value, label), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_cover(song, artist):
    song_key = normalize(song)
    artist_key = normalize(artist)

    # Local project CSVs.
    for data in (cleaned, raw):
        if data is None or data.empty or "song" not in data.columns:
            continue

        cover_col = first_existing(
            data,
            [
                "album_cover_url",
                "album_art_url",
                "cover_url",
                "image_url",
                "album_cover",
                "cover",
            ],
        )

        if not cover_col:
            continue

        work = data.copy()
        work["_song_key"] = work["song"].fillna("").astype(str).map(normalize)

        matches = work[work["_song_key"] == song_key]

        if "artist" in work.columns and not matches.empty:
            artist_matches = matches[
                matches["artist"].fillna("").astype(str).map(normalize) == artist_key
            ]
            if not artist_matches.empty:
                matches = artist_matches

        for value in matches[cover_col].dropna().astype(str):
            value = value.strip()
            if value.startswith(("http://", "https://")):
                return value

    # Online fallback.
    try:
        query = quote(f"{song} {artist}")
        url = (
            "https://itunes.apple.com/search"
            f"?term={query}&entity=song&limit=8"
        )

        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))

        results = payload.get("results", [])

        for item in results:
            result_song = normalize(item.get("trackName", ""))
            result_artist = normalize(item.get("artistName", ""))

            song_match = (
                song_key == result_song
                or song_key in result_song
                or result_song in song_key
            )
            artist_match = (
                artist_key == result_artist
                or artist_key in result_artist
                or result_artist in artist_key
            )

            if song_match and artist_match:
                artwork = item.get("artworkUrl100") or item.get("artworkUrl60")
                if artwork:
                    return (
                        artwork
                        .replace("100x100", "600x600")
                        .replace("60x60", "600x600")
                    )

        if results:
            artwork = (
                results[0].get("artworkUrl100")
                or results[0].get("artworkUrl60")
            )
            if artwork:
                return (
                    artwork
                    .replace("100x100", "600x600")
                    .replace("60x60", "600x600")
                )

    except Exception:
        pass

    return ""


def render_song_card(rank, song, artist, score):
    cover = get_cover(song, artist)

    with st.container(border=True):
        if cover:
            st.image(cover, width="stretch")
        else:
            st.markdown(
                '<div class="song-placeholder">K</div>',
                unsafe_allow_html=True,
            )

        safe_song = html.escape(str(song))
        safe_artist = html.escape(str(artist))

        try:
            score_value = float(score)
            percentage = score_value * 100 if score_value <= 1.2 else score_value
            percentage = max(0, min(100, percentage))
        except Exception:
            percentage = 0

        st.markdown(
            '<div class="song-info">'
            f'<div class="rank">{rank}</div>'
            f'<div class="song-name">{safe_song}</div>'
            f'<div class="song-artist">{safe_artist}</div>'
            '<div class="score-row">'
            '<span class="score-label">Integrated score</span>'
            f'<span class="score-value">{fmt(score, 3)}</span>'
            '</div>'
            '<div class="score-track">'
            f'<div class="score-fill" style="width:{percentage:.0f}%"></div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def style_chart(fig, height=350):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=12, b=12),
        title=dict(text=""),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=C["text"], size=11),
        showlegend=False,
        coloraxis_colorbar=dict(
            thickness=11,
            outlinewidth=0,
            tickfont=dict(size=9),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_family="DM Sans",
            font_size=11,
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#ECE8F1",
        zeroline=False,
        linecolor="#E6E0EB",
        title_font=dict(size=10),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#ECE8F1",
        zeroline=False,
        linecolor="#E6E0EB",
        title_font=dict(size=10),
    )

    return fig


def chart_card_title(title, note=""):
    note_html = (
        f'<span class="section-note">{html.escape(note)}</span>'
        if note else ""
    )
    st.markdown(
        '<div class="chart-heading">'
        f'{html.escape(title)}'
        f'{note_html}'
        '</div>',
        unsafe_allow_html=True,
    )


def show_chart(fig, height=350):
    st.plotly_chart(
        style_chart(fig, height),
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="brand-title">K-POP ANALYTICS</div>'
        '<div class="brand-sub">SOUTH KOREA TOP 50</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    pages = [
        "Home",
        "Top Songs",
        "Comeback Momentum",
        "Fandom Intensity",
        "Sustainability",
        "Artist Analysis",
        "Song Explorer",
        "About Project",
    ]

    page = st.radio(
        "Navigation",
        pages,
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-caption">Filters</div>', unsafe_allow_html=True)

    artist_options = []
    if integrated is not None and "artist" in integrated.columns:
        artist_options = sorted(
            integrated["artist"].dropna().astype(str).unique().tolist()
        )

    category_options = []
    if integrated is not None and "fandom_category" in integrated.columns:
        category_options = sorted(
            integrated["fandom_category"].dropna().astype(str).unique().tolist()
        )

    st.markdown('<div class="sidebar-label">Artist</div>', unsafe_allow_html=True)
    selected_artists = st.multiselect(
        "Artist filter",
        artist_options,
        label_visibility="collapsed",
    )

    if category_options:
        st.markdown(
            '<div class="sidebar-label" style="margin-top:14px;">Category</div>',
            unsafe_allow_html=True,
        )
        selected_categories = st.multiselect(
            "Category filter",
            category_options,
            label_visibility="collapsed",
        )
    else:
        selected_categories = []

    st.markdown(
        '<div class="sidebar-label" style="margin-top:14px;">Ranking size</div>',
        unsafe_allow_html=True,
    )
    ranking_size = st.slider(
        "Ranking size",
        min_value=5,
        max_value=10,
        value=10,
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-divider"></div>'
        '<div class="sidebar-note">'
        'Scores are project-specific analytical indices derived from chart data. '
        'They are not direct measurements of fan count, audience size, or commercial success.'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HOME
# ============================================================

if page == "Home":
    page_header(
        "SOUTH KOREA TOP 50 · 2021 – 2026",
        "K-Pop Chart Analytics",
        "Comebacks, fandom intensity, sustainability and more — exploring the stories behind the charts.",
    )

    df = apply_filters(integrated, selected_artists, selected_categories)

    if df is None or df.empty:
        st.error(
            "Integrated data could not be loaded. Check the CSV filenames and project folder structure."
        )
        st.stop()

    songs_count = int(df["song"].nunique()) if "song" in df.columns else len(df)
    artists_count = int(df["artist"].nunique()) if "artist" in df.columns else 0

    if "total_reentries" in df.columns:
        reentries = int(pd.to_numeric(df["total_reentries"], errors="coerce").fillna(0).sum())
    elif momentum is not None:
        reentries = len(momentum)
    else:
        reentries = 0

    avg_gap = (
        pd.to_numeric(df["average_gap_days"], errors="coerce").mean()
        if "average_gap_days" in df.columns
        else np.nan
    )

    if "overall_performance_score" in df.columns and not df.empty:
        top_row = df.sort_values(
            "overall_performance_score",
            ascending=False,
        ).iloc[0]
        top_song = str(top_row.get("song", "—"))
    else:
        top_song = "—"

    show_kpis(
        [
            (f"{songs_count:,}", "Songs Analysed"),
            (f"{artists_count:,}", "Artists"),
            (f"{reentries:,}", "Re-entry Events"),
            (f"{fmt(avg_gap)}", "Average Gap (days)"),
            (top_song[:20], "Top Performer"),
        ]
    )

    section("Top 5 Performers", "Based on Integrated Performance Score")

    score_col = first_existing(df, ["overall_performance_score"])

    if score_col:
        top = df.sort_values(score_col, ascending=False).head(5)
        cards = st.columns(5)

        for i, (_, row) in enumerate(top.iterrows()):
            with cards[i]:
                render_song_card(
                    i + 1,
                    row.get("song", "Unknown"),
                    row.get("artist", "Unknown"),
                    row.get(score_col, np.nan),
                )

    st.write("")

    left, right = st.columns([1.08, 0.92], gap="medium")

    with left:
        with st.container(border=True):
            chart_card_title("Top 10 Songs by Overall Performance")

        if score_col:
            work = df.sort_values(score_col, ascending=False).head(10).copy()
            work["label"] = work["song"].astype(str)

            fig = px.bar(
                work.sort_values(score_col),
                x=score_col,
                y="label",
                orientation="h",
                color=score_col,
                color_continuous_scale=SCALE,
                text=score_col,
                hover_data=["artist"] if "artist" in work.columns else None,
            )
            fig.update_traces(
                texttemplate="%{text:.3f}",
                textposition="outside",
                cliponaxis=False,
                marker_line_width=0,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Overall Performance Score",
                yaxis_title="",
            )
            show_chart(fig, 365)
        else:
            st.info("Overall performance score is not available.")

    
    with right:
        with st.container(border=True):
            chart_card_title("Momentum vs Fandom Intensity", "Bubble size = sustainability")

        required = {"average_momentum_score", "fandom_intensity_score"}

        if required.issubset(df.columns):
            plot_df = df.copy()

            fig = px.scatter(
                plot_df,
                x="average_momentum_score",
                y="fandom_intensity_score",
                size="sustainability_score" if "sustainability_score" in plot_df.columns else None,
                color="sustainability_score" if "sustainability_score" in plot_df.columns else None,
                hover_name="song" if "song" in plot_df.columns else None,
                hover_data=["artist"] if "artist" in plot_df.columns else None,
                color_continuous_scale=SCALE,
            )
            fig.update_layout(
                xaxis_title="Comeback Momentum",
                yaxis_title="Fandom Intensity",
            )
            show_chart(fig, 365)
        else:
            st.info("Required score fields are not available.")

    
    section("Key Insights")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.markdown(
            '<div class="info-card">'
            '<div class="info-title">Chart Re-entry</div>'
            f'<div class="info-text">'
            f'{songs_count:,} songs are represented in the integrated analysis.'
            '</div></div>',
            unsafe_allow_html=True,
        )

    with i2:
        st.markdown(
            '<div class="info-card">'
            '<div class="info-title">Project Focus</div>'
            '<div class="info-text">'
            'The dashboard connects chart re-entry, comeback momentum, fandom intensity, '
            'sustainability and integrated song performance.'
            '</div></div>',
            unsafe_allow_html=True,
        )

    with i3:
        st.markdown(
            '<div class="info-card">'
            '<div class="info-title">Interpretation</div>'
            '<div class="info-text">'
            'All scores are project-specific analytical indices and should be interpreted '
            'within this dataset and methodology.'
            '</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# TOP SONGS
# ============================================================

elif page == "Top Songs":
    page_header(
        "RANKING HUB",
        "Top Songs",
        "A clean ranking view of songs with the strongest integrated project scores.",
    )

    df = apply_filters(integrated, selected_artists, selected_categories)

    if df is None or df.empty:
        st.warning("No integrated song data is available.")
        st.stop()

    score_col = first_existing(df, ["overall_performance_score"])

    if score_col:
        top = df.sort_values(score_col, ascending=False).head(ranking_size)

        cols = st.columns(5)
        for i, (_, row) in enumerate(top.head(5).iterrows()):
            with cols[i]:
                render_song_card(
                    i + 1,
                    row.get("song", "Unknown"),
                    row.get("artist", "Unknown"),
                    row.get(score_col, np.nan),
                )

        st.write("")

        display_cols = [
            "song",
            "artist",
            "total_reentries",
            "average_gap_days",
            "best_reentry_position",
            "average_momentum_score",
            "fandom_intensity_score",
            "sustainability_score",
            "overall_performance_score",
        ]
        display_cols = [c for c in display_cols if c in top.columns]

        table = top[display_cols].copy()

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download ranking CSV",
            data=top.to_csv(index=False).encode("utf-8"),
            file_name="kpop_top_songs.csv",
            mime="text/csv",
        )
    else:
        st.warning("overall_performance_score is missing from the integrated dataset.")


# ============================================================
# COMEBACK MOMENTUM
# ============================================================

elif page == "Comeback Momentum":
    page_header(
        "COMEBACK ANALYSIS",
        "Comeback Momentum",
        "Explore chart returns, gap lengths, re-entry positions and comeback-event strength.",
    )

    m = apply_filters(momentum, selected_artists, selected_categories)

    if m is None or m.empty:
        st.warning("Phase 4 comeback data is not available.")
        st.stop()

    gap_col = first_existing(m, ["gap_days"])
    momentum_col = first_existing(m, ["momentum_score"])
    position_col = first_existing(m, ["reentry_position"])

    avg_gap = pd.to_numeric(m[gap_col], errors="coerce").mean() if gap_col else np.nan
    longest_gap = pd.to_numeric(m[gap_col], errors="coerce").max() if gap_col else np.nan

    show_kpis(
        [
            (f"{len(m):,}", "Re-entry Events"),
            (f"{fmt(avg_gap)} days", "Average Gap"),
            (f"{fmt(longest_gap)} days", "Longest Gap"),
        ]
    )

    left, right = st.columns(2, gap="medium")

    with left:
        with st.container(border=True):
            chart_card_title("Strongest Comeback Events", "Highest momentum scores")

        if momentum_col:
            work = m.sort_values(momentum_col, ascending=False).head(10).copy()
            work["label"] = (
                work["song"].astype(str)
                if "song" in work.columns
                else work.index.astype(str)
            )

            fig = px.bar(
                work.sort_values(momentum_col),
                x=momentum_col,
                y="label",
                orientation="h",
                color=momentum_col,
                color_continuous_scale=SCALE,
                hover_data=["artist"] if "artist" in work.columns else None,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Momentum Score",
                yaxis_title="",
            )
            show_chart(fig, 410)
        else:
            st.info("Momentum score is not available.")

    
    with right:
        with st.container(border=True):
            chart_card_title("Gap vs Re-entry Position", "Return behaviour")

        if gap_col and position_col:
            fig = px.scatter(
                m,
                x=gap_col,
                y=position_col,
                color=momentum_col if momentum_col else None,
                hover_name="song" if "song" in m.columns else None,
                hover_data=["artist"] if "artist" in m.columns else None,
                color_continuous_scale=SCALE if momentum_col else None,
            )
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(
                xaxis_title="Gap (days)",
                yaxis_title="Re-entry position",
            )
            show_chart(fig, 410)
        else:
            st.info("Gap and re-entry position fields are not available.")

    
    section("Event Detail", "Detected comeback events")

    cols = [
        c for c in [
            "song",
            "artist",
            "previous_date",
            "reentry_date",
            "gap_days",
            "reentry_position",
            "momentum_score",
        ]
        if c in m.columns
    ]

    st.dataframe(
        m[cols].head(200),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FANDOM
# ============================================================

elif page == "Fandom Intensity":
    page_header(
        "FANDOM SIGNALS",
        "Fandom Intensity",
        "Explore the project-defined fandom intensity score and its relationship with chart behaviour.",
    )

    f = apply_filters(fandom, selected_artists, selected_categories)

    if f is None or f.empty:
        st.warning("Phase 5 fandom data is not available.")
        st.stop()

    fandom_col = first_existing(
        f,
        ["fandom_intensity_score", "fandom_score"],
    )

    if fandom_col:
        show_kpis(
            [
                (fmt(f[fandom_col].max(), 3), "Highest Fandom Score"),
                (fmt(f[fandom_col].mean(), 3), "Average Fandom Score"),
                (
                    f"{f['song'].nunique():,}" if "song" in f.columns else "—",
                    "Songs Analysed",
                ),
            ]
        )

        left, right = st.columns(2, gap="medium")

        with left:
            with st.container(border=True):
                chart_card_title("Highest Fandom Intensity", "Top songs")

            work = f.sort_values(fandom_col, ascending=False).head(10).copy()
            work["label"] = (
                work["song"].astype(str)
                if "song" in work.columns
                else work.index.astype(str)
            )

            fig = px.bar(
                work.sort_values(fandom_col),
                x=fandom_col,
                y="label",
                orientation="h",
                color=fandom_col,
                color_continuous_scale=SCALE,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Fandom Intensity",
                yaxis_title="",
            )
            show_chart(fig, 410)

        
        with right:
            with st.container(border=True):
                chart_card_title("Momentum × Fandom", "Bubble size = sustainability")

            if "average_momentum_score" in f.columns:
                fig = px.scatter(
                    f,
                    x="average_momentum_score",
                    y=fandom_col,
                    size="sustainability_score" if "sustainability_score" in f.columns else None,
                    color="sustainability_score" if "sustainability_score" in f.columns else None,
                    hover_name="song" if "song" in f.columns else None,
                    hover_data=["artist"] if "artist" in f.columns else None,
                    color_continuous_scale=SCALE,
                )
                fig.update_layout(
                    xaxis_title="Comeback Momentum",
                    yaxis_title="Fandom Intensity",
                )
                show_chart(fig, 410)
            else:
                st.info("Momentum score is not available.")

        
        if "fandom_category" in f.columns:
            section("Fandom Category Distribution", "Project-defined categories")

            counts = f["fandom_category"].value_counts().reset_index()
            counts.columns = ["category", "songs"]

            fig = px.bar(
                counts.sort_values("songs"),
                x="songs",
                y="category",
                orientation="h",
                color="songs",
                color_continuous_scale=SCALE,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Songs",
                yaxis_title="",
            )
            show_chart(fig, 340)

        section("Song-Level Detail", "Fandom analysis table")
        st.dataframe(
            f.head(200),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No fandom score column was found.")


# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":
    page_header(
        "LONGEVITY",
        "Chart Sustainability",
        "Explore which songs and artists maintain stronger chart presence over time.",
    )

    s = apply_filters(sustainability, selected_artists, selected_categories)

    if s is None or s.empty:
        st.warning("Phase 6 sustainability data is not available.")
        st.stop()

    sustainability_col = first_existing(
        s,
        ["sustainability_score"],
    )

    if sustainability_col:
        top_row = s.sort_values(sustainability_col, ascending=False).iloc[0]

        show_kpis(
            [
                (fmt(s[sustainability_col].max(), 3), "Highest Sustainability"),
                (fmt(s[sustainability_col].mean(), 3), "Average Sustainability"),
                (str(top_row.get("song", "—"))[:20], "Top Song"),
            ]
        )

        section("Top Songs by Sustainability", "Highest project scores")

        work = s.sort_values(sustainability_col, ascending=False).head(10).copy()
        work["label"] = (
            work["song"].astype(str)
            if "song" in work.columns
            else work.index.astype(str)
        )

        fig = px.bar(
            work.sort_values(sustainability_col),
            x=sustainability_col,
            y="label",
            orientation="h",
            color=sustainability_col,
            color_continuous_scale=SCALE,
            hover_data=["artist"] if "artist" in work.columns else None,
        )
        fig.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Sustainability Score",
            yaxis_title="",
        )
        show_chart(fig, 410)

        if artist_sustainability is not None and not artist_sustainability.empty:
            a = apply_filters(
                artist_sustainability,
                selected_artists,
                selected_categories,
            )

            artist_score = first_existing(
                a,
                ["sustainability_score"],
            )

            if artist_score and "artist" in a.columns:
                section("Artist Sustainability", "Artist-level view")

                work = a.sort_values(artist_score, ascending=False).head(10).copy()

                fig = px.bar(
                    work.sort_values(artist_score),
                    x=artist_score,
                    y="artist",
                    orientation="h",
                    color=artist_score,
                    color_continuous_scale=SCALE,
                )
                fig.update_layout(
                    coloraxis_showscale=False,
                    xaxis_title="Sustainability Score",
                    yaxis_title="",
                )
                show_chart(fig, 400)

        section("Song-Level Detail")
        st.dataframe(
            s.head(200),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No sustainability score column was found.")


# ============================================================
# ARTIST ANALYSIS
# ============================================================

elif page == "Artist Analysis":
    page_header(
        "ARTIST VIEW",
        "Artist Analysis",
        "Inspect artist-level sustainability together with momentum and fandom signals.",
    )

    # Use the integrated song-level dataset as the single source of truth.
    # This avoids schema mismatches in the optional Phase 6 artist CSV.
    artist_base = apply_filters(integrated, selected_artists, selected_categories)

    if artist_base is None or artist_base.empty:
        st.warning("Integrated song data is not available for artist analysis.")
        st.stop()

    if "artist" not in artist_base.columns:
        st.warning("The integrated dataset does not contain an artist column.")
        st.stop()

    # Build artist-level metrics from the same scores used elsewhere
    # in the dashboard. Mean is used so every artist is represented
    # consistently across songs.
    numeric_artist_cols = [
        c
        for c in [
            "sustainability_score",
            "average_momentum_score",
            "fandom_intensity_score",
            "overall_performance_score",
        ]
        if c in artist_base.columns
    ]

    artist_work = artist_base.copy()
    for col in numeric_artist_cols:
        artist_work[col] = pd.to_numeric(artist_work[col], errors="coerce")

    agg_map = {col: "mean" for col in numeric_artist_cols}
    artist_summary = (
        artist_work.groupby("artist", dropna=True)
        .agg(agg_map)
        .reset_index()
    )

    song_counts = (
        artist_work.groupby("artist", dropna=True)["song"]
        .nunique()
        .rename("song_count")
        .reset_index()
        if "song" in artist_work.columns
        else pd.DataFrame(columns=["artist", "song_count"])
    )

    if not song_counts.empty:
        artist_summary = artist_summary.merge(song_counts, on="artist", how="left")

    sustainability_col = first_existing(
        artist_summary,
        ["sustainability_score"],
    )

    momentum_col = first_existing(
        artist_summary,
        ["average_momentum_score"],
    )

    fandom_col = first_existing(
        artist_summary,
        ["fandom_intensity_score"],
    )

    if sustainability_col is None:
        st.warning(
            "The integrated dataset does not contain sustainability_score, "
            "so artist sustainability cannot be displayed."
        )
        st.stop()

    artist_summary = artist_summary.dropna(
        subset=[sustainability_col]
    ).copy()

    if artist_summary.empty:
        st.warning("No artist sustainability values are available.")
        st.stop()

    artist_list = sorted(
        artist_summary["artist"].astype(str).dropna().unique().tolist()
    )

    selected_artist = st.selectbox(
        "Select an artist",
        ["All artists"] + artist_list,
    )

    if selected_artist == "All artists":
        work = artist_summary.copy()
    else:
        work = artist_summary[
            artist_summary["artist"].astype(str) == selected_artist
        ].copy()

    selected_row = work.iloc[0]

    show_kpis(
        [
            (
                fmt(selected_row.get(sustainability_col), 3),
                "Sustainability",
            ),
            (
                fmt(selected_row.get(momentum_col), 3)
                if momentum_col
                else "—",
                "Momentum",
            ),
            (
                fmt(selected_row.get(fandom_col), 3)
                if fandom_col
                else "—",
                "Fandom",
            ),
            (
                f"{int(selected_row.get('song_count', 0)):,}",
                "Songs",
            ),
        ]
    )

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            chart_card_title(
                "Artist Sustainability",
                "Mean score across analysed songs",
            )

            top = artist_summary.sort_values(
                sustainability_col,
                ascending=False,
            ).head(ranking_size).copy()

            fig = px.bar(
                top.sort_values(sustainability_col),
                x=sustainability_col,
                y="artist",
                orientation="h",
                color=sustainability_col,
                color_continuous_scale=SCALE,
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Sustainability Score",
                yaxis_title="",
            )
            show_chart(fig, 410)

    with right:
        with st.container(border=True):
            chart_card_title(
                "Momentum vs Fandom",
                "Artist-level mean scores",
            )

            if momentum_col and fandom_col:
                plot_df = artist_summary.dropna(
                    subset=[momentum_col, fandom_col]
                ).copy()

                fig = px.scatter(
                    plot_df,
                    x=momentum_col,
                    y=fandom_col,
                    size="song_count" if "song_count" in plot_df.columns else None,
                    color=sustainability_col,
                    hover_name="artist",
                    color_continuous_scale=SCALE,
                )
                fig.update_layout(
                    coloraxis_colorbar_title="Sustainability",
                    xaxis_title="Momentum",
                    yaxis_title="Fandom Intensity",
                )
                show_chart(fig, 410)
            else:
                st.info(
                    "Momentum and fandom scores are not available "
                    "in the integrated dataset."
                )

    section(
        "Selected Artist Profile",
        "Mean scores across the artist's analysed songs",
    )

    if selected_artist != "All artists":
        profile_labels = []
        profile_values = []

        for label, col in [
            ("Sustainability", sustainability_col),
            ("Momentum", momentum_col),
            ("Fandom", fandom_col),
        ]:
            if col and pd.notna(selected_row.get(col)):
                profile_labels.append(label)
                profile_values.append(float(selected_row[col]))

        if profile_values:
            fig = go.Figure(
                go.Scatterpolar(
                    r=profile_values + [profile_values[0]],
                    theta=profile_labels + [profile_labels[0]],
                    fill="toself",
                    line=dict(color="#7B3FC6", width=2),
                    fillcolor="rgba(123,63,198,0.16)",
                )
            )
            fig.update_layout(
                height=360,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        showgrid=True,
                        gridcolor="#E8E3F0",
                    ),
                    angularaxis=dict(
                        gridcolor="#E8E3F0",
                    ),
                ),
                showlegend=False,
            )
            show_chart(fig, 360)
    else:
        st.info("Select an artist above to see the individual score profile.")

    section(
        "Artist Dataset",
        "Artist-level metrics calculated from the integrated song dataset",
    )

    st.dataframe(
        artist_summary.sort_values(
            sustainability_col,
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# SONG EXPLORER
# ============================================================

elif page == "Song Explorer":
    page_header(
        "DEEP DIVE",
        "Song Explorer",
        "Open a song profile and inspect its integrated analytical dimensions.",
    )

    df = apply_filters(integrated, selected_artists, selected_categories)

    if df is None or df.empty or "song" not in df.columns:
        st.warning("Integrated song data is not available.")
        st.stop()

    if "artist" in df.columns:
        df["_option"] = (
            df["song"].astype(str)
            + " — "
            + df["artist"].astype(str)
        )
    else:
        df["_option"] = df["song"].astype(str)

    options = df["_option"].drop_duplicates().tolist()

    selected = st.selectbox("Choose a song", options)

    row = df[df["_option"] == selected].iloc[0]

    song = str(row.get("song", "Unknown"))
    artist = str(row.get("artist", "Unknown"))

    left, right = st.columns([.34, .66], gap="large")

    with left:
        cover = get_cover(song, artist)
        if cover:
            st.image(cover, width="stretch")
        else:
            st.markdown(
                '<div class="song-placeholder" style="border-radius:14px;">K</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="section-title" style="margin-top:12px;">'
            f'{html.escape(song)}</div>'
            f'<div class="song-artist">{html.escape(artist)}</div>',
            unsafe_allow_html=True,
        )

    with right:
        show_kpis(
            [
                (fmt(row.get("overall_performance_score"), 3), "Overall Performance"),
                (fmt(row.get("average_momentum_score"), 3), "Momentum"),
                (fmt(row.get("fandom_intensity_score"), 3), "Fandom"),
                (fmt(row.get("sustainability_score"), 3), "Sustainability"),
            ]
        )

        section("Score Profile")

        dimensions = [
            ("Overall", row.get("overall_performance_score", np.nan)),
            ("Momentum", row.get("average_momentum_score", np.nan)),
            ("Fandom", row.get("fandom_intensity_score", np.nan)),
            ("Sustainability", row.get("sustainability_score", np.nan)),
        ]

        radar_values = []
        radar_labels = []

        for label, value in dimensions:
            try:
                value = float(value)
                if not np.isnan(value):
                    radar_labels.append(label)
                    radar_values.append(value)
            except Exception:
                pass

        if radar_values:
            radar_values_closed = radar_values + [radar_values[0]]
            radar_labels_closed = radar_labels + [radar_labels[0]]

            fig = px.line_polar(
                r=radar_values_closed,
                theta=radar_labels_closed,
                line_close=True,
            )
            fig.update_traces(
                fill="toself",
                line_color="#6D35B1",
            )
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(
                        visible=True,
                        gridcolor="#E7DFEF",
                    ),
                    angularaxis=dict(
                        gridcolor="#E7DFEF",
                    ),
                ),
                showlegend=False,
            )
            show_chart(fig, 370)

    section("Chart Behaviour")

    behaviour_cols = [
        c for c in [
            "total_reentries",
            "average_gap_days",
            "longest_gap_days",
            "best_reentry_position",
            "average_reentry_position",
        ]
        if c in row.index
    ]

    if behaviour_cols:
        behaviour = pd.DataFrame(
            {
                "Metric": [c.replace("_", " ").title() for c in behaviour_cols],
                "Value": [row[c] for c in behaviour_cols],
            }
        )
        st.dataframe(
            behaviour,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# ABOUT
# ============================================================

else:
    page_header(
        "PROJECT METHODOLOGY",
        "About the Project",
        "What the dashboard measures, how the dimensions connect, and how to interpret the scores.",
    )

    left, right = st.columns([1.15, .85], gap="medium")

    with left:
        section("Project Objective")
        st.markdown(
            '<div class="info-card">'
            '<div class="info-text">'
            'This project studies chart behaviour in the South Korea Top 50 playlist '
            'through comeback momentum, chart re-entry, fandom intensity, '
            'sustainability and integrated song performance.'
            '</div></div>',
            unsafe_allow_html=True,
        )

        section("Five Analytical Dimensions")

        dimensions = [
            ("Chart Re-entry", "Detects songs returning to the chart after an absence."),
            ("Comeback Momentum", "Measures the strength of detected return events."),
            ("Fandom Intensity", "A project-defined score built from chart behaviour."),
            ("Chart Sustainability", "Measures persistence and continued chart presence."),
            ("Integrated Performance", "Combines the project dimensions into an overall score."),
        ]

        for title, text in dimensions:
            st.markdown(
                f'<div class="info-card" style="margin-bottom:9px;">'
                f'<div class="info-title">{html.escape(title)}</div>'
                f'<div class="info-text">{html.escape(text)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with right:
        section("Interpretation")

        st.markdown(
            '<div class="info-card">'
            '<div class="info-text">'
            'The scores in this dashboard are analytical indices created for this project. '
            'They should not be interpreted as direct measurements of real-world fandom size, '
            'fan count, total popularity, or commercial revenue.'
            '</div></div>',
            unsafe_allow_html=True,
        )

        section("Data Status")

        files = [
            ("Integrated analysis", integrated),
            ("Comeback momentum", momentum),
            ("Fandom intensity", fandom),
            ("Sustainability", sustainability),
            ("Artist sustainability", artist_sustainability),
            ("Cleaned source data", cleaned),
        ]

        rows = []
        for name, frame in files:
            rows.append(
                {
                    "Dataset": name,
                    "Status": "Loaded" if frame is not None and not frame.empty else "Not found",
                    "Rows": len(frame) if frame is not None else 0,
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )

        section("Technology")

        st.markdown(
            '<div class="info-card">'
            '<div class="info-text">'
            'Python · Pandas · Plotly · Streamlit'
            '</div></div>',
            unsafe_allow_html=True,
        )

