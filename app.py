import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request
from difflib import SequenceMatcher
import re
import html

# ============================================================
# K-POP CHART ANALYTICS — PROFESSIONAL DASHBOARD
# ============================================================

st.set_page_config(
    page_title="K-Pop Chart Analytics",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme
# -----------------------------
COLORS = {
    "bg": "#F7F5FB",
    "surface": "#FFFFFF",
    "surface_alt": "#FCFAFF",
    "border": "#E9E3F1",
    "text": "#21152B",
    "muted": "#756A7F",
    "purple": "#6D3FA3",
    "purple_dark": "#43205F",
    "purple_mid": "#8B5CC2",
    "purple_light": "#DCC9EE",
    "purple_pale": "#F0E8F8",
    "pink": "#C75C9A",
    "green": "#43816A",
    "gold": "#B58A42",
}

PURPLE_SCALE = [
    "#EEE5F6",
    "#DCC9EE",
    "#C4A9DE",
    "#A782CE",
    "#8B5CC2",
    "#6D3FA3",
    "#54267B",
    "#43205F",
]

# -----------------------------
# Clean, stable CSS
# -----------------------------
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {{
    --bg: {COLORS["bg"]};
    --surface: {COLORS["surface"]};
    --border: {COLORS["border"]};
    --text: {COLORS["text"]};
    --muted: {COLORS["muted"]};
    --purple: {COLORS["purple"]};
    --purple-dark: {COLORS["purple_dark"]};
    --purple-pale: {COLORS["purple_pale"]};
}}

html, body, [class*="css"] {{
    font-family: "DM Sans", sans-serif;
}}

.stApp {{
    background: var(--bg);
    color: var(--text);
}}

[data-testid="stSidebar"] {{
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.1rem;
}}

.block-container {{
    max-width: 1480px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}}

h1, h2, h3, h4 {{
    font-family: "Plus Jakarta Sans", sans-serif !important;
    color: var(--text);
    letter-spacing: -0.025em;
}}

h1 {{ font-size: 2.05rem !important; }}
h2 {{ font-size: 1.35rem !important; }}
h3 {{ font-size: 1.05rem !important; }}

[data-testid="stMetric"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 17px 18px;
    box-shadow: 0 5px 18px rgba(66, 32, 95, 0.045);
}}

[data-testid="stMetricLabel"] {{
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}}

[data-testid="stMetricValue"] {{
    color: var(--text) !important;
    font-family: "Plus Jakarta Sans", sans-serif !important;
    font-size: 1.55rem !important;
}}

.stButton button {{
    border-radius: 10px;
    border: 1px solid var(--border);
    background: white;
    color: var(--text);
    font-weight: 600;
}}

.stButton button:hover {{
    border-color: var(--purple);
    color: var(--purple);
}}

[data-testid="stDataFrame"] {{
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
}}

div[data-baseweb="select"] > div {{
    border-radius: 10px;
    border-color: var(--border);
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 9px;
    padding: 8px 15px;
}}

hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.3rem 0;
}}

.small-muted {{
    color: var(--muted);
    font-size: 0.84rem;
}}

.eyebrow {{
    color: var(--purple);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}}

.page-title {{
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 0.15rem;
}}

.page-subtitle {{
    color: var(--muted);
    font-size: 0.94rem;
    margin-bottom: 1.35rem;
}}

