
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
import html
import re

# ============================================================
# K-POP CHART ANALYTICS
# Final Dashboard
# Built from KPOP_Chart_Analytics_Final.ipynb outputs
# ============================================================

st.set_page_config(
    page_title="K-Pop Chart Analytics",
    page_icon="KP",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================

BG = "#F7F4FB"
WHITE = "#FFFFFF"
TEXT = "#261832"
MUTED = "#6E617B"
MUTED_2 = "#9589A2"
PURPLE_DARK = "#24113F"
PURPLE = "#A86BFF"
PURPLE_2 = "#C08BFF"
PURPLE_LIGHT = "#5B3D78"
PURPLE_PALE = "#2A1A3B"
BORDER = "#E4DCEF"
GRID = "#EAE3F2"

PURPLE_SCALE = [
    "#E4D5F2",
    "#C9A9E7",
    "#AB7BD4",
    "#8958C0",
    "#A86BFF",
    "#C08BFF",
    "#E0C4FF",
]

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@500;600;700;800&display=swap');

:root {{
    --bg:{BG};
    --white:{WHITE};
    --text:{TEXT};
    --muted:{MUTED};
    --purple:{PURPLE};
    --purple-dark:{PURPLE_DARK};
    --border:{BORDER};
}}

html, body, [class*="css"], .stApp {{
    font-family:"DM Sans","Inter",Arial,sans-serif !important;
    color:var(--text) !important;
}}

.stApp {{
    background:var(--bg) !important;
}}

.block-container {{
    max-width:1540px;
    padding:1.35rem 1.75rem 2.5rem;
}}

[data-testid="stHeader"] {{
    background:transparent !important;
}}

h1,h2,h3,h4,h5,h6 {{
    font-family:"Inter","DM Sans",Arial,sans-serif !important;
    color:var(--text) !important;
}}

p,span,label,td,th {{
    font-family:"DM Sans","Inter",Arial,sans-serif;
}}

/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

[data-testid="stSidebar"] {{
    background:#140D20 !important;
    border-right:1px solid var(--border) !important;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding:1.15rem 0.9rem 1rem !important;
}}

.brand {{
    padding:.25rem .5rem 1rem;
}}

.brand-logo {{
    width:84px;
    height:84px;
    box-sizing:border-box;
    border-radius:50%;
    object-fit:cover;
    padding:0;
    background:transparent;
    border:0;
    box-shadow:0 8px 18px rgba(49,20,73,.22);
    margin-bottom:.8rem;
}}

.brand-title {{
    color:#F7F2FC !important;
    font-family:"Inter",sans-serif;
    font-weight:800;
    font-size:.88rem;
    letter-spacing:-.02em;
}}

.brand-subtitle {{
    color:var(--muted) !important;
    font-size:.64rem;
    line-height:1.55;
    margin-top:.35rem;
}}

.sidebar-label {{
    color:#C08BFF !important;
    font-family:"Inter",sans-serif;
    font-size:.60rem;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.13em;
    margin:.95rem .5rem .35rem;
}}

[data-testid="stSidebar"] hr {{
    border:0 !important;
    border-top:1px solid var(--border) !important;
    margin:.4rem 0 !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {{
    gap:.12rem !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label {{
    min-height:36px !important;
    padding:.42rem .55rem !important;
    border:1px solid transparent !important;
    border-radius:9px !important;
    background:transparent !important;
    color:#B8A9C5 !important;
    opacity:1 !important;
    font-size:.72rem !important;
    font-weight:600 !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
    background:#21132F !important;
    border-color:#4A3262 !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
    background:linear-gradient(90deg,#322047,#241631) !important;
    border-color:#7448A5 !important;
    color:#F0DEFF !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label p,
[data-testid="stSidebar"] [data-testid="stRadio"] label span,
[data-testid="stSidebar"] [data-testid="stRadio"] label div {{
    color:inherit !important;
    opacity:1 !important;
    font-size:inherit !important;
    font-weight:inherit !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] input {{
    accent-color:var(--purple) !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background:#1B1328 !important;
    border:1px solid #4A3560 !important;
    border-radius:8px !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] * {{
    color:#F0E8F8 !important;
    opacity:1 !important;
}}

.sidebar-note {{
    margin-top:1rem;
    padding:.7rem;
    border:1px solid var(--border);
    border-radius:9px;
    background:#1B1328;
    color:var(--muted) !important;
    font-size:.61rem;
    line-height:1.55;
}}

/* ----------------------------------------------------------
   HERO
---------------------------------------------------------- */

.hero {{
    position:relative;
    overflow:hidden;
    min-height:225px;
    border-radius:20px;
    padding:2rem 2.2rem;
    margin-bottom:1.1rem;
    background:
        radial-gradient(circle at 92% 12%,rgba(255,255,255,.18),transparent 24%),
        radial-gradient(circle at 82% 100%,rgba(255,255,255,.10),transparent 32%),
        linear-gradient(115deg,#1D0E32 0%,#3C1B62 48%,#7139A1 100%);
    box-shadow:0 20px 46px rgba(0,0,0,.28);
}}

.hero-inner {{
    position:relative;
    z-index:2;
    max-width:900px;
}}

.hero-kicker {{
    color:rgba(255,255,255,.76);
    font-family:"Inter",sans-serif;
    font-size:.61rem;
    font-weight:800;
    letter-spacing:.14em;
    text-transform:uppercase;
}}

.hero-title {{
    color:#FFFFFF !important;
    font-family:"Inter",sans-serif !important;
    font-size:clamp(2.3rem,4.7vw,3.65rem);
    font-weight:800;
    line-height:1;
    letter-spacing:-.065em;
    margin:.55rem 0 .7rem;
}}

.hero-copy {{
    color:rgba(255,255,255,.89);
    font-size:.77rem;
    line-height:1.65;
    max-width:820px;
}}

.hero-pill {{
    display:inline-block;
    margin-top:1rem;
    padding:.40rem .7rem;
    border:1px solid rgba(255,255,255,.23);
    background:rgba(255,255,255,.10);
    border-radius:999px;
    color:#FFFFFF;
    font-size:.60rem;
    font-weight:600;
}}

/* ----------------------------------------------------------
   MOTION / SECTION HIERARCHY
---------------------------------------------------------- */

@keyframes rise-in {{
    from {{ opacity:0; transform:translateY(14px); }}
    to {{ opacity:1; transform:translateY(0); }}
}}

@keyframes line-reveal {{
    from {{ width:0; opacity:0; }}
    to {{ width:100%; opacity:1; }}
}}

@keyframes hero-shimmer {{
    0%, 100% {{ transform:translateX(-8%) scale(1); opacity:.34; }}
    50% {{ transform:translateX(8%) scale(1.08); opacity:.58; }}
}}

.eyebrow, .page-title, .page-copy, .section-label, .rule {{
    animation:rise-in .65s cubic-bezier(.22,1,.36,1) both;
}}

.eyebrow {{
    color:#75449B;
    font-family:"Inter",sans-serif;
    font-size:.60rem;
    font-weight:800;
    letter-spacing:.14em;
    text-transform:uppercase;
    margin-top:.4rem;
}}

.page-title {{
    color:#261832;
    font-family:"Inter",sans-serif;
    font-size:2rem;
    font-weight:800;
    letter-spacing:-.05em;
    line-height:1.05;
    margin-top:.45rem;
}}

.page-copy {{
    color:#6E617B;
    font-size:.76rem;
    line-height:1.6;
    margin-top:.45rem;
}}

.rule {{
    height:2px;
    width:100%;
    margin:1rem 0 1.15rem;
    background:linear-gradient(90deg,#8B4BC2 0%,#D8B7FF 42%,transparent 100%);
    transform-origin:left center;
    animation:line-reveal .9s cubic-bezier(.22,1,.36,1) both;
}}

.section-label {{
    position:relative;
    color:#75449B;
    font-family:"Inter",sans-serif;
    font-size:.60rem;
    font-weight:800;
    letter-spacing:.15em;
    line-height:1;
    text-transform:uppercase;
    margin:1.55rem 0 .75rem;
    padding-left:.8rem;
}}

.section-label::before {{
    content:"";
    position:absolute;
    left:0;
    top:50%;
    width:3px;
    height:1.1rem;
    border-radius:3px;
    background:linear-gradient(#7B3FE4,#C08BFF);
    transform:translateY(-50%);
    box-shadow:0 0 12px rgba(139,75,194,.35);
}}

.hero::after {{
    content:"";
    position:absolute;
    width:45%;
    height:160%;
    right:-12%;
    top:-28%;
    background:linear-gradient(110deg,transparent,rgba(255,255,255,.12),transparent);
    filter:blur(8px);
    transform:rotate(18deg);
    animation:hero-shimmer 7s ease-in-out infinite;
}}

.kpi, [data-testid="stPlotlyChart"], [data-testid="stDataFrame"],
[data-testid="stVerticalBlockBorderWrapper"], .insight {{
    animation:rise-in .7s cubic-bezier(.22,1,.36,1) both;
    transition:transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}}

.kpi:nth-of-type(2), [data-testid="stPlotlyChart"]:nth-of-type(2),
.insight:nth-of-type(2) {{ animation-delay:.08s; }}
.kpi:nth-of-type(3), [data-testid="stPlotlyChart"]:nth-of-type(3),
.insight:nth-of-type(3) {{ animation-delay:.16s; }}
.kpi:nth-of-type(4), [data-testid="stPlotlyChart"]:nth-of-type(4),
.insight:nth-of-type(4) {{ animation-delay:.24s; }}
.kpi:nth-of-type(5), [data-testid="stPlotlyChart"]:nth-of-type(5),
.insight:nth-of-type(5) {{ animation-delay:.32s; }}

.kpi:hover, [data-testid="stPlotlyChart"]:hover,
[data-testid="stVerticalBlockBorderWrapper"]:hover, .insight:hover {{
    transform:translateY(-3px);
    border-color:#B88AE0 !important;
    box-shadow:0 14px 30px rgba(78,35,108,.13) !important;
}}

.song-card img {{
    transition:transform .45s cubic-bezier(.22,1,.36,1), filter .45s ease;
}}

.song-card:hover img {{
    transform:scale(1.045);
    filter:saturate(1.12) contrast(1.03);
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration:.01ms !important;
        animation-iteration-count:1 !important;
        scroll-behavior:auto !important;
        transition-duration:.01ms !important;
    }}
}}

/* ----------------------------------------------------------
   PAGE TITLES / SECTION PANELS
---------------------------------------------------------- */

.card {{
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    box-shadow: none;
}}

.card-title {{
    color: #261832 !important;
    font-family: "Inter", sans-serif;
    font-size: .90rem;
    font-weight: 800;
    letter-spacing: -.02em;
    line-height: 1.25;
    margin-top: .15rem;
}}

.card-note {{
    color: #6E617B !important;
    font-size: .64rem;
    line-height: 1.5;
    margin-top: .20rem;
    margin-bottom: .55rem;
}}

/* Real component surfaces */
/* Bordered Streamlit containers used for album cards */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background:#FFFFFF !important;
    border:1px solid #E4DCEF !important;
    border-radius:14px !important;
    box-shadow:0 8px 24px rgba(55,28,74,.06) !important;
    padding:.35rem !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] {{
    margin-bottom:.15rem !important;
}}

[data-testid="stPlotlyChart"] .modebar {{ opacity:.18; transition:opacity .2s ease; }}
[data-testid="stPlotlyChart"]:hover .modebar {{ opacity:.75; }}

[data-testid="stPlotlyChart"] {{
    background: #FFFFFF !important;
    border: 1px solid #E4DCEF !important;
    border-radius: 14px !important;
    padding: 8px 10px 4px !important;
    box-shadow: 0 8px 24px rgba(55,28,74,.06) !important;
    margin-top: .25rem !important;
    margin-bottom: 1rem !important;
}}

[data-testid="stDataFrame"] {{
    background: #FFFFFF !important;
    border: 1px solid #E4DCEF !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 24px rgba(55,28,74,.06) !important;
    margin-top: .25rem !important;
    margin-bottom: 1rem !important;
}}

/* ----------------------------------------------------------
   KPI
---------------------------------------------------------- */

.kpi {{
    background:linear-gradient(145deg,#FFFFFF,#F8F3FC);
    border:1px solid var(--border);
    border-radius:13px;
    padding:.9rem 1rem;
    min-height:112px;
    box-shadow:0 8px 24px rgba(55,28,74,.06);
}}

.kpi-label {{
    color:#756780;
    font-family:"Inter",sans-serif;
    font-size:.56rem;
    font-weight:800;
    letter-spacing:.09em;
    text-transform:uppercase;
}}

.kpi-value {{
    color:#4B2369;
    font-family:"Inter",sans-serif;
    font-size:1.30rem;
    font-weight:800;
    letter-spacing:-.045em;
    line-height:1.1;
    margin-top:.35rem;
}}

.kpi-value.long {{
    font-size:.88rem;
    line-height:1.25;
}}

.kpi-sub {{
    color:#9589A2;
    font-size:.59rem;
    margin-top:.4rem;
}}

/* ----------------------------------------------------------
   TOP SONG CARDS
---------------------------------------------------------- */

.song-card {{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:12px;
    padding:.48rem;
    box-shadow:0 8px 24px rgba(55,28,74,.06);
    height:100%;
}}

.song-card [data-testid="stImage"] {{
    border-radius:9px !important;
    overflow:hidden !important;
}}

.song-card img {{
    width:100% !important;
    aspect-ratio:1/1 !important;
    object-fit:cover !important;
    border-radius:9px !important;
}}

.cover-empty {{
    width:100%;
    aspect-ratio:1/1;
    border-radius:9px;
    background:linear-gradient(145deg,#3A205B,#7A45A8);
    display:flex;
    align-items:center;
    justify-content:center;
    color:#F0DEFF;
    font-family:"Inter",sans-serif;
    font-weight:800;
    font-size:1.05rem;
}}

.rank {{
    display:inline-flex;
    width:24px;
    height:24px;
    align-items:center;
    justify-content:center;
    border-radius:7px;
    background:var(--purple-dark);
    color:#FFFFFF;
    font-size:.60rem;
    font-weight:800;
    margin-top:.48rem;
}}

.song-name {{
    color:var(--text);
    font-family:"Inter",sans-serif;
    font-size:.69rem;
    line-height:1.28;
    font-weight:800;
    margin-top:.30rem;
    min-height:1.75rem;
}}

.song-artist {{
    color:var(--muted);
    font-size:.59rem;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}}

.song-score {{
    color:#C08BFF;
    font-size:.57rem;
    font-weight:700;
    margin-top:.23rem;
}}

/* ----------------------------------------------------------
   TABLES / CONTROLS
---------------------------------------------------------- */

[data-testid="stDataFrame"] {{
    border:1px solid var(--border);
    border-radius:10px;
    overflow:hidden;
}}

[data-testid="stDataFrame"] * {{
    font-size:.67rem !important;
}}

[data-testid="stMetric"] {{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:11px;
    padding:.65rem .75rem;
}}

[data-testid="stMetricValue"] {{
    color:#4B2369 !important;
}}

.stButton button {{
    border:1px solid #5B3D78 !important;
    background:#241631 !important;
    color:#F0DEFF !important;
    border-radius:8px !important;
    font-weight:700 !important;
}}

.stButton button:hover {{
    border-color:#A86BFF !important;
    background:#352047 !important;
}}

[data-baseweb="select"] > div {{
    border-color:#5B3D78 !important;
    border-radius:8px !important;
}}

[data-baseweb="select"] * {{
    color:#F0E8F8 !important;
}}

.insight {{
    padding:.62rem .7rem;
    background:#FBF9FD;
    border:1px solid #EDE5F2;
    border-radius:9px;
    color:#51435A;
    font-size:.64rem;
    line-height:1.5;
    margin-bottom:.42rem;
}}

.insight strong {{
    color:#4B2369;
}}

.footer {{
    border-top:1px solid var(--border);
    margin-top:2rem;
    padding-top:1rem;
    text-align:center;
    color:#8E7D9E;
    font-size:.59rem;
    line-height:1.6;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# PATHS AND DATA
# ============================================================

APP_DIR = Path(__file__).resolve().parent

# The dashboard can run either from the project root or from a
# dedicated dashboard subfolder. Keep the same UI/design in both cases.
if (APP_DIR / "outputs").exists():
    PROJECT_DIR = APP_DIR
elif (APP_DIR.parent / "outputs").exists():
    PROJECT_DIR = APP_DIR.parent
else:
    PROJECT_DIR = APP_DIR

LOGO_CANDIDATES = [
    PROJECT_DIR / "img" / "logo.png",
    APP_DIR / "img" / "logo.png",
    PROJECT_DIR / "logo.png",
]
LOGO_PATH = next((p for p in LOGO_CANDIDATES if p.exists()), None)
LOGO_DATA = (
    base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    if LOGO_PATH is not None
    else ""
)

OUTPUT_DIR = PROJECT_DIR / "outputs"
DATA_DIR = PROJECT_DIR / "data"

def read_output(filename):
    path = OUTPUT_DIR / filename
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None

dashboard = read_output("KPOP_FINAL_DASHBOARD_DATA.csv")
top_songs = read_output("KPOP_FINAL_TOP_SONGS.csv")
all_songs = read_output("KPOP_FINAL_ALL_SONGS.csv")
artist_analysis = read_output("KPOP_FINAL_ARTIST_ANALYSIS.csv")
kpis = read_output("KPOP_FINAL_KPIS.csv")
momentum = read_output("phase4_comeback_momentum_events.csv")
fandom = read_output("phase5_fandom_intensity_song_analysis.csv")
sustainability = read_output("phase6_chart_sustainability_analysis.csv")
artist_sustainability = read_output("phase6_artist_sustainability_analysis.csv")

if dashboard is None:
    st.error(
        "Dashboard data was not found. Please confirm the project outputs folder "
        "contains KPOP_FINAL_DASHBOARD_DATA.csv."
    )
    st.stop()

dashboard = dashboard.copy()

# Numeric conversion.
numeric_columns = [
    "total_reentries",
    "average_gap_days",
    "longest_gap_days",
    "best_reentry_position",
    "average_reentry_position",
    "highest_momentum_score",
    "average_momentum_score",
    "normalized_frequency",
    "chart_strength",
    "fandom_intensity_score",
    "reentry_strength",
    "sustainability_score",
    "average_momentum_score_normalized",
    "fandom_intensity_score_normalized",
    "sustainability_score_normalized",
    "overall_performance_score",
    "overall_rank",
    "performance_balance",
]

for col in numeric_columns:
    if col in dashboard.columns:
        dashboard[col] = pd.to_numeric(dashboard[col], errors="coerce")

dashboard = dashboard.dropna(subset=["song", "artist"]).copy()

# ============================================================
# HELPERS
# ============================================================

def esc(value):
    return html.escape(str(value))

def page_header(title, description):
    st.markdown(
        f"""
        <div class="eyebrow">South Korea Top 50 · Data Science Project</div>
        <div class="page-title">{esc(title)}</div>
        <div class="page-copy">{esc(description)}</div>
        <div class="rule"></div>
        """,
        unsafe_allow_html=True,
    )

def section_label(text):
    st.markdown(
        f'<div class="section-label">{esc(text)}</div>',
        unsafe_allow_html=True,
    )

def card_heading(title, note=""):
    note_html = f'<div class="card-note">{esc(note)}</div>' if note else ""
    st.markdown(
        f"""
        <div class="card-title">{esc(title)}</div>
        {note_html}
        """,
        unsafe_allow_html=True,
    )

def style_plot(fig, height=420, title=None):
    fig.update_layout(
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Inter, Arial, sans-serif",
            color=TEXT,
            size=10,
        ),
        margin=dict(l=24, r=18, t=55 if title else 18, b=32),
        title=dict(
            text=title or "",
            x=0,
            xanchor="left",
            font=dict(
                family="Inter, Arial, sans-serif",
                size=14,
                color=TEXT,
            ),
        ),
        legend=dict(
            font=dict(
                family="Inter, Arial, sans-serif",
                size=9,
                color="#51435A",
            ),
            bgcolor="rgba(27,19,40,0)",
        ),
        hoverlabel=dict(
            bgcolor="#241631",
            bordercolor="#7448A5",
            font=dict(
                family="Inter, Arial, sans-serif",
                color="#261832",
                size=10,
            ),
        ),
        hovermode="closest",
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor="#604A72",
        tickfont=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#261832",
        ),
        title_font=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#51435A",
        ),
        tickcolor="#604A72",
        automargin=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor="#604A72",
        tickfont=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#261832",
        ),
        title_font=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#51435A",
        ),
        tickcolor="#604A72",
        automargin=True,
    )
    return fig


def style_horizontal_ranking(fig, height=470):
    """High-contrast horizontal ranking chart with readable long labels."""
    fig.update_layout(
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Inter, Arial, sans-serif",
            color=TEXT,
            size=10,
        ),
        margin=dict(l=245, r=24, t=22, b=44),
        showlegend=False,
        coloraxis_showscale=False,
        hovermode="closest",
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor="#604A72",
        tickfont=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#51435A",
        ),
        title_font=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#51435A",
        ),
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#604A72",
        tickfont=dict(
            family="Inter, Arial, sans-serif",
            size=9,
            color="#261832",
        ),
        title_font=dict(
            family="Inter, Arial, sans-serif",
            size=10,
            color="#51435A",
        ),
        automargin=True,
    )
    return fig

def get_cover(row):
    value = row.get("album_cover_url", "")
    if pd.isna(value):
        return ""
    value = str(value).strip()
    if value.startswith(("http://", "https://")):
        return value
    return ""

def chart_label(song, artist, max_len=42):
    text = f"{song} — {artist}"
    return text if len(text) <= max_len else text[:max_len - 1].rstrip() + "…"

def render_song_card(row, rank):
    cover = get_cover(row)

    # Use a real Streamlit bordered container. A raw HTML <div> cannot wrap
    # a later st.image() call, which previously created the empty pill above
    # every album cover.
    with st.container(border=True):
        if cover:
            st.image(cover, use_container_width=True)
        else:
            st.markdown('<div class="cover-empty">KP</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="rank">{int(rank)}</div>
            <div class="song-name">{esc(row["song"])}</div>
            <div class="song-artist">{esc(row["artist"])}</div>
            <div class="song-score">
                Overall score {float(row["overall_performance_score"]):.4f}
            </div>
            """,
            unsafe_allow_html=True,
        )

def top_rows(data, n=10, score="overall_performance_score"):
    return data.sort_values(score, ascending=False).head(n).copy()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    f"""
    <div class="brand">
        <img class="brand-logo" src="data:image/png;base64,{LOGO_DATA}" alt="K-Pop Chart Analytics logo">
        <div class="brand-subtitle">
            Data-driven analysis of chart re-entry, comeback momentum,
            fandom intensity and sustainability.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-label">Dashboard</div>',
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Dashboard",
    [
        "Home",
        "Top Songs",
        "Comeback Momentum",
        "Fandom Intensity",
        "Sustainability",
        "Artist Analysis",
        "Song Explorer",
        "About Project",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-label">Filters</div>',
    unsafe_allow_html=True,
)

artists = sorted(dashboard["artist"].astype(str).unique())
selected_artists = st.sidebar.multiselect(
    "Artist",
    artists,
    default=[],
)

categories = []
if "fandom_category" in dashboard.columns:
    categories = sorted(
        dashboard["fandom_category"].dropna().astype(str).unique()
    )

selected_categories = st.sidebar.multiselect(
    "Fandom category",
    categories,
    default=[],
)

ranking_size = st.sidebar.slider(
    "Ranking size",
    min_value=5,
    max_value=10,
    value=10,
)

filtered = dashboard.copy()

if selected_artists:
    filtered = filtered[
        filtered["artist"].astype(str).isin(selected_artists)
    ]

if selected_categories:
    filtered = filtered[
        filtered["fandom_category"].astype(str).isin(selected_categories)
    ]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        <b>Interpretation note</b><br>
        Momentum, fandom intensity, sustainability and overall performance
        are project-specific analytical indices. They are intended for
        comparison within this dataset and are not direct measurements
        of real-world fandom size or commercial success.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-inner">
                <div class="hero-kicker">
                    South Korea Top 50 · Data Science Project
                </div>
                <div class="hero-title">
                    K-POP CHART ANALYTICS
                </div>
                <div class="hero-copy">
                    A complete analytical view of chart re-entry, comeback
                    momentum, fandom intensity, sustainability and integrated
                    song performance.
                </div>
                <div class="hero-pill">
                    Chart Re-Entry · Comeback Momentum · Fandom Intensity · Sustainability
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_songs = filtered["song"].nunique()
    total_artists = filtered["artist"].nunique()

    if momentum is not None:
        m = momentum.copy()
        if selected_artists:
            m = m[m["artist"].astype(str).isin(selected_artists)]
        reentry_events = len(m)
        avg_gap = m["gap_days"].mean() if not m.empty else np.nan
    else:
        reentry_events = int(filtered["total_reentries"].sum())
        avg_gap = filtered["average_gap_days"].mean()

    top = filtered.sort_values(
        "overall_performance_score", ascending=False
    ).iloc[0]

    kpis_home = [
        ("Songs", f"{total_songs:,}", "Songs in current view"),
        ("Re-entry events", f"{reentry_events:,}", "Detected chart returns"),
        ("Average gap", f"{avg_gap:.2f} days", "Between appearances"),
        ("Artists", f"{total_artists:,}", "Artists in current view"),
        ("Top performer", str(top["song"]), str(top["artist"])),
    ]

    cols = st.columns(5)
    for col, (label, value, sub) in zip(cols, kpis_home):
        with col:
            long = "long" if len(value) > 18 else ""
            st.markdown(
                f"""
                <div class="kpi">
                    <div class="kpi-label">{esc(label)}</div>
                    <div class="kpi-value {long}">{esc(value)}</div>
                    <div class="kpi-sub">{esc(sub)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_label("Top songs")

    top10 = top_rows(filtered, ranking_size)

    card_heading(
        "Top Songs by Overall Performance",
        "Album artwork and ranking from the integrated performance score.",
    )

    for start in range(0, len(top10), 5):
        chunk = top10.iloc[start:start + 5]
        cols = st.columns(5, gap="small")

        for offset, (_, row) in enumerate(chunk.iterrows()):
            with cols[offset]:
                render_song_card(row, start + offset + 1)

        if start + 5 < len(top10):
            st.write("")


    section_label("Analytical overview")

    left, right = st.columns([1.45, 1], gap="large")

    with left:
        card_heading(
            "Overall performance ranking",
            "Comparison of the highest-ranked songs.",
        )

        chart = top10.copy()
        chart["label"] = [
            chart_label(song, artist)
            for song, artist in zip(chart["song"], chart["artist"])
        ]
        chart = chart.sort_values("overall_performance_score")

        fig = px.bar(
            chart,
            x="overall_performance_score",
            y="label",
            orientation="h",
            color="overall_performance_score",
            color_continuous_scale=PURPLE_SCALE,
            labels={
                "overall_performance_score": "Overall score",
                "label": "Song — Artist",
            },
        )
        fig.update_layout(coloraxis_showscale=False)
        style_horizontal_ranking(fig, 440)
        st.plotly_chart(fig, use_container_width=True)

    
    with right:
        card_heading(
            "Key findings",
            "Highlights from the current analytical view.",
        )

        momentum_top = filtered.sort_values(
            "average_momentum_score", ascending=False
        ).iloc[0]

        fandom_top = filtered.sort_values(
            "fandom_intensity_score", ascending=False
        ).iloc[0]

        sustainability_top = filtered.sort_values(
            "sustainability_score", ascending=False
        ).iloc[0]

        insights = [
            f"<strong>{esc(top['song'])}</strong> has the highest overall performance score in the current view.",
            f"<strong>{esc(momentum_top['song'])}</strong> has the highest average comeback momentum.",
            f"<strong>{esc(fandom_top['song'])}</strong> has the highest fandom intensity score.",
            f"<strong>{esc(sustainability_top['song'])}</strong> has the highest sustainability score.",
            f"The current view contains <strong>{reentry_events:,}</strong> detected re-entry events.",
        ]

        for item in insights:
            st.markdown(
                f'<div class="insight">{item}</div>',
                unsafe_allow_html=True,
            )

    
# ============================================================
# TOP SONGS
# ============================================================

elif page == "Top Songs":

    page_header(
        "Top Songs",
        "Explore the songs ranked by the integrated overall performance score.",
    )

    top10 = top_rows(filtered, ranking_size)

    card_heading(
        "Top Songs",
        "Album cover, artist, rank and overall performance score.",
    )

    for start in range(0, len(top10), 5):
        chunk = top10.iloc[start:start + 5]
        cols = st.columns(5, gap="small")

        for offset, (_, row) in enumerate(chunk.iterrows()):
            with cols[offset]:
                render_song_card(row, start + offset + 1)

        if start + 5 < len(top10):
            st.write("")


    st.write("")
    card_heading(
        "Detailed ranking",
        "Underlying metrics used by the dashboard.",
    )

    display_cols = [
        c for c in [
            "overall_rank",
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
        if c in top10.columns
    ]

    st.dataframe(
        top10[display_cols],
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download top-song ranking",
        top10[display_cols].to_csv(index=False).encode("utf-8"),
        "KPOP_Top_Songs_Ranking.csv",
        "text/csv",
    )


# ============================================================
# COMEBACK MOMENTUM
# ============================================================

elif page == "Comeback Momentum":

    page_header(
        "Comeback Momentum",
        "Measure the strength of a song's return after a period away from the chart.",
    )

    if momentum is None:
        st.error("The comeback momentum output file is missing.")
        st.stop()

    m = momentum.copy()

    if selected_artists:
        m = m[m["artist"].astype(str).isin(selected_artists)]

    if m.empty:
        st.warning("No momentum events match the selected filters.")
        st.stop()

    a, b, c, d = st.columns(4)
    with a:
        st.metric("Re-entry events", f"{len(m):,}")
    with b:
        st.metric("Average gap", f"{m['gap_days'].mean():.2f} days")
    with c:
        st.metric("Longest gap", f"{m['gap_days'].max():.0f} days")
    with d:
        st.metric("Songs", f"{m['song'].nunique():,}")

    section_label("Momentum analysis")

    left, right = st.columns(2, gap="large")

    with left:
        card_heading(
            "Strongest comeback events",
            "Highest event-level momentum scores.",
        )

        topm = m.sort_values(
            "momentum_score", ascending=False
        ).head(ranking_size).copy()

        topm["label"] = [
            chart_label(song, artist)
            for song, artist in zip(topm["song"], topm["artist"])
        ]

        fig = px.bar(
            topm.sort_values("momentum_score"),
            x="momentum_score",
            y="label",
            orientation="h",
            color="momentum_score",
            color_continuous_scale=PURPLE_SCALE,
            labels={
                "momentum_score": "Momentum score",
                "label": "Song — Artist",
            },
        )
        fig.update_layout(coloraxis_showscale=False)
        style_horizontal_ranking(fig, 455)
        st.plotly_chart(fig, use_container_width=True)

    
    with right:
        card_heading(
            "Gap vs. re-entry position",
            "Event-level relationship between absence duration and return position.",
        )

        fig = px.scatter(
            m,
            x="gap_days",
            y="reentry_position",
            size="momentum_score",
            color="momentum_score",
            hover_data=["song", "artist", "momentum_score"],
            color_continuous_scale=PURPLE_SCALE,
            labels={
                "gap_days": "Gap before re-entry (days)",
                "reentry_position": "Re-entry position",
                "momentum_score": "Momentum",
            },
        )
        fig.update_yaxes(autorange="reversed")
        style_plot(fig, 455)
        st.plotly_chart(fig, use_container_width=True)

    
    card_heading("Event details")

    st.dataframe(
        m.sort_values("momentum_score", ascending=False).head(50),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FANDOM INTENSITY
# ============================================================

elif page == "Fandom Intensity":

    page_header(
        "Fandom Intensity",
        "Analyse repeated appearances, chart strength and comeback momentum as a project-specific fandom signal.",
    )

    topf = top_rows(
        filtered,
        ranking_size,
        "fandom_intensity_score",
    )

    a, b, c = st.columns(3)
    with a:
        st.metric(
            "Highest score",
            f"{topf['fandom_intensity_score'].max():.4f}",
        )
    with b:
        st.metric(
            "Average score",
            f"{filtered['fandom_intensity_score'].mean():.4f}",
        )
    with c:
        st.metric(
            "Songs analysed",
            f"{len(filtered):,}",
        )

    section_label("Fandom analysis")

    left, right = st.columns(2, gap="large")

    with left:
        card_heading(
            "Top songs by fandom intensity",
            "Highest project-specific fandom intensity scores.",
        )

        chart = topf.copy()
        chart["label"] = [
            chart_label(song, artist)
            for song, artist in zip(chart["song"], chart["artist"])
        ]

        fig = px.bar(
            chart.sort_values("fandom_intensity_score"),
            x="fandom_intensity_score",
            y="label",
            orientation="h",
            color="fandom_intensity_score",
            color_continuous_scale=PURPLE_SCALE,
            labels={
                "fandom_intensity_score": "Fandom intensity",
                "label": "Song — Artist",
            },
        )
        fig.update_layout(coloraxis_showscale=False)
        style_horizontal_ranking(fig, 455)
        st.plotly_chart(fig, use_container_width=True)

    
    with right:
        card_heading(
            "Momentum vs. fandom intensity",
            "Relationship between the two analytical dimensions.",
        )

        fig = px.scatter(
            filtered,
            x="average_momentum_score",
            y="fandom_intensity_score",
            color="sustainability_score",
            hover_data=["song", "artist"],
            color_continuous_scale=PURPLE_SCALE,
            labels={
                "average_momentum_score": "Average momentum",
                "fandom_intensity_score": "Fandom intensity",
                "sustainability_score": "Sustainability",
            },
        )
        style_horizontal_ranking(fig, 455)
        st.plotly_chart(fig, use_container_width=True)

    
    if "fandom_category" in filtered.columns:
        card_heading(
            "Fandom category distribution",
            "Number of songs in each analytical category.",
        )

        counts = (
            filtered["fandom_category"]
            .value_counts()
            .rename_axis("category")
            .reset_index(name="songs")
        )

        fig = px.bar(
            counts,
            x="category",
            y="songs",
            color="songs",
            color_continuous_scale=PURPLE_SCALE,
            labels={"category": "Category", "songs": "Songs"},
        )
        fig.update_layout(coloraxis_showscale=False)
        style_plot(fig, 370)
        st.plotly_chart(fig, use_container_width=True)

    
# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":

    page_header(
        "Chart Sustainability",
        "Identify songs that combine repeated chart presence, chart strength, momentum and fandom intensity.",
    )

    tops = top_rows(
        filtered,
        ranking_size,
        "sustainability_score",
    )

    a, b, c = st.columns(3)
    with a:
        st.metric(
            "Highest sustainability",
            f"{tops['sustainability_score'].max():.4f}",
        )
    with b:
        st.metric(
            "Average sustainability",
            f"{filtered['sustainability_score'].mean():.4f}",
        )
    with c:
        st.metric(
            "Songs analysed",
            f"{len(filtered):,}",
        )

    section_label("Sustainability analysis")

    card_heading(
        "Top songs by sustainability",
        "Highest sustainability scores in the current view.",
    )

    chart = tops.copy()
    chart["label"] = [
        chart_label(song, artist)
        for song, artist in zip(chart["song"], chart["artist"])
    ]

    fig = px.bar(
        chart.sort_values("sustainability_score"),
        x="sustainability_score",
        y="label",
        orientation="h",
        color="sustainability_score",
        color_continuous_scale=PURPLE_SCALE,
        labels={
            "sustainability_score": "Sustainability score",
            "label": "Song — Artist",
        },
    )
    fig.update_layout(coloraxis_showscale=False)
    style_horizontal_ranking(fig, 470)
    st.plotly_chart(fig, use_container_width=True)


    if artist_sustainability is not None:
        a_df = artist_sustainability.copy()

        if selected_artists:
            a_df = a_df[
                a_df["artist"].astype(str).isin(selected_artists)
            ]

        if "average_sustainability_score" in a_df.columns:
            a_df["average_sustainability_score"] = pd.to_numeric(
                a_df["average_sustainability_score"],
                errors="coerce",
            )
            a_df = a_df.dropna(
                subset=["average_sustainability_score"]
            ).sort_values(
                "average_sustainability_score",
                ascending=False,
            ).head(ranking_size)

            card_heading(
                "Artist sustainability",
                "Average sustainability across songs with chart re-entry.",
            )

            fig = px.bar(
                a_df.sort_values("average_sustainability_score"),
                x="average_sustainability_score",
                y="artist",
                orientation="h",
                color="average_sustainability_score",
                color_continuous_scale=PURPLE_SCALE,
                labels={
                    "average_sustainability_score": "Sustainability",
                    "artist": "Artist",
                },
            )
            fig.update_layout(coloraxis_showscale=False)
            style_horizontal_ranking(fig, 440)
            st.plotly_chart(fig, use_container_width=True)

        
    card_heading("Sustainability detail")

    cols = [
        c for c in [
            "song",
            "artist",
            "total_reentries",
            "average_gap_days",
            "longest_gap_days",
            "best_reentry_position",
            "sustainability_score",
            "overall_performance_score",
        ]
        if c in tops.columns
    ]

    st.dataframe(
        tops[cols],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ARTIST ANALYSIS
# ============================================================

elif page == "Artist Analysis":

    page_header(
        "Artist Analysis",
        "Compare artists using re-entry frequency, comeback momentum, fandom intensity and sustainability.",
    )

    if artist_analysis is None:
        st.error("Artist analysis output file is missing.")
        st.stop()

    artists_df = artist_analysis.copy()

    if selected_artists:
        artists_df = artists_df[
            artists_df["artist"].astype(str).isin(selected_artists)
        ]

    for col in [
        "songs_with_reentry",
        "total_reentries",
        "average_momentum_score",
        "average_fandom_intensity",
        "average_sustainability_score",
    ]:
        if col in artists_df.columns:
            artists_df[col] = pd.to_numeric(
                artists_df[col], errors="coerce"
            )

    if artists_df.empty:
        st.warning("No artists match the selected filters.")
        st.stop()

    top_artists = artists_df.sort_values(
        "average_sustainability_score",
        ascending=False,
    ).head(ranking_size)

    a, b, c = st.columns(3)
    with a:
        st.metric("Artists analysed", f"{len(artists_df):,}")
    with b:
        st.metric("Top re-entry events", f"{artists_df['total_reentries'].max():,.0f}")
    with c:
        st.metric(
            "Highest sustainability",
            f"{artists_df['average_sustainability_score'].max():.4f}",
        )

    section_label("Artist performance")

    card_heading(
        "Artists by average sustainability",
        "Artist-level sustainability among songs with re-entry.",
    )

    fig = px.bar(
        top_artists.sort_values("average_sustainability_score"),
        x="average_sustainability_score",
        y="artist",
        orientation="h",
        color="average_sustainability_score",
        color_continuous_scale=PURPLE_SCALE,
        labels={
            "average_sustainability_score": "Sustainability",
            "artist": "Artist",
        },
    )
    fig.update_layout(coloraxis_showscale=False)
    style_horizontal_ranking(fig, 470)
    st.plotly_chart(fig, use_container_width=True)


    card_heading(
        "Artist momentum vs. fandom",
        "Aggregated artist-level relationship.",
    )

    fig = px.scatter(
        artists_df,
        x="average_momentum_score",
        y="average_fandom_intensity",
        size="average_sustainability_score",
        color="average_sustainability_score",
        hover_data=["artist", "total_reentries"],
        color_continuous_scale=PURPLE_SCALE,
        labels={
            "average_momentum_score": "Average momentum",
            "average_fandom_intensity": "Average fandom intensity",
            "average_sustainability_score": "Sustainability",
        },
    )
    style_plot(fig, 450)
    st.plotly_chart(fig, use_container_width=True)


    card_heading("Artist detail table")

    st.dataframe(
        artists_df.sort_values(
            "average_sustainability_score",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download artist analysis",
        artists_df.to_csv(index=False).encode("utf-8"),
        "KPOP_Artist_Analysis.csv",
        "text/csv",
    )


# ============================================================
# SONG EXPLORER
# ============================================================

elif page == "Song Explorer":

    page_header(
        "Song Explorer",
        "Inspect the complete analytical profile of any song in the integrated dataset.",
    )

    labels = (
        filtered["song"].astype(str)
        + " — "
        + filtered["artist"].astype(str)
    )

    selected = st.selectbox(
        "Select a song",
        labels.tolist(),
    )

    row = filtered.loc[labels == selected].iloc[0]
    cover = get_cover(row)

    left, right = st.columns([0.72, 1.8], gap="large")

    with left:
    
        if cover:
            st.image(cover, use_container_width=True)
        else:
            st.markdown(
                '<div class="cover-empty">KP</div>',
                unsafe_allow_html=True,
            )

    
    with right:
        st.markdown(
            f"""
            <div class="eyebrow">Selected song</div>
            <div class="page-title" style="font-size:1.7rem;">
                {esc(row["song"])}
            </div>
            <div class="page-copy">{esc(row["artist"])}</div>
            """,
            unsafe_allow_html=True,
        )

        metric_cols = st.columns(4)

        metrics = [
            ("Overall", row["overall_performance_score"]),
            ("Momentum", row["average_momentum_score"]),
            ("Fandom", row["fandom_intensity_score"]),
            ("Sustainability", row["sustainability_score"]),
        ]

        for col, (label, value) in zip(metric_cols, metrics):
            with col:
                st.markdown(
                    f"""
                    <div class="kpi">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{float(value):.4f}</div>
                        <div class="kpi-sub">Analytical score</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.write("")

    categories = [
        "Overall",
        "Momentum",
        "Fandom",
        "Sustainability",
    ]

    values = [
        float(row["overall_performance_score"]),
        float(row["average_momentum_score"]),
        float(row["fandom_intensity_score"]),
        float(row["sustainability_score"]),
    ]

    # Rescale dimensions independently for a meaningful profile display.
    max_value = max(values) if max(values) > 0 else 1
    radar = [v / max_value for v in values]
    radar += radar[:1]
    theta = categories + categories[:1]

    fig = go.Figure(
        go.Scatterpolar(
            r=radar,
            theta=theta,
            fill="toself",
            line=dict(color=PURPLE, width=2),
            fillcolor="rgba(111,58,165,.15)",
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor=WHITE,
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor=GRID,
                linecolor=BORDER,
                tickfont=dict(family="Inter, Arial, sans-serif", size=9, color="#51435A"),
            ),
            angularaxis=dict(
                gridcolor=GRID,
                linecolor=BORDER,
                tickfont=dict(family="Inter, Arial, sans-serif", size=10, color="#24152F"),
            ),
        ),
        showlegend=False,
        height=420,
        paper_bgcolor=WHITE,
        margin=dict(l=30, r=30, t=45, b=20),
        title=dict(
            text="Relative analytical profile",
            x=0,
            font=dict(size=14, color=TEXT),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    details = {
        "Total re-entries": row["total_reentries"],
        "Average gap (days)": row["average_gap_days"],
        "Longest gap (days)": row["longest_gap_days"],
        "Best re-entry position": row["best_reentry_position"],
        "Average re-entry position": row["average_reentry_position"],
        "Fandom category": row.get("fandom_category", "N/A"),
        "Performance balance": row.get("performance_balance", np.nan),
    }

    card_heading("Chart behaviour details")

    detail_df = pd.DataFrame(
        [{"Metric": k, "Value": v} for k, v in details.items()]
    )

    st.dataframe(
        detail_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "About Project":

    page_header(
        "About the Project",
        "Methodology, analytical dimensions and interpretation guidelines.",
    )

    left, right = st.columns(2, gap="large")

    with left:
        card_heading("Project objective")

        st.markdown(
            """
            This project analyses the South Korea Top 50 chart to identify
            songs that leave and later return to the chart, then measures
            comeback momentum, repeated chart behaviour, fandom intensity
            and sustainability.

            The final integrated analysis combines these dimensions into
            an overall performance score for comparative analysis.
            """
        )

    
    with right:
        card_heading("Analytical framework")

        definitions = [
            ("Chart re-entry", "A song appears again after previously leaving the tracked chart."),
            ("Comeback momentum", "A project-specific measure combining the gap before return and the re-entry position."),
            ("Fandom intensity", "A project-specific index based on repeated appearances, chart strength and momentum."),
            ("Sustainability", "A combined measure of repeated presence, chart strength, momentum and fandom intensity."),
            ("Overall performance", "An integrated score combining normalized sustainability, fandom intensity and momentum."),
        ]

        for title, definition in definitions:
            st.markdown(
                f'<div class="insight"><strong>{esc(title)}</strong><br>{esc(definition)}</div>',
                unsafe_allow_html=True,
            )

    
    card_heading(
        "Dataset summary",
        "Values from the cleaned and validated project outputs.",
    )

    summary = pd.DataFrame(
        {
            "Metric": [
                "Cleaned chart records",
                "Unique song titles",
                "Unique song-artist combinations",
                "Artists with re-entry",
                "Re-entry events",
            ],
            "Value": [
                "27,750",
                "527",
                "541",
                "118",
                len(momentum) if momentum is not None else "Available in outputs",
            ],
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )


    card_heading("Interpretation note")

    st.markdown(
        """
        The analytical scores are constructed for this project and should
        be interpreted as comparative indices within the dataset. They are
        not direct measurements of total fandom size, market share,
        revenue or commercial success.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        K-POP CHART ANALYTICS<br>
        Chart Re-Entry · Comeback Momentum · Fandom Intensity · Sustainability<br>
        Built with Python, Pandas, Plotly and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