.hero {{
    background: linear-gradient(135deg, #43205F 0%, #6D3FA3 58%, #8B5CC2 100%);
    border-radius: 22px;
    padding: 32px 34px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 16px 35px rgba(67, 32, 95, 0.18);
}}

.hero-kicker {{
    color: #E9DDF3;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}}

.hero-title {{
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 2.25rem;
    font-weight: 800;
    line-height: 1.08;
    margin: 7px 0 10px;
}}

.hero-copy {{
    color: #F2EBF7;
    max-width: 760px;
    line-height: 1.6;
    font-size: 0.93rem;
}}

.section-head {{
    display: flex;
    justify-content: space-between;
    align-items: end;
    gap: 12px;
    margin: 25px 0 11px;
}}

.section-title {{
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: 1.08rem;
    font-weight: 800;
}}

.section-note {{
    color: var(--muted);
    font-size: 0.78rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 5px 18px rgba(66, 32, 95, 0.035);
}}

.rank-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 5px 18px rgba(66, 32, 95, 0.035);
}}

.rank-art {{
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    display: block;
    background: #EEE8F4;
}}

.rank-body {{
    padding: 12px 13px 14px;
}}

.rank-number {{
    color: var(--purple);
    font-weight: 800;
    font-size: 0.73rem;
}}

.rank-song {{
    color: var(--text);
    font-weight: 800;
    margin-top: 4px;
    line-height: 1.25;
}}

.rank-artist {{
    color: var(--muted);
    font-size: 0.78rem;
    margin-top: 3px;
}}

.score-pill {{
    display: inline-block;
    background: var(--purple-pale);
    color: var(--purple-dark);
    border-radius: 999px;
    padding: 4px 9px;
    font-size: 0.7rem;
    font-weight: 800;
    margin-top: 9px;
}}

.insight {{
    background: linear-gradient(135deg, #F5EFF9, #FBF9FD);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 17px 18px;
}}

.insight-title {{
    color: var(--purple-dark);
    font-weight: 800;
    margin-bottom: 5px;
}}

.insight-copy {{
    color: var(--muted);
    line-height: 1.55;
    font-size: 0.85rem;
}}

.profile-score {{
    text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 17px 10px;
}}

.profile-score-label {{
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
}}

.profile-score-value {{
    font-family: "Plus Jakarta Sans", sans-serif;
    color: var(--purple-dark);
    font-size: 1.45rem;
    font-weight: 800;
    margin-top: 3px;
}}

.footer {{
    margin-top: 38px;
    padding: 18px 0 5px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    text-align: center;
    font-size: 0.76rem;
}}

@media (max-width: 900px) {{
    .block-container {{ padding: 1rem 1rem 3rem; }}
    .hero-title {{ font-size: 1.75rem; }}
    .page-title {{ font-size: 1.65rem; }}
}}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DATA LOADING
# ============================================================

ROOT = Path(__file__).resolve().parent
SEARCH_ROOTS = [ROOT, ROOT.parent, ROOT.parent.parent, ROOT.parent.parent.parent]


def find_output(name):
    # Support both the original local project layout and the GitHub/Streamlit layout.
    for base in SEARCH_ROOTS:
        candidates = [
            base / name,
            base / "outputs" / name,
        ]
        for path in candidates:
            if path.exists():
                return path
    return None


def find_data(name):
    for base in SEARCH_ROOTS:
        candidates = [
            base / name,
            base / "data" / name,
            base / "data" / "processed" / name,
        ]
        for path in candidates:
            if path.exists():
                return path
    return None


@st.cache_data(show_spinner=False)
def load_csv(path_string):
    try:
        return pd.read_csv(path_string)
    except Exception:
        return None


def load_output(name):
    path = find_output(name)
    return load_csv(str(path)) if path else None


integrated = load_output("phase7_integrated_kpop_analysis.csv")
if integrated is None:
    integrated = load_output("KPOP_FINAL_DASHBOARD_DATA.csv")

momentum = load_output("phase4_comeback_momentum_events.csv")
fandom = load_output("phase5_fandom_intensity_song_analysis.csv")
sustainability = load_output("phase6_chart_sustainability_analysis.csv")
artist_sustainability = load_output("phase6_artist_sustainability_analysis.csv")

cleaned_path = find_data("Atlantic_South_Korea_Cleaned.csv")
raw_path = find_data("Atlantic_South_Korea.csv")

cleaned = load_csv(str(cleaned_path)) if cleaned_path else None
raw = load_csv(str(raw_path)) if raw_path else None


# ============================================================
# HELPERS
# ============================================================

REQUIRED = [
    "song",
    "artist",
    "overall_performance_score",
    "average_momentum_score",
    "fandom_intensity_score",
    "sustainability_score",
]


def safe_num(df, cols):
    if df is None:
        return
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


def normalize_text(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def nice_number(value, decimals=1):
    if pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}"


def first_existing(df, candidates):
    if df is None:
        return None
    for col in candidates:
        if col in df.columns:
            return col
    return None


def prepare_data():
    global integrated, momentum, fandom, sustainability, artist_sustainability

    if integrated is not None:
        safe_num(
            integrated,
            [
                "overall_performance_score",
                "average_momentum_score",
                "fandom_intensity_score",
                "sustainability_score",
                "total_reentries",
                "average_gap_days",
                "longest_gap_days",
                "best_reentry_position",
                "average_reentry_position",
            ],
        )

    if momentum is not None:
        safe_num(
            momentum,
            ["gap_days", "reentry_position", "momentum_score"],
        )

    if fandom is not None:
        safe_num(
            fandom,
            ["fandom_intensity_score", "average_momentum_score", "sustainability_score"],
        )

    if sustainability is not None:
        safe_num(
            sustainability,
            ["sustainability_score", "average_gap_days", "total_reentries"],
        )

    if artist_sustainability is not None:
        safe_num(
            artist_sustainability,
            [
                "sustainability_score",
                "average_momentum_score",
                "fandom_intensity_score",
            ],
        )


prepare_data()


def get_cover(song, artist):
    """Use a local cover URL first, then iTunes as a lightweight fallback."""
    datasets = [cleaned, raw]

    for df in datasets:
        if df is None or "album_cover_url" not in df.columns:
            continue

        work = df.copy()
        if "song" not in work.columns:
            continue

        song_norm = normalize_text(song)
        artist_norm = normalize_text(artist)

        work["_song_norm"] = work["song"].map(normalize_text)
        exact = work[work["_song_norm"] == song_norm]

        if "artist" in work.columns:
            exact_artist = exact[
                exact["artist"].map(normalize_text) == artist_norm
            ]
            if not exact_artist.empty:
                exact = exact_artist

        for value in exact["album_cover_url"].dropna().astype(str):
            if value.startswith(("http://", "https://")):
                return value

    # Online fallback
    try:
        query = quote(f"{song} {artist}")
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("results"):
            art = data["results"][0].get("artworkUrl100")
            if art:
                return art.replace("100x100", "600x600")
    except Exception:
        pass

    return ""


@st.cache_data(show_spinner=False)
def cached_cover(song, artist):
    return get_cover(song, artist)


def page_header(kicker, title, subtitle):
    st.markdown(
        f"""
        <div class="eyebrow">{html.escape(kicker)}</div>
        <div class="page-title">{html.escape(title)}</div>
        <div class="page-subtitle">{html.escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def section_head(title, note=""):
    note_html = f'<div class="section-note">{html.escape(note)}</div>' if note else ""
    st.markdown(
        f"""
        <div class="section-head">
            <div class="section-title">{html.escape(title)}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=38, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=COLORS["text"]),
        title_font=dict(family="Plus Jakarta Sans", size=15),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="DM Sans",
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EEE8F4",
        zeroline=False,
        linecolor="#E9E3F1",
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEE8F4",
        zeroline=False,
        linecolor="#E9E3F1",
    )
    return fig


def show_chart(fig, height=390):
    st.plotly_chart(chart_layout(fig, height), use_container_width=True, config={"displayModeBar": False})


def empty_state(message):
    st.info(message)


def filtered_integrated(selected_artists, selected_categories):
    if integrated is None:
        return None

    df = integrated.copy()

    if selected_artists and "artist" in df.columns:
        df = df[df["artist"].isin(selected_artists)]

    if selected_categories and "fandom_category" in df.columns:
        df = df[df["fandom_category"].isin(selected_categories)]

    return df


def top_cards(df, n=5):
    if df is None or df.empty:
        empty_state("No song data is available for the current filters.")
        return

    score_col = first_existing(df, ["overall_performance_score"])
    if score_col:
        work = df.sort_values(score_col, ascending=False).head(n)
    else:
        work = df.head(n)

    cols = st.columns(n)
    for idx, (_, row) in enumerate(work.iterrows()):
        with cols[idx]:
            song = str(row.get("song", "Unknown"))
            artist = str(row.get("artist", "Unknown"))
            cover = cached_cover(song, artist)
            art = (
                f'<img class="rank-art" src="{html.escape(cover)}">'
                if cover
                else '<div class="rank-art"></div>'
            )
            score = row.get("overall_performance_score", np.nan)
            st.markdown(
                f"""
                <div class="rank-card">
                    {art}
                    <div class="rank-body">
                        <div class="rank-number">#{idx + 1}</div>
                        <div class="rank-song">{html.escape(song)}</div>
                        <div class="rank-artist">{html.escape(artist)}</div>
                        <span class="score-pill">Score {nice_number(score)}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def ranking_table(df, n=10):
    if df is None or df.empty:
        empty_state("No ranking data is available.")
        return

    score = first_existing(df, ["overall_performance_score"])
    if score:
        work = df.sort_values(score, ascending=False).head(n).copy()
    else:
        work = df.head(n).copy()

    preferred = [
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
    cols = [c for c in preferred if c in work.columns]
    st.dataframe(
        work[cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "average_gap_days": st.column_config.NumberColumn("Avg gap", format="%.1f"),
            "average_momentum_score": st.column_config.NumberColumn("Momentum", format="%.1f"),
            "fandom_intensity_score": st.column_config.NumberColumn("Fandom", format="%.1f"),
            "sustainability_score": st.column_config.NumberColumn("Sustainability", format="%.1f"),
            "overall_performance_score": st.column_config.NumberColumn("Overall", format="%.1f"),
        },
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:6px 4px 18px;">
            <div style="font-size:0.7rem;font-weight:800;letter-spacing:0.12em;color:{COLORS["purple"]};">
                K-POP DATA PRODUCT
            </div>
            <div style="font-family:'Plus Jakarta Sans';font-size:1.25rem;font-weight:800;margin-top:4px;">
                Chart Analytics
            </div>
            <div class="small-muted" style="margin-top:6px;line-height:1.5;">
                Comebacks, fandom intensity and chart sustainability in one workspace.
            </div>
        </div>
        """,
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

    page = st.radio("Navigate", pages, label_visibility="collapsed")

    st.divider()

    st.markdown("**Filters**")

    all_artists = []
    if integrated is not None and "artist" in integrated.columns:
        all_artists = sorted(
            integrated["artist"].dropna().astype(str).unique().tolist()
        )

    selected_artists = st.multiselect(
        "Artist",
        all_artists,
        placeholder="All artists",
    )

    categories = []
    if integrated is not None and "fandom_category" in integrated.columns:
        categories = sorted(
            integrated["fandom_category"].dropna().astype(str).unique().tolist()
        )

    selected_categories = st.multiselect(
        "Fandom category",
        categories,
        placeholder="All categories",
    )

    ranking_size = st.slider("Ranking size", 5, 15, 10)

    st.divider()

    st.caption(
        "Scores are project-specific analytical indices. They are not direct measurements of real-world fandom size, fan count, or commercial success."
    )


df = filtered_integrated(selected_artists, selected_categories)

# ============================================================
# HOME
# ============================================================

if page == "Home":
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">South Korea Top 50 · Integrated Analysis</div>
            <div class="hero-title">K-Pop Chart Analytics</div>
            <div class="hero-copy">
                A focused view of chart re-entry, comeback momentum, fandom intensity,
                sustainability and integrated song performance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df is None or df.empty:
        empty_state("Integrated dashboard data could not be found. Place the Phase 7 integrated CSV beside this app.")
    else:
        section_head("Executive snapshot", "Current filter selection")

        songs = df["song"].nunique() if "song" in df.columns else len(df)
        artists = df["artist"].nunique() if "artist" in df.columns else 0
        reentries = (
            int(df["total_reentries"].sum())
            if "total_reentries" in df.columns
            else (len(momentum) if momentum is not None else 0)
        )
        avg_gap = (
            df["average_gap_days"].mean()
            if "average_gap_days" in df.columns
            else np.nan
        )
        top_name = (
            df.sort_values("overall_performance_score", ascending=False).iloc[0]["song"]
            if "overall_performance_score" in df.columns and not df.empty
            else "—"
        )

        k = st.columns(5)
        k[0].metric("Songs", f"{songs:,}")
        k[1].metric("Artists", f"{artists:,}")
        k[2].metric("Re-entry events", f"{reentries:,}")
        k[3].metric("Average gap", f"{nice_number(avg_gap)} days")
        k[4].metric("Top performer", str(top_name)[:24])

        section_head("Top performers", "Integrated performance score")
        top_cards(df, min(5, len(df)))

        c1, c2 = st.columns([1.15, 1])
        with c1:
            section_head("Overall performance", "Highest integrated scores")
            work = df.sort_values("overall_performance_score", ascending=False).head(ranking_size)
            fig = px.bar(
                work.sort_values("overall_performance_score"),
                x="overall_performance_score",
                y="song",
                orientation="h",
                color="overall_performance_score",
                color_continuous_scale=PURPLE_SCALE,
                hover_data=["artist"],
            )
            fig.update_layout(coloraxis_showscale=False)
            show_chart(fig, 430)

        with c2:
            section_head("Momentum × fandom", "Each point represents a song")
            x = "average_momentum_score"
            y = "fandom_intensity_score"
            if x in df.columns and y in df.columns:
                fig = px.scatter(
                    df,
                    x=x,
                    y=y,
                    hover_name="song",
                    hover_data=["artist"],
                    size="sustainability_score" if "sustainability_score" in df.columns else None,
                    color="sustainability_score" if "sustainability_score" in df.columns else None,
                    color_continuous_scale=PURPLE_SCALE,
                )
                show_chart(fig, 430)
            else:
                empty_state("Momentum and fandom fields are not available.")

        section_head("Project insights", "Read the indices together")
        i1, i2, i3 = st.columns(3)
        with i1:
            st.markdown(
                """
                <div class="insight">
                    <div class="insight-title">Comeback momentum</div>
                    <div class="insight-copy">
                        Measures how strongly songs return to the chart after an absence,
                        using the project’s comeback-event analysis.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with i2:
            st.markdown(
                """
                <div class="insight">
                    <div class="insight-title">Fandom intensity</div>
                    <div class="insight-copy">
                        Combines the project’s selected chart-behaviour signals into a
                        song-level fandom intensity index.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with i3:
            st.markdown(
                """
                <div class="insight">
                    <div class="insight-title">Sustainability</div>
                    <div class="insight-copy">
                        Captures the project’s view of how consistently a song or artist
                        maintains chart presence over time.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================
# TOP SONGS
# ============================================================

elif page == "Top Songs":
    page_header(
        "RANKINGS",
        "Top Songs",
        "Explore the strongest songs across the integrated project score.",
    )

    if df is None or df.empty:
        empty_state("No integrated song data is available.")
    else:
        section_head("Top performers", f"Top {ranking_size} by overall score")
        top_cards(df, min(5, len(df)))

        st.divider()

        section_head("Detailed ranking", "All major analytical dimensions")
        ranking_table(df, ranking_size)

        csv = (
            df.sort_values("overall_performance_score", ascending=False)
            .to_csv(index=False)
            .encode("utf-8")
        )
        st.download_button(
            "Download filtered ranking CSV",
            csv,
            "kpop_filtered_ranking.csv",
            "text/csv",
        )

# ============================================================
# COMEBACK MOMENTUM
# ============================================================

elif page == "Comeback Momentum":
    page_header(
        "RE-ENTRY ANALYSIS",
        "Comeback Momentum",
        "Understand when songs leave the chart, return, and how strong those returns are.",
    )

    if momentum is None or momentum.empty:
        empty_state("Phase 4 momentum data could not be found.")
    else:
        m = momentum.copy()
        if selected_artists and "artist" in m.columns:
            m = m[m["artist"].isin(selected_artists)]

        if m.empty:
            empty_state("No comeback events match the selected artist filter.")
        else:
            section_head("Momentum snapshot")
            k = st.columns(4)
            k[0].metric("Re-entry events", f"{len(m):,}")
            k[1].metric("Average gap", f"{nice_number(m['gap_days'].mean())} days" if "gap_days" in m else "—")
            k[2].metric("Longest gap", f"{nice_number(m['gap_days'].max())} days" if "gap_days" in m else "—")
            k[3].metric("Songs", f"{m['song'].nunique():,}" if "song" in m else "—")

            c1, c2 = st.columns(2)
            with c1:
                section_head("Strongest comeback events", "Top momentum scores")
                if "momentum_score" in m.columns:
                    work = m.sort_values("momentum_score", ascending=False).head(15)
                    label = work["song"].astype(str) + " — " + work["artist"].astype(str)
                    fig = px.bar(
                        work.assign(label=label).sort_values("momentum_score"),
                        x="momentum_score",
                        y="label",
                        orientation="h",
                        color="momentum_score",
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    show_chart(fig, 470)
                else:
                    empty_state("Momentum score column is not available.")

            with c2:
                section_head("Gap vs re-entry position", "Chart return behaviour")
                if {"gap_days", "reentry_position"}.issubset(m.columns):
                    fig = px.scatter(
                        m,
                        x="gap_days",
                        y="reentry_position",
                        hover_name="song",
                        hover_data=["artist"],
                        color="momentum_score" if "momentum_score" in m.columns else None,
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    fig.update_yaxes(autorange="reversed")
                    show_chart(fig, 470)
                else:
                    empty_state("Required momentum fields are not available.")

            section_head("Event-level detail", "Every detected comeback event")
            cols = [
                c for c in
                ["song", "artist", "previous_date", "reentry_date", "gap_days", "reentry_position", "momentum_score"]
                if c in m.columns
            ]
            st.dataframe(m[cols], use_container_width=True, hide_index=True)

# ============================================================
# FANDOM INTENSITY
# ============================================================

elif page == "Fandom Intensity":
    page_header(
        "FANDOM SIGNALS",
        "Fandom Intensity",
        "Inspect the project’s song-level fandom intensity index and its relationship with comeback behaviour.",
    )

    if fandom is None or fandom.empty:
        empty_state("Phase 5 fandom analysis data could not be found.")
    else:
        f = fandom.copy()
        if selected_artists and "artist" in f.columns:
            f = f[f["artist"].isin(selected_artists)]

        if f.empty:
            empty_state("No fandom records match the selected artist filter.")
        else:
            score = first_existing(f, ["fandom_intensity_score"])
            if score is None:
                empty_state("Fandom intensity score column is not available.")
            else:
                section_head("Fandom snapshot")
                k = st.columns(3)
                k[0].metric("Highest score", nice_number(f[score].max()))
                k[1].metric("Average score", nice_number(f[score].mean()))
                k[2].metric("Songs analyzed", f["song"].nunique() if "song" in f else len(f))

                c1, c2 = st.columns(2)
                with c1:
                    section_head("Highest fandom intensity", "Top songs")
                    work = f.sort_values(score, ascending=False).head(15)
                    label = work["song"].astype(str)
                    fig = px.bar(
                        work.sort_values(score),
                        x=score,
                        y=label,
                        orientation="h",
                        color=score,
                        color_continuous_scale=PURPLE_SCALE,
                        hover_data=["artist"] if "artist" in work.columns else None,
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    show_chart(fig, 470)

                with c2:
                    section_head("Momentum × fandom", "Sustainability shown by colour")
                    if "average_momentum_score" in f.columns:
                        fig = px.scatter(
                            f,
                            x="average_momentum_score",
                            y=score,
                            hover_name="song",
                            hover_data=["artist"] if "artist" in f.columns else None,
                            size="sustainability_score" if "sustainability_score" in f.columns else None,
                            color="sustainability_score" if "sustainability_score" in f.columns else None,
                            color_continuous_scale=PURPLE_SCALE,
                        )
                        show_chart(fig, 470)
                    else:
                        empty_state("Average momentum score is not available.")

                if "fandom_category" in f.columns:
                    section_head("Fandom category distribution", "Project-defined categories")
                    counts = f["fandom_category"].value_counts().reset_index()
                    counts.columns = ["category", "songs"]
                    fig = px.bar(
                        counts,
                        x="category",
                        y="songs",
                        color="songs",
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    show_chart(fig, 360)

                section_head("Song-level detail")
                cols = [
                    c for c in
                    ["song", "artist", score, "average_momentum_score", "sustainability_score", "fandom_category"]
                    if c in f.columns
                ]
                st.dataframe(f[cols].sort_values(score, ascending=False), use_container_width=True, hide_index=True)

# ============================================================
# SUSTAINABILITY
# ============================================================

elif page == "Sustainability":
    page_header(
        "LONGEVITY",
        "Chart Sustainability",
        "See which songs and artists maintain chart presence most consistently in the project.",
    )

    if sustainability is None or sustainability.empty:
        empty_state("Phase 6 song sustainability data could not be found.")
    else:
        s = sustainability.copy()
        if selected_artists and "artist" in s.columns:
            s = s[s["artist"].isin(selected_artists)]

        score = first_existing(s, ["sustainability_score"])

        if s.empty or score is None:
            empty_state("No sustainability records match the current filters.")
        else:
            section_head("Sustainability snapshot")
            top_row = s.sort_values(score, ascending=False).iloc[0]
            k = st.columns(3)
            k[0].metric("Highest score", nice_number(s[score].max()))
            k[1].metric("Average score", nice_number(s[score].mean()))
            k[2].metric("Top song", str(top_row.get("song", "—"))[:26])

            c1, c2 = st.columns(2)
            with c1:
                section_head("Song sustainability", "Highest project scores")
                work = s.sort_values(score, ascending=False).head(15)
                fig = px.bar(
                    work.sort_values(score),
                    x=score,
                    y="song",
                    orientation="h",
                    color=score,
                    color_continuous_scale=PURPLE_SCALE,
                    hover_data=["artist"] if "artist" in work.columns else None,
                )
                fig.update_layout(coloraxis_showscale=False)
                show_chart(fig, 470)

            with c2:
                section_head("Sustainability vs momentum", "Song-level relationship")
                if "average_momentum_score" in s.columns:
                    fig = px.scatter(
                        s,
                        x="average_momentum_score",
                        y=score,
                        hover_name="song",
                        hover_data=["artist"] if "artist" in s.columns else None,
                        color=score,
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    show_chart(fig, 470)
                else:
                    empty_state("Momentum data is not available in the sustainability file.")

            section_head("Artist sustainability")
            if artist_sustainability is not None and not artist_sustainability.empty:
                a = artist_sustainability.copy()
                if selected_artists and "artist" in a.columns:
                    a = a[a["artist"].isin(selected_artists)]

                ascore = first_existing(a, ["sustainability_score"])
                if ascore:
                    work = a.sort_values(ascore, ascending=False).head(15)
                    fig = px.bar(
                        work.sort_values(ascore),
                        x=ascore,
                        y="artist",
                        orientation="h",
                        color=ascore,
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    show_chart(fig, 420)
                else:
                    st.info("Artist sustainability score column is not available.")
            else:
                st.info("Artist sustainability file is optional and was not found.")

# ============================================================
# ARTIST ANALYSIS
# ============================================================

elif page == "Artist Analysis":
    page_header(
        "ARTIST VIEW",
        "Artist Analysis",
        "Compare artist-level sustainability and the project’s supporting momentum and fandom signals.",
    )

    if artist_sustainability is None or artist_sustainability.empty:
        empty_state("Artist sustainability data could not be found.")
    else:
        a = artist_sustainability.copy()
        if selected_artists and "artist" in a.columns:
            a = a[a["artist"].isin(selected_artists)]

        if a.empty:
            empty_state("No artist records match the current filter.")
        else:
            score = first_existing(a, ["sustainability_score"])
            if score is None:
                empty_state("Artist sustainability score column is not available.")
            else:
                artists = sorted(a["artist"].dropna().astype(str).unique())
                selected = st.selectbox("Select an artist", artists)

                row = a[a["artist"].astype(str) == selected].iloc[0]

                section_head("Selected artist", selected)
                k = st.columns(4)
                k[0].metric("Sustainability", nice_number(row.get(score, np.nan)))
                k[1].metric(
                    "Momentum",
                    nice_number(row.get("average_momentum_score", np.nan)),
                )
                k[2].metric(
                    "Fandom",
                    nice_number(row.get("fandom_intensity_score", np.nan)),
                )
                k[3].metric(
                    "Songs",
                    str(row.get("song_count", row.get("songs", "—"))),
                )

                c1, c2 = st.columns([1, 1])
                with c1:
                    section_head("Artist score profile")
                    labels = []
                    values = []
                    for label, col in [
                        ("Sustainability", score),
                        ("Momentum", "average_momentum_score"),
                        ("Fandom", "fandom_intensity_score"),
                    ]:
                        if col in row.index and pd.notna(row[col]):
                            labels.append(label)
                            values.append(float(row[col]))

                    if values:
                        fig = go.Figure(
                            go.Scatterpolar(
                                r=values + [values[0]],
                                theta=labels + [labels[0]],
                                fill="toself",
                                line=dict(color=COLORS["purple"], width=2),
                            )
                        )
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(showticklabels=True, gridcolor="#E9E3F1"),
                                angularaxis=dict(gridcolor="#E9E3F1"),
                            ),
                            showlegend=False,
                        )
                        show_chart(fig, 390)
                    else:
                        empty_state("Not enough artist-level score data for a profile chart.")

                with c2:
                    section_head("Artist comparison", "Sustainability score")
                    work = a.sort_values(score, ascending=False).head(ranking_size)
                    fig = px.bar(
                        work.sort_values(score),
                        x=score,
                        y="artist",
                        orientation="h",
                        color=score,
                        color_continuous_scale=PURPLE_SCALE,
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    show_chart(fig, 390)

                section_head("Artist dataset")
                st.dataframe(a, use_container_width=True, hide_index=True)

# ============================================================
# SONG EXPLORER
# ============================================================

elif page == "Song Explorer":
    page_header(
        "DEEP DIVE",
        "Song Explorer",
        "Open a single song profile and inspect its four core analytical dimensions.",
    )

    if df is None or df.empty or "song" not in df.columns:
        empty_state("Integrated song data is not available.")
    else:
        options = (
            df[["song", "artist"]]
            .drop_duplicates()
            .assign(label=lambda x: x["song"].astype(str) + " — " + x["artist"].astype(str))
        )
        labels = options["label"].tolist()

        selected_label = st.selectbox("Choose a song", labels)

        selected_row = options[options["label"] == selected_label].iloc[0]
        song = selected_row["song"]
        artist = selected_row["artist"]

        row = df[
            (df["song"].astype(str) == str(song))
            & (df["artist"].astype(str) == str(artist))
        ].iloc[0]

        cover = cached_cover(str(song), str(artist))

        left, right = st.columns([0.32, 0.68])

        with left:
            if cover:
                st.image(cover, use_container_width=True)
            st.markdown(
                f"""
                <div style="margin-top:12px;">
                    <div class="eyebrow">Song profile</div>
                    <div style="font-family:'Plus Jakarta Sans';font-size:1.45rem;font-weight:800;">
                        {html.escape(str(song))}
                    </div>
                    <div class="small-muted" style="margin-top:4px;">
                        {html.escape(str(artist))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            section_head("Core scores", "Integrated analytical profile")
            score_items = [
                ("Overall", "overall_performance_score"),
                ("Momentum", "average_momentum_score"),
                ("Fandom", "fandom_intensity_score"),
                ("Sustainability", "sustainability_score"),
            ]
            cols = st.columns(4)
            for col, (label, key) in zip(cols, score_items):
                with col:
                    value = row.get(key, np.nan)
                    st.markdown(
                        f"""
                        <div class="profile-score">
                            <div class="profile-score-label">{label}</div>
                            <div class="profile-score-value">{nice_number(value)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            section_head("Score profile")
            labels = []
            values = []
            for label, key in score_items[1:]:
                value = row.get(key, np.nan)
                if pd.notna(value):
                    labels.append(label)
                    values.append(float(value))

            if values:
                fig = go.Figure(
                    go.Scatterpolar(
                        r=values + [values[0]],
                        theta=labels + [labels[0]],
                        fill="toself",
                        line=dict(color=COLORS["purple"], width=2),
                        fillcolor="rgba(109,63,163,0.18)",
                    )
                )
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(showgrid=True, gridcolor="#E9E3F1"),
                        angularaxis=dict(gridcolor="#E9E3F1"),
                    ),
                    showlegend=False,
                )
                show_chart(fig, 390)

        section_head("Chart behaviour")
        details = {}
        for label, key in [
            ("Total re-entries", "total_reentries"),
            ("Average gap days", "average_gap_days"),
            ("Longest gap days", "longest_gap_days"),
            ("Best re-entry position", "best_reentry_position"),
            ("Average re-entry position", "average_reentry_position"),
        ]:
            if key in row.index:
                details[label] = row[key]

        if details:
            detail_df = pd.DataFrame(
                {"Metric": list(details.keys()), "Value": list(details.values())}
            )
            st.dataframe(detail_df, use_container_width=True, hide_index=True)
        else:
            st.info("Detailed chart-behaviour fields are not available.")

# ============================================================
# ABOUT
# ============================================================

else:
    page_header(
        "PROJECT",
        "About the Analysis",
        "A concise explanation of what this dashboard measures and how to interpret it.",
    )

    c1, c2 = st.columns([1.15, 0.85])

    with c1:
        section_head("Project objective")
        st.markdown(
            """
            <div class="card">
                <p style="line-height:1.7;color:#756A7F;margin-top:0;">
                    This project analyzes songs appearing in the South Korea Top 50
                    playlist and combines chart re-entry behaviour with comeback
                    momentum, fandom intensity and chart sustainability.
                </p>
                <p style="line-height:1.7;color:#756A7F;margin-bottom:0;">
                    The dashboard is designed to make the analytical pipeline easier
                    to explore, compare and communicate.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        section_head("Five analytical dimensions")
        dimensions = [
            ("01", "Chart re-entry", "Identifies songs returning after an absence."),
            ("02", "Comeback momentum", "Quantifies the project’s return-strength signal."),
            ("03", "Fandom intensity", "Summarizes the project-defined fandom signal."),
            ("04", "Chart sustainability", "Measures continued chart presence in the project."),
            ("05", "Integrated performance", "Combines the project’s core dimensions into one score."),
        ]
        for num, title, copy in dimensions:
            st.markdown(
                f"""
                <div class="card" style="margin-bottom:9px;padding:14px 16px;">
                    <span style="color:{COLORS["purple"]};font-weight:800;">{num}</span>
                    <span style="font-weight:800;margin-left:10px;">{title}</span>
                    <div class="small-muted" style="margin-top:4px;margin-left:33px;">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c2:
        section_head("Interpretation note")
        st.markdown(
            """
            <div class="insight">
                <div class="insight-title">Use the scores as analytical indices</div>
                <div class="insight-copy">
                    The project-specific scores should be interpreted within this
                    dataset and methodology. They are not direct measurements of
                    real-world fan counts, total audience size, market share,
                    commercial revenue, or universal popularity.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        section_head("Data availability")
        if integrated is not None:
            st.success(f"Integrated dataset loaded · {len(integrated):,} rows")
        else:
            st.warning("Integrated dataset not found.")

        if momentum is not None:
            st.success(f"Momentum dataset loaded · {len(momentum):,} rows")
        else:
            st.warning("Momentum dataset not found.")

        if fandom is not None:
            st.success(f"Fandom dataset loaded · {len(fandom):,} rows")
        else:
            st.warning("Fandom dataset not found.")

        if sustainability is not None:
            st.success(f"Sustainability dataset loaded · {len(sustainability):,} rows")
        else:
            st.warning("Sustainability dataset not found.")

    section_head("Technology")
    tech = st.columns(4)
    tech[0].metric("Python", "Core")
    tech[1].metric("Pandas", "Data")
    tech[2].metric("Plotly", "Charts")
    tech[3].metric("Streamlit", "Dashboard")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <b>K-POP CHART ANALYTICS</b> · Comeback Momentum · Chart Re-Entry ·
        Fandom Intensity · Sustainability<br>
        Built with Python, Pandas, Plotly and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)

