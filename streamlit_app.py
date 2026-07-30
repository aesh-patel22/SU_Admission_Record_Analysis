import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False

st.set_page_config(
    page_title="Sarvajanik University Analytics",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# ====================== PREMIUM GLASSMORPHISM CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

    /* ── Root & Background ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #020818 0%, #0b1437 40%, #0e1f3d 70%, #071426 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0; z-index: 0;
        background:
            radial-gradient(ellipse 800px 600px at 15% 20%, rgba(56,132,255,0.12) 0%, transparent 70%),
            radial-gradient(ellipse 600px 500px at 85% 75%, rgba(139,92,246,0.10) 0%, transparent 70%),
            radial-gradient(ellipse 500px 400px at 50% 50%, rgba(20,184,166,0.05) 0%, transparent 60%);
        pointer-events: none;
    }
    [data-testid="stAppViewContainer"] > .main { background: transparent !important; }
    .main .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1400px;
        position: relative; z-index: 1;
    }

    /* ── Global Typography ── */
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700; }
    h1 {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #34d399 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.4rem; letter-spacing: -0.5px; line-height: 1.2;
        margin-bottom: 0.3rem;
    }
    h2 { color: #94a3b8; font-size: 1.1rem; font-weight: 400; }
    /* Only color text nodes that aren't already styled */
    .stMarkdown p, .stText { color: #cbd5e1; }

    /* ── Sidebar always visible ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060e24 0%, #0a1628 100%) !important;
        backdrop-filter: blur(24px) saturate(180%);
        border-right: 1px solid rgba(96,165,250,0.18) !important;
        min-width: 240px !important;
        width: 240px !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

    /* ── Kill EVERY variant of the collapse/expand toggle ── */
    [data-testid="collapsedControl"]          { display: none !important; visibility: hidden !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; visibility: hidden !important; }
    button[kind="header"]                     { display: none !important; }
    .st-emotion-cache-1egp75o,
    .st-emotion-cache-1li7dat,
    .st-emotion-cache-po3384,
    [class*="collapsedControl"]               { display: none !important; }
    body > div > div > section:first-of-type ~ div > button,
    [data-testid="stAppViewContainer"] > div > button { display: none !important; }

    section[data-testid="stSidebar"] { transform: none !important; visibility: visible !important; }

    /* ── Radio nav items ── */
    .stRadio > div { gap: 4px !important; }
    .stRadio > div > label {
        display: flex !important;
        align-items: center !important;
        color: #94a3b8 !important;
        padding: 11px 16px !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
        width: 100% !important;
    }
    .stRadio > div > label:hover {
        background: rgba(96,165,250,0.10) !important;
        color: #e2e8f0 !important;
        border-color: rgba(96,165,250,0.15) !important;
    }
    .stRadio > div > label[data-baseweb="radio"]:has(input:checked),
    .stRadio > div > label:has(> div > input:checked) {
        background: rgba(96,165,250,0.15) !important;
        color: #60a5fa !important;
        border-color: rgba(96,165,250,0.3) !important;
    }
    .stRadio > div > label > div:first-child { display: none !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: inherit !important; margin: 0 !important; font-size: inherit !important; }

    /* ── Glass Cards ── */
    .glass-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(24px) saturate(160%);
        -webkit-backdrop-filter: blur(24px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px 22px 24px;
        box-shadow:
            0 4px 24px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.06);
        transition: transform 0.35s cubic-bezier(.22,.68,0,1.2), box-shadow 0.35s ease, border-color 0.3s ease;
        text-align: center;
        position: relative; overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    }
    .glass-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(96,165,250,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
        border-color: rgba(96,165,250,0.25);
    }
    .glass-card .card-label {
        font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: #64748b; margin-bottom: 10px;
    }
    .glass-card .card-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.4rem; font-weight: 800; line-height: 1.1;
        letter-spacing: -1px;
    }
    .glass-card .card-sub {
        font-size: 0.78rem; color: #475569; margin-top: 6px;
    }

    /* ── Accent Colors per Card ── */
    .card-blue  .card-value { color: #60a5fa; text-shadow: 0 0 30px rgba(96,165,250,0.5); }
    .card-green .card-value { color: #34d399; text-shadow: 0 0 30px rgba(52,211,153,0.5); }
    .card-amber .card-value { color: #fbbf24; text-shadow: 0 0 30px rgba(251,191,36,0.5); }
    .card-violet .card-value { color: #a78bfa; text-shadow: 0 0 30px rgba(167,139,250,0.5); }

    /* ── Section Headers ── */
    .section-label {
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: #60a5fa;
        margin-bottom: 6px; display: block;
    }
    .divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(96,165,250,0.4), rgba(167,139,250,0.3), transparent);
        margin: 28px 0;
        border: none;
    }

    /* ── Plotly Chart Wrapper ── */
    .chart-glass {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 6px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        overflow: hidden;
    }

    /* ── Streamlit overrides ── */
    .stSuccess {
        background: rgba(52,211,153,0.08) !important;
        border: 1px solid rgba(52,211,153,0.25) !important;
        border-radius: 14px !important;
        color: #34d399 !important;
    }
    .stInfo {
        background: rgba(96,165,250,0.08) !important;
        border: 1px solid rgba(96,165,250,0.2) !important;
        border-radius: 14px !important;
        color: #93c5fd !important;
    }
    .stMetric {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
    }
    .stMetric label { color: #64748b !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.08em; }
    .stMetric [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 800 !important; }

    .stSlider > label { color: #94a3b8 !important; font-weight: 500 !important; }
    .stSlider [data-baseweb="slider"] > div { background: rgba(96,165,250,0.2) !important; }

    /* Hide default Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; height: 0 !important; }
    .stDeployButton { display: none !important; }

    [data-testid="collapsedControl"]          { display: none !important; opacity: 0 !important; pointer-events: none !important; width: 0 !important; height: 0 !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; opacity: 0 !important; pointer-events: none !important; }
    button[aria-label="Close sidebar"]        { display: none !important; }
    button[aria-label="Open sidebar"]         { display: none !important; }
    button[aria-label="collapse sidebar"]     { display: none !important; }
    button[aria-label="expand sidebar"]       { display: none !important; }
    .st-emotion-cache-1egp75o { display: none !important; }
    .st-emotion-cache-1li7dat  { display: none !important; }
    .st-emotion-cache-po3384   { display: none !important; }
    .st-emotion-cache-czk5ss   { display: none !important; }
    [class*="collapsedControl"] { display: none !important; }
    .material-symbols-rounded  { display: none !important; font-size: 0 !important; }
    span[data-testid="stIconMaterial"] { display: none !important; }
    /* ── Flyout Submenu for Year Wise Breakdown ──
       The nav button itself is the only visible box (styled identically to
       every other nav item). This wrapper just anchors the hidden submenu
       and reveals it on hover, with no extra visible box or arrow. */
    .year-menu-wrapper {
        position: relative;
        height: 0;
        overflow: visible;
    }
    .year-menu-l1 {
        display: none;
        position: absolute;
        top: -46px;
        left: calc(100% + 4px);
        width: 190px;
        background: #09152b;
        border: 1px solid rgba(96,165,250,0.3);
        border-radius: 14px;
        padding: 6px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.6);
        z-index: 99999;
    }
    [data-testid="stSidebar"] .stButton:last-of-type:hover + .element-container .year-menu-l1,
    .year-menu-l1:hover {
        display: block;
    }
    .year-item-l1 {
        position: relative;
        padding: 8px 12px;
        border-radius: 8px;
        color: #cbd5e1;
        font-size: 0.84rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s ease;
    }
    .year-item-l1:hover {
        background: rgba(96,165,250,0.2);
        color: #60a5fa;
    }
    .year-menu-l2 {
        display: none;
        position: absolute;
        top: -4px;
        left: calc(100% + 4px);
        width: 200px;
        background: #0b1a36;
        border: 1px solid rgba(96,165,250,0.3);
        border-radius: 14px;
        padding: 6px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.6);
        z-index: 100000;
    }
    .year-item-l1:hover .year-menu-l2 {
        display: block;
    }
    .metric-item-l2 {
        padding: 8px 10px;
        border-radius: 8px;
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none !important;
        display: block;
        transition: all 0.15s ease;
    }
    .metric-item-l2:hover {
        background: rgba(96,165,250,0.25);
        color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Remove the sidebar collapse button from the DOM via JS
st.markdown("""
<script>
(function nukeSidebarToggle() {
    function hide(el) {
        el.style.cssText += 'display:none!important;visibility:hidden!important;width:0!important;height:0!important;opacity:0!important;pointer-events:none!important;';
    }
    function nuke() {
        document.querySelectorAll('button').forEach(btn => {
            const txt = (btn.innerText || btn.textContent || '');
            if (txt.includes('keyboard_double') || txt.trim() === 'keyboard_double_arrow_left' || txt.trim() === 'keyboard_double_arrow_right') {
                hide(btn);
            }
        });
        ['collapsedControl','stSidebarCollapsedControl','stHeader'].forEach(id => {
            document.querySelectorAll('[data-testid="' + id + '"]').forEach(hide);
        });
        ['Close sidebar','Open sidebar','collapse sidebar','expand sidebar'].forEach(label => {
            document.querySelectorAll('button[aria-label="' + label + '"]').forEach(hide);
        });
        document.querySelectorAll('span').forEach(span => {
            const txt = (span.innerText || span.textContent || '').trim();
            if (txt === 'keyboard_double_arrow_left' || txt === 'keyboard_double_arrow_right' || txt.startsWith('keyboard_double')) {
                hide(span);
                if (span.parentElement) hide(span.parentElement);
            }
        });
    }
    nuke();
    setTimeout(nuke, 100);
    setTimeout(nuke, 500);
    setTimeout(nuke, 1500);
    new MutationObserver(nuke).observe(document.documentElement, {childList: true, subtree: true});
})();
</script>
""", unsafe_allow_html=True)

# ====================== CHART THEME (cached as module-level constants) ======================
_AXIS_STYLE = dict(
    gridcolor='rgba(255,255,255,0.05)',
    linecolor='rgba(255,255,255,0.1)',
    tickcolor='rgba(255,255,255,0.1)',
)
_LAYOUT_BASE = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#94a3b8', size=12),
    title_font=dict(family='Space Grotesk', color='#e2e8f0', size=16),
    legend=dict(bgcolor='rgba(255,255,255,0.04)', bordercolor='rgba(255,255,255,0.08)', borderwidth=1),
    margin=dict(l=16, r=16, t=48, b=16),
    hoverlabel=dict(bgcolor='rgba(15,23,42,0.95)', bordercolor='rgba(96,165,250,0.3)', font_color='#e2e8f0'),
)
COLORS = ['#60a5fa', '#a78bfa', '#34d399', '#fbbf24', '#f472b6', '#38bdf8', '#fb923c', '#4ade80']


def apply_layout(fig, height=500, xaxis_extra=None, yaxis_extra=None):
    """Apply shared dark theme."""
    xaxis = {**_AXIS_STYLE, **(xaxis_extra or {})}
    yaxis = {**_AXIS_STYLE, **(yaxis_extra or {})}
    fig.update_layout(height=height, xaxis=xaxis, yaxis=yaxis, **_LAYOUT_BASE)


def wrap_chart(fig, height=500, xaxis_extra=None, yaxis_extra=None):
    """Apply shared dark theme + wrap in glass div."""
    apply_layout(fig, height=height, xaxis_extra=xaxis_extra, yaxis_extra=yaxis_extra)
    st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)


# ====================== OPTIMIZED DATA LOADING ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV files (fast) — created by convert_data.py
_CSV_FILES = [
    (os.path.join(BASE_DIR, "data", "admission_2023_24.csv"), "2023"),
    (os.path.join(BASE_DIR, "data", "admission_2024_25.csv"), "2024"),
    (os.path.join(BASE_DIR, "data", "admission_2025_26.csv"), "2025"),
    (os.path.join(BASE_DIR, "data", "admission_2026_27.csv"), "2026"),
]

# XLS files (slow fallback) — original files
_XLS_FILES = [
    (os.path.join(BASE_DIR, "20260106153152255_Admission 2023 24.xls"), "2023"),
    (os.path.join(BASE_DIR, "20260106153439552_Admission 2024 25.xls"), "2024"),
    (os.path.join(BASE_DIR, "20260106153808096_Admission 2025 26.xls"), "2025"),
    (os.path.join(BASE_DIR, "20260106153841088_Admission 2026 27.xls"), "2026"),
]


@st.cache_data(show_spinner="Loading admission data…")
def load_all_data():
    """Load data from CSV (fast) or XLS (slow fallback). Auto-saves CSV on first XLS load."""
    dfs = []

    # ── Try CSV first (10-50x faster than XLS) ──
    for path, year in _CSV_FILES:
        if os.path.exists(path):
            try:
                df_temp = pd.read_csv(path, low_memory=False)
                df_temp['Year'] = year
                dfs.append(df_temp)
            except Exception:
                pass

    if dfs:
        return pd.concat(dfs, ignore_index=True)

    # ── Fallback: Read XLS and auto-save as CSV for next time ──
    data_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_names = [
        "admission_2023_24.csv",
        "admission_2024_25.csv",
        "admission_2025_26.csv",
        "admission_2026_27.csv",
    ]

    for (xls_path, year), csv_name in zip(_XLS_FILES, csv_names):
        if os.path.exists(xls_path):
            try:
                df_temp = pd.read_excel(xls_path, header=3, engine='xlrd')
                df_temp['Year'] = year
                dfs.append(df_temp)
                # Auto-save CSV so next load is instant
                try:
                    df_temp.to_csv(os.path.join(data_dir, csv_name), index=False)
                except Exception:
                    pass
            except Exception:
                pass

    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    if 'City' in df.columns:
        df['City'] = df['City'].astype(str).str.strip().str.title()
        df['City'] = df['City'].replace(
            {'Suart': 'Surat', 'SURAT': 'Surat', 'surat': 'Surat', 'Suarat': 'Surat', 'Surat City': 'Surat'}
        )
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('Inquiry').astype(str)

    # ---- Single source of truth for "is this admission confirmed?" ----
    # NOTE: 'Status' only ever holds Submitted / Inquiry / Not Submitted — it
    # never contains the word "Confirmed", so checks against Status alone
    # always evaluate to 0. The real signal is the dedicated 'Confirmed'
    # column (Yes/No), falling back to 'Confirmation Date' being filled in,
    # and only then to a text search on Status for older/other datasets.
    if 'Confirmed' in df.columns:
        df['_IsConfirmed'] = df['Confirmed'].astype(str).str.strip().str.lower().isin(['yes', 'true', '1'])
    elif 'Confirmation Date' in df.columns:
        df['_IsConfirmed'] = df['Confirmation Date'].notna()
    elif 'Status' in df.columns:
        df['_IsConfirmed'] = df['Status'].str.contains('Confirmed|Confirm|Admitted', na=False, case=False)
    else:
        df['_IsConfirmed'] = False
    return df


@st.cache_data(show_spinner=False)
def compute_kpis(df: pd.DataFrame):
    if df.empty:
        return 0, 0, 0
    total = len(df)
    if 'Status' in df.columns:
        s = df['Status'].astype(str)
        is_sub = s.str.contains('Submitted|Submit', na=False, case=False) & ~s.str.contains('Not Submitted|NotSubmitted', na=False, case=False)
        submitted = int(is_sub.sum())
    else:
        submitted = 0
    confirmed = _get_confirmed_count(df)
    return total, submitted, confirmed


@st.cache_data(show_spinner=False)
def _get_confirmed_count(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    if '_IsConfirmed' in df.columns:
        return int(df['_IsConfirmed'].sum())
    if 'Confirmed' in df.columns:
        return int(df['Confirmed'].astype(str).str.contains('Yes|True|1', na=False, case=False).sum())
    if 'Confirmation Date' in df.columns:
        return int(df['Confirmation Date'].notna().sum())
    if 'Status' in df.columns:
        return int(df['Status'].str.contains('Confirmed|Confirm|Admitted', na=False, case=False).sum())
    return 0


# ── Cached chart-data helpers (avoid recomputing on every rerun) ──

@st.cache_data(show_spinner=False)
def get_top_programs(df: pd.DataFrame, n: int = 10):
    if df.empty or 'Program1' not in df.columns:
        return pd.Series(dtype='int64')
    return df['Program1'].value_counts().head(n)


@st.cache_data(show_spinner=False)
def get_city_counts(df: pd.DataFrame, n: int = 15):
    if df.empty or 'City' not in df.columns:
        return pd.DataFrame(columns=['City', 'Count']), 0, 0
    city_count = df['City'].value_counts().head(n).reset_index()
    city_count.columns = ['City', 'Count']
    surat = int((df['City'] == 'Surat').sum())
    other = len(df) - surat
    return city_count, surat, other


@st.cache_data(show_spinner=False)
def get_gender_program_data(df: pd.DataFrame, top_n: int = 8):
    if df.empty or 'Gender' not in df.columns or 'Program1' not in df.columns:
        return pd.Series(dtype='int64'), pd.DataFrame(), pd.DataFrame()
    gender_dist = df['Gender'].value_counts()
    top_progs = df['Program1'].value_counts().head(top_n).index
    gp = (df[df['Program1'].isin(top_progs)]
          .groupby(['Gender', 'Program1'], observed=True)
          .size().reset_index(name='Count'))
    gender_stats = (
        df.groupby('Gender', observed=True)
        .agg(
            Total=('Status', 'count'),
            Submitted=('Status', lambda x: x.str.contains('Submitted|Submit', na=False, case=False).sum()),
            Confirmed=('_IsConfirmed', 'sum')
        )
        .reset_index()
    )
    gender_stats['Conversion_%'] = (gender_stats['Confirmed'] / gender_stats['Total'] * 100).round(1).fillna(0)
    return gender_dist, gp, gender_stats


@st.cache_data(show_spinner=False)
def compute_board_counts(df: pd.DataFrame):
    """Robust board detection — checks each column individually, no row-joining."""
    if df.empty:
        return pd.DataFrame(columns=['Board', 'Count'])

    str_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    gseb_mask = pd.Series(False, index=df.index)
    cbse_mask = pd.Series(False, index=df.index)
    icse_mask = pd.Series(False, index=df.index)
    for col in str_cols:
        col_upper = df[col].astype(str).str.upper()
        gseb_mask = gseb_mask | col_upper.str.contains('GSEB', na=False)
        cbse_mask = cbse_mask | col_upper.str.contains('CBSE', na=False)
        icse_mask = icse_mask | col_upper.str.contains('ICSE', na=False)

    gseb = int(gseb_mask.sum())
    cbse = int(cbse_mask.sum())
    icse = int(icse_mask.sum())
    other = max(0, len(df) - gseb - cbse - icse)

    board_df = pd.DataFrame({
        'Board': ['GSEB', 'CBSE', 'ICSE', 'Other'],
        'Count': [gseb, cbse, icse, other],
    })
    return board_df[board_df['Count'] > 0].reset_index(drop=True)


MARKS_COL = '12th/ HSC Overall / Diploma'


def find_column(df: pd.DataFrame, keyword: str):
    """
    Find a column whose name contains `keyword` (case-insensitive).
    Some question headers (e.g. the lead-source column) have slightly
    inconsistent spacing/punctuation across yearly source files, so an
    exact-match lookup is fragile — this matches on substring instead.
    """
    keyword = keyword.lower()
    for c in df.columns:
        if keyword in c.lower():
            return c
    return None


@st.cache_data(show_spinner=False)
def get_program_training_data(df: pd.DataFrame):
    """
    Confirmed admissions with a valid 12th % and a known program, restricted
    to programs with enough historical volume (>=15 confirmed cases) to be a
    meaningful signal rather than a one-off fluke. This is the training set
    for the distance-weighted nearest-neighbour model below.
    """
    if df.empty or MARKS_COL not in df.columns or 'Program1' not in df.columns or '_IsConfirmed' not in df.columns:
        return pd.DataFrame(columns=[MARKS_COL, 'Program1'])
    data = df.loc[df['_IsConfirmed'], [MARKS_COL, 'Program1']].dropna()
    data = data[(data[MARKS_COL] >= 0) & (data[MARKS_COL] <= 100)]
    counts = data['Program1'].value_counts()
    valid_programs = counts[counts >= 15].index
    data = data[data['Program1'].isin(valid_programs)]
    return data.reset_index(drop=True)


def predict_program(train_data: pd.DataFrame, marks: float, k: int = 25, top_n: int = 3):
    """
    Distance-weighted k-nearest-neighbours over a single feature (12th %).
    Finds the k historical confirmed admissions closest to `marks`, weights
    each by inverse distance, and aggregates the weight by program — giving
    a genuine data-driven probability estimate of which program a student
    with this percentage is likely to be confirmed into, learned straight
    from the dataset rather than a fixed percentage-bracket rule.
    """
    if train_data.empty:
        return []
    k = min(k, len(train_data))
    dist = (train_data[MARKS_COL] - marks).abs().to_numpy()
    nearest_idx = np.argsort(dist)[:k]
    nearest = train_data.iloc[nearest_idx].copy()
    nearest['_weight'] = 1.0 / (dist[nearest_idx] + 0.5)
    scores = nearest.groupby('Program1')['_weight'].sum()
    scores = (scores / scores.sum()).sort_values(ascending=False)
    return list(scores.head(top_n).items())


@st.cache_resource(show_spinner=False)
def get_anthropic_client():
    """
    Build the Anthropic client from a Streamlit secret / env var.
    Returns None if no key is configured or the SDK isn't installed —
    callers must handle that gracefully rather than crashing the page.
    """
    if not _ANTHROPIC_AVAILABLE:
        return None
    api_key = None
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        pass
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


@st.cache_data(show_spinner=False)
def llm_recommend_program(marks: float, neighbor_counts: tuple, model_name: str = "claude-haiku-4-5-20251001"):
    """
    Ask Claude to recommend a program, grounded in the SAME nearest-neighbour
    evidence the KNN model uses (not the full dataset, and not general
    knowledge) — so its answer is reasoning over real historical admissions
    at this university, with a short natural-language explanation attached.
    """
    client = get_anthropic_client()
    if client is None:
        return None

    context_lines = "\n".join(f"- {prog}: {cnt} students" for prog, cnt in neighbor_counts)
    prompt = (
        f"You are analyzing Sarvajanik University's historical confirmed-admission data.\n"
        f"A prospective student has a 12th grade percentage of {marks}%.\n\n"
        f"Among the historically confirmed students with the closest 12th percentage to "
        f"this student, here is the breakdown of which programs they were admitted into:\n"
        f"{context_lines}\n\n"
        f"Based only on this data, recommend the single most likely program for this "
        f"student and briefly explain your reasoning in 1-2 sentences. Respond in exactly "
        f"this format:\nProgram: <program name>\nReasoning: <short reasoning>"
    )
    try:
        resp = client.messages.create(
            model=model_name,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        return f"⚠️ LLM call failed: {e}"


@st.cache_data(show_spinner=False)
def get_yearly_conversion(df: pd.DataFrame):
    if df.empty or 'Year' not in df.columns or 'Status' not in df.columns:
        return pd.DataFrame()
    yearly = (
        df.groupby('Year')
        .agg(
            Total=('Status', 'count'),
            Confirmed=('_IsConfirmed', 'sum')
        )
        .reset_index()
    )
    yearly['Conversion_%'] = (yearly['Confirmed'] / yearly['Total'] * 100).round(1)
    return yearly


# ====================== LOAD & CLEAN ======================
raw_df = load_all_data()
df = clean_data(raw_df)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:24px 16px 20px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                        display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">🎓</div>
            <div>
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3b82f6;">Sarvajanik</div>
                <div style="font-size:0.9rem;font-weight:700;color:#e2e8f0;line-height:1.2;">University</div>
            </div>
        </div>
        <div style="padding:12px 14px;background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.18);
                    border-radius:12px;margin-bottom:4px;">
            <div style="font-size:0.65rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px;">Total Records</div>
            <div style="font-size:1.6rem;font-weight:800;color:#60a5fa;letter-spacing:-0.5px;">{len(df):,}</div>
        </div>
    </div>
    <div style="padding:0 16px 8px;">
        <div style="font-size:0.65rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
                    color:#475569;margin-bottom:8px;padding-left:4px;">Navigate</div>
    </div>
    """, unsafe_allow_html=True)

    NAV_ITEMS = [
        "🏠 Home Overview",
        "📈 Inquiry Funnel",
        "🏆 Program Popularity",
        "🗺️ Geographic Analysis",
        "👥 Gender Analysis",
        "📚 Board & Stream",
        "📢 Source & Category",
        "🔮 Advanced Analytics",
        "📅 Year Wise Breakdown",
    ]

    # Handle URL query params for hover links
    q_params = st.query_params
    if q_params.get("page") in ["📅 Year Wise Breakdown", "Year Wise Breakdown"]:
        st.session_state["page"] = "📅 Year Wise Breakdown"
    if "year" in q_params:
        st.session_state["year_selected"] = q_params["year"]
    if "metric" in q_params:
        st.session_state["year_metric_selected"] = q_params["metric"]

    if "page" not in st.session_state:
        st.session_state["page"] = NAV_ITEMS[0]
    if "year_selected" not in st.session_state:
        st.session_state["year_selected"] = "2023-2024"
    if "year_metric_selected" not in st.session_state:
        st.session_state["year_metric_selected"] = "🏆 Program Popularity"

    for item in NAV_ITEMS:
        is_active = st.session_state["page"] == item
        if item == "📅 Year Wise Breakdown":
            if st.button("📅 Year Wise Breakdown", key="nav_year_breakdown_btn", use_container_width=True):
                st.session_state["page"] = item
                st.rerun()

            menu_html = """
            <div class="year-menu-wrapper">
                <div class="year-menu-l1">
                    <div class="year-item-l1">
                        <span>📅 2023-2024</span>
                        <span style="font-size:0.65rem;">▶</span>
                        <div class="year-menu-l2">
                            <a href="?page=📅+Year+Wise+Breakdown&year=2023-2024&metric=🏆+Program+Popularity" target="_self" class="metric-item-l2">🏆 Program Popularity</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2023-2024&metric=🏷️+Admissions+Category" target="_self" class="metric-item-l2">🏷️ Admissions Category</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2023-2024&metric=👥+Gender+Analysis" target="_self" class="metric-item-l2">👥 Gender Analysis</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2023-2024&metric=📚+Board+%26+Stream" target="_self" class="metric-item-l2">📚 Board & Stream</a>
                        </div>
                    </div>
                    <div class="year-item-l1">
                        <span>📅 2024-2025</span>
                        <span style="font-size:0.65rem;">▶</span>
                        <div class="year-menu-l2">
                            <a href="?page=📅+Year+Wise+Breakdown&year=2024-2025&metric=🏆+Program+Popularity" target="_self" class="metric-item-l2">🏆 Program Popularity</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2024-2025&metric=🏷️+Admissions+Category" target="_self" class="metric-item-l2">🏷️ Admissions Category</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2024-2025&metric=👥+Gender+Analysis" target="_self" class="metric-item-l2">👥 Gender Analysis</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2024-2025&metric=📚+Board+%26+Stream" target="_self" class="metric-item-l2">📚 Board & Stream</a>
                        </div>
                    </div>
                    <div class="year-item-l1">
                        <span>📅 2025-2026</span>
                        <span style="font-size:0.65rem;">▶</span>
                        <div class="year-menu-l2">
                            <a href="?page=📅+Year+Wise+Breakdown&year=2025-2026&metric=🏆+Program+Popularity" target="_self" class="metric-item-l2">🏆 Program Popularity</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2025-2026&metric=🏷️+Admissions+Category" target="_self" class="metric-item-l2">🏷️ Admissions Category</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2025-2026&metric=👥+Gender+Analysis" target="_self" class="metric-item-l2">👥 Gender Analysis</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2025-2026&metric=📚+Board+%26+Stream" target="_self" class="metric-item-l2">📚 Board & Stream</a>
                        </div>
                    </div>
                    <div class="year-item-l1">
                        <span>📅 2026-2027</span>
                        <span style="font-size:0.65rem;">▶</span>
                        <div class="year-menu-l2">
                            <a href="?page=📅+Year+Wise+Breakdown&year=2026-2027&metric=🏆+Program+Popularity" target="_self" class="metric-item-l2">🏆 Program Popularity</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2026-2027&metric=🏷️+Admissions+Category" target="_self" class="metric-item-l2">🏷️ Admissions Category</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2026-2027&metric=👥+Gender+Analysis" target="_self" class="metric-item-l2">👥 Gender Analysis</a>
                            <a href="?page=📅+Year+Wise+Breakdown&year=2026-2027&metric=📚+Board+%26+Stream" target="_self" class="metric-item-l2">📚 Board & Stream</a>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(menu_html, unsafe_allow_html=True)
        else:
            if st.button(
                item,
                key=f"nav_{item}",
                use_container_width=True,
                help=item,
            ):
                st.session_state["page"] = item
                st.rerun()

    # Build active-item highlight CSS
    active_idx = NAV_ITEMS.index(st.session_state["page"]) if st.session_state["page"] in NAV_ITEMS else 0
    active_css = f"""
    <style>
        [data-testid="stSidebar"] .stButton > button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 12px !important;
            color: #94a3b8 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 10px 14px !important;
            margin-bottom: 3px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            justify-content: flex-start !important;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(96,165,250,0.10) !important;
            color: #e2e8f0 !important;
            border-color: rgba(96,165,250,0.15) !important;
        }}
        [data-testid="stSidebar"] .stButton > button:focus {{
            box-shadow: none !important;
            outline: none !important;
        }}
        [data-testid="stSidebar"] .stButton:last-of-type > button {{
            background: rgba(148,163,184,0.08) !important;
            border-color: rgba(148,163,184,0.12) !important;
        }}
        [data-testid="stSidebar"] .stButton:nth-of-type({active_idx + 1}) > button {{
            background: rgba(96,165,250,0.15) !important;
            color: #60a5fa !important;
            border-color: rgba(96,165,250,0.3) !important;
            font-weight: 600 !important;
        }}
    </style>
    """
    st.markdown(active_css, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 16px 20px;margin-top:auto;">
        <div style="padding:10px 12px;background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.15);
                    border-radius:10px;font-size:0.72rem;color:#64748b;text-align:center;">
            📊 Analytics Dashboard v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.get("page", NAV_ITEMS[0])

# ====================== PAGES (lazy — only compute what's needed) ======================

if page == "🏠 Home Overview":
    st.markdown('<span class="section-label">Dashboard</span>', unsafe_allow_html=True)
    st.title("Admission Analytics")
    st.markdown('<h2>2023 – 2027 · Sarvajanik University</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    total, submitted, confirmed = compute_kpis(df)
    conv = round(confirmed / total * 100, 1) if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, cls, label, value, sub in [
        (c1, "card-blue",   "Total Inquiries",       f"{total:,}",     "All-time records"),
        (c2, "card-green",  "Submitted",             f"{submitted:,}", "Applications filed"),
        (c3, "card-amber",  "Confirmed Admissions",  f"{confirmed:,}", "Seat confirmed"),
        (c4, "card-violet", "Conversion Rate",       f"{conv}%",       "Inquiry → Admit"),
    ]:
        with col:
            st.markdown(f"""
            <div class="glass-card {cls}">
                <div class="card-label">{label}</div>
                <div class="card-value">{value}</div>
                <div class="card-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    top10 = get_top_programs(df, 10)
    if not top10.empty:
        fig = px.bar(top10, text_auto=True, title="Top 10 Most Applied Programs",
                     color_discrete_sequence=COLORS)
        fig.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
        wrap_chart(fig)

elif page == "📈 Inquiry Funnel":
    st.markdown('<span class="section-label">Conversion</span>', unsafe_allow_html=True)
    st.title("Inquiry Funnel")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty:
        total, submitted, confirmed = compute_kpis(df)
        fig = go.Figure(go.Funnel(
            y=['Total Inquiries', 'Submitted', 'Confirmed'],
            x=[total, submitted, confirmed],
            textinfo="value+percent initial",
            marker=dict(color=['#60a5fa', '#34d399', '#fbbf24'],
                        line=dict(color='rgba(0,0,0,0.2)', width=1)),
            connector=dict(line=dict(color='rgba(255,255,255,0.06)', width=2))
        ))
        fig.update_layout(title="Admission Conversion Funnel")
        wrap_chart(fig, height=550)

        rate_sub = round(submitted / total * 100, 1) if total else 0
        rate_con = round(confirmed / total * 100, 1) if total else 0
        c1, c2, c3 = st.columns(3)
        for col, label, val, cls in [
            (c1, "Inquiry → Submit", f"{rate_sub}%", "card-green"),
            (c2, "Inquiry → Confirm", f"{rate_con}%", "card-amber"),
            (c3, "Drop-off Rate", f"{round(100-rate_sub,1)}%", "card-violet"),
        ]:
            with col:
                st.markdown(f'<div class="glass-card {cls}"><div class="card-label">{label}</div><div class="card-value">{val}</div></div>', unsafe_allow_html=True)

elif page == "🏆 Program Popularity":
    st.markdown('<span class="section-label">Programs</span>', unsafe_allow_html=True)
    st.title("Program Popularity")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    top15 = get_top_programs(df, 15)
    if not top15.empty:
        top15_df = top15.reset_index()
        top15_df.columns = ['Program', 'Count']
        fig = px.bar(top15_df, x='Count', y='Program', orientation='h',
                     text_auto=True, title="Top 15 Programs by Demand",
                     color='Count', color_continuous_scale='Blues')
        fig.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
        wrap_chart(fig, height=560, yaxis_extra={'categoryorder': 'total ascending'})

elif page == "🗺️ Geographic Analysis":
    st.markdown('<span class="section-label">Geography</span>', unsafe_allow_html=True)
    st.title("Geographic Analysis")
    st.markdown('<h2>Surat & South Gujarat focus</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    city_count, surat_count, other_count = get_city_counts(df, 15)
    if not city_count.empty:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig1 = px.bar(city_count, x='Count', y='City', orientation='h',
                          text_auto=True, title="Top 15 Cities by Inquiries",
                          color='Count', color_continuous_scale='Blues')
            wrap_chart(fig1, height=480, yaxis_extra={'categoryorder': 'total ascending'})
        with c2:
            fig2 = px.pie(
                values=[surat_count, other_count],
                names=['Surat', 'Other Regions'],
                title="Surat vs Rest", hole=0.55,
                color_discrete_sequence=['#60a5fa', '#1e3a5f']
            )
            fig2.update_traces(textfont_color='#e2e8f0', marker_line_color='rgba(0,0,0,0.2)')
            wrap_chart(fig2, height=480)

elif page == "👥 Gender Analysis":
    st.markdown('<span class="section-label">Demographics</span>', unsafe_allow_html=True)
    st.title("Gender Analysis")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    gender_dist, gp, gender_stats = get_gender_program_data(df)
    if not gender_dist.empty:
        c1, c2 = st.columns([2, 3])
        with c1:
            fig1 = px.pie(names=gender_dist.index, values=gender_dist.values,
                          title="Gender Distribution", hole=0.5,
                          color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
            fig1.update_traces(textfont_color='#e2e8f0', marker_line_color='rgba(0,0,0,0)')
            wrap_chart(fig1, height=380)
        with c2:
            if not gp.empty:
                fig2 = px.bar(gp, x='Program1', y='Count', color='Gender',
                              title="Program Preference by Gender", barmode='group',
                              color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
                wrap_chart(fig2, height=380, xaxis_extra={'tickangle': -30})

        st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
        if not gender_stats.empty:
            fig3 = px.bar(gender_stats, x='Gender', y='Conversion_%', text_auto=True,
                          title="Conversion Rate by Gender (%)",
                          color_discrete_sequence=['#a78bfa'])
            fig3.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            wrap_chart(fig3)

elif page == "📚 Board & Stream":
    st.markdown('<span class="section-label">Academic Background</span>', unsafe_allow_html=True)
    st.title("Board & Stream Analysis")
    st.markdown('<h2>GSEB · CBSE · ICSE &nbsp;·&nbsp; Science · Commerce · Arts</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    board_df = compute_board_counts(df)
    if not board_df.empty:
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(
                board_df, x='Board', y='Count', text_auto=True,
                title="Students by Board",
                color='Board',
                color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
            )
            fig1.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            wrap_chart(fig1, height=420)

        with c2:
            fig2 = px.pie(
                board_df, names='Board', values='Count',
                title="Board Distribution", hole=0.48,
                color='Board',
                color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
            )
            fig2.update_traces(
                textfont_color='#e2e8f0',
                textinfo='label+percent',
                marker_line_color='rgba(0,0,0,0.15)',
                marker_line_width=2,
                pull=[0.04, 0.04, 0.04, 0],
            )
            wrap_chart(fig2, height=420)

elif page == "📢 Source & Category":
    st.markdown('<span class="section-label">Acquisition & Reservation</span>', unsafe_allow_html=True)
    st.title("Lead Source & Category")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    source_col = find_column(df, 'from where you get the detail')

    if not df.empty and source_col:
        st.markdown("#### 📢 Lead Source")
        src_df = df[df[source_col].notna()].copy()
        src_df[source_col] = src_df[source_col].astype(str).str.strip()

        c1, c2 = st.columns(2)
        with c1:
            top_src = src_df[source_col].value_counts().head(10).reset_index()
            top_src.columns = ['Source', 'Count']
            fig1 = px.bar(
                top_src, x='Count', y='Source', orientation='h', text_auto=True,
                title="Inquiries by Lead Source",
                color_discrete_sequence=['#60a5fa'],
            )
            fig1.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, yaxis_title="")
            wrap_chart(fig1, height=420)

        with c2:
            src_stats = (
                src_df.groupby(source_col, observed=True)
                .agg(Total=('Status', 'count'), Confirmed=('_IsConfirmed', 'sum'))
                .reset_index()
            )
            src_stats = src_stats[src_stats['Total'] >= 10]  # drop tiny/noisy sources
            src_stats['Conversion_%'] = (src_stats['Confirmed'] / src_stats['Total'] * 100).round(1)
            src_stats = src_stats.sort_values('Conversion_%', ascending=True)
            fig2 = px.bar(
                src_stats, x='Conversion_%', y=source_col, orientation='h', text_auto=True,
                title="Conversion Rate by Source (%)",
                color_discrete_sequence=['#34d399'],
            )
            fig2.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            fig2.update_layout(yaxis_title="")
            wrap_chart(fig2, height=420)

        missing = int(df[source_col].isna().sum())
        st.caption(f"{missing:,} of {len(df):,} records don't have a lead source on file (sources with under 10 records are excluded from the conversion chart).")
    else:
        st.info("No lead-source column found in the current dataset.")

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty and 'Category' in df.columns:
        st.markdown("#### 🏷️ Category-wise Breakdown")
        cat_df = df[df['Category'].notna()].copy()

        c3, c4 = st.columns([2, 3])
        with c3:
            cat_dist = cat_df['Category'].value_counts()
            fig3 = px.pie(
                names=cat_dist.index, values=cat_dist.values,
                title="Category Distribution", hole=0.48,
                color_discrete_sequence=['#60a5fa', '#a78bfa', '#fbbf24', '#f472b6', '#34d399'],
            )
            fig3.update_traces(
                textfont_color='#e2e8f0', textinfo='label+percent',
                marker_line_color='rgba(0,0,0,0.15)', marker_line_width=2,
            )
            wrap_chart(fig3, height=400)

        with c4:
            cat_stats = (
                cat_df.groupby('Category', observed=True)
                .agg(Total=('Status', 'count'), Confirmed=('_IsConfirmed', 'sum'))
                .reset_index()
            )
            cat_stats['Conversion_%'] = (cat_stats['Confirmed'] / cat_stats['Total'] * 100).round(1)
            cat_stats = cat_stats.sort_values('Conversion_%', ascending=False)
            fig4 = px.bar(
                cat_stats, x='Category', y='Conversion_%', text_auto=True,
                title="Conversion Rate by Category (%)",
                color_discrete_sequence=['#a78bfa'],
            )
            fig4.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            wrap_chart(fig4, height=400)

        missing_cat = int(df['Category'].isna().sum())
        st.caption(f"{missing_cat:,} of {len(df):,} records don't have a category on file.")
    else:
        st.info("No category column found in the current dataset.")

elif page == "🔮 Advanced Analytics":
    st.markdown('<span class="section-label">Intelligence</span>', unsafe_allow_html=True)
    st.title("Advanced Analytics")
    st.markdown('<h2>Trends, Forecasts & Recommendations</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            yearly = get_yearly_conversion(df)
            if not yearly.empty:
                fig1 = px.line(yearly, x='Year', y='Conversion_%', markers=True,
                               title="Year-wise Conversion Rate Trend",
                               color_discrete_sequence=['#60a5fa'])
                fig1.update_traces(line_width=3, marker_size=8, marker_color='#a78bfa')
                wrap_chart(fig1)


        total, _, confirmed = compute_kpis(df)
        occ_rate = round(confirmed / max(total, 1) * 100, 1)
        c3, c4, c5 = st.columns(3)
        with c3: st.metric("Seat Occupancy Rate", f"{occ_rate}%")
        with c4: st.metric("Total Records", f"{total:,}")
        with c5: st.metric("Confirmed Admissions", f"{confirmed:,}")


elif page == "📅 Year Wise Breakdown":
    st.markdown('<span class="section-label">Yearly Deep Dive</span>', unsafe_allow_html=True)
    st.title("Year Wise Breakdown")
    st.markdown('<h2>Select Academic Year & Metric for granular analysis</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    YEAR_MAP = {
        "2023-2024": "2023",
        "2024-2025": "2024",
        "2025-2026": "2025",
        "2026-2027": "2026",
    }
    years_list = list(YEAR_MAP.keys())
    metrics_list = ["🏆 Program Popularity", "🏷️ Admissions Category", "👥 Gender Analysis", "📚 Board & Stream"]

    c_yr, c_met = st.columns([1, 1])
    with c_yr:
        st.markdown("<div style='font-size:0.75rem;font-weight:700;letter-spacing:0.08em;color:#60a5fa;text-transform:uppercase;margin-bottom:6px;'>📅 Academic Year</div>", unsafe_allow_html=True)
        selected_year = st.radio(
            "Select Year",
            years_list,
            index=years_list.index(st.session_state.get("year_selected", "2023-2024")) if st.session_state.get("year_selected") in years_list else 0,
            key="yr_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state["year_selected"] = selected_year

    with c_met:
        st.markdown("<div style='font-size:0.75rem;font-weight:700;letter-spacing:0.08em;color:#a78bfa;text-transform:uppercase;margin-bottom:6px;'>📊 Sub-Analysis Metric</div>", unsafe_allow_html=True)
        selected_metric = st.radio(
            "Select Metric",
            metrics_list,
            index=metrics_list.index(st.session_state.get("year_metric_selected", "🏆 Program Popularity")) if st.session_state.get("year_metric_selected") in metrics_list else 0,
            key="met_radio",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state["year_metric_selected"] = selected_metric

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    # Filter data for selected year
    year_code = YEAR_MAP[selected_year]
    year_df = df[df['Year'] == year_code].copy() if not df.empty and 'Year' in df.columns else pd.DataFrame()

    if year_df.empty:
        st.warning(f"No records available for Academic Year {selected_year}.")
    else:
        # Display KPIs for selected year
        total_yr, sub_yr, conf_yr = compute_kpis(year_df)
        conv_yr = round(conf_yr / total_yr * 100, 1) if total_yr > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        for col, cls, label, val, sub_t in [
            (k1, "card-blue",   f"AY {selected_year} Records", f"{total_yr:,}", "Total inquiries"),
            (k2, "card-green",  "Submitted Applications",      f"{sub_yr:,}",  "Filed forms"),
            (k3, "card-amber",  "Confirmed Admissions",       f"{conf_yr:,}", "Admitted seats"),
            (k4, "card-violet", "Year Conversion Rate",        f"{conv_yr}%",  "Inquiry → Admit"),
        ]:
            with col:
                st.markdown(f"""
                <div class="glass-card {cls}">
                    <div class="card-label">{label}</div>
                    <div class="card-value">{val}</div>
                    <div class="card-sub">{sub_t}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

        # Render chosen metric view for this year
        if selected_metric == "🏆 Program Popularity":
            st.markdown(f"### 🏆 Program Popularity — AY {selected_year}")
            if 'Program1' in year_df.columns:
                top15_yr = year_df['Program1'].value_counts().head(15).reset_index()
                top15_yr.columns = ['Program', 'Count']
                fig_p = px.bar(top15_yr, x='Count', y='Program', orientation='h',
                               text_auto=True, title=f"Top Programs by Demand ({selected_year})",
                               color='Count', color_continuous_scale='Blues')
                fig_p.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
                wrap_chart(fig_p, height=560, yaxis_extra={'categoryorder': 'total ascending'})
            else:
                st.info("Program data not available for this year.")

        elif selected_metric == "🏷️ Admissions Category":
            st.markdown(f"### 🏷️ Admissions Category — AY {selected_year}")
            if 'Category' in year_df.columns:
                cat_yr = year_df[year_df['Category'].notna()].copy()
                c1_cat, c2_cat = st.columns([2, 3])
                with c1_cat:
                    cat_dist = cat_yr['Category'].value_counts()
                    fig_c1 = px.pie(names=cat_dist.index, values=cat_dist.values,
                                    title=f"Category Distribution ({selected_year})", hole=0.48,
                                    color_discrete_sequence=['#60a5fa', '#a78bfa', '#fbbf24', '#f472b6', '#34d399'])
                    fig_c1.update_traces(textfont_color='#e2e8f0', textinfo='label+percent',
                                         marker_line_color='rgba(0,0,0,0.15)', marker_line_width=2)
                    wrap_chart(fig_c1, height=420)

                with c2_cat:
                    cat_stats = (
                        cat_yr.groupby('Category', observed=True)
                        .agg(Total=('Status', 'count'), Confirmed=('_IsConfirmed', 'sum'))
                        .reset_index()
                    )
                    cat_stats['Conversion_%'] = (cat_stats['Confirmed'] / cat_stats['Total'] * 100).round(1).fillna(0)
                    cat_stats = cat_stats.sort_values('Conversion_%', ascending=False)
                    fig_c2 = px.bar(cat_stats, x='Category', y='Conversion_%', text_auto=True,
                                    title=f"Conversion Rate by Category (%) ({selected_year})",
                                    color_discrete_sequence=['#a78bfa'])
                    fig_c2.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
                    wrap_chart(fig_c2, height=420)
            else:
                st.info("Category data not available for this year.")

        elif selected_metric == "👥 Gender Analysis":
            st.markdown(f"### 👥 Gender Analysis — AY {selected_year}")
            if 'Gender' in year_df.columns and 'Program1' in year_df.columns:
                c1_g, c2_g = st.columns([2, 3])
                with c1_g:
                    g_dist = year_df['Gender'].value_counts()
                    fig_g1 = px.pie(names=g_dist.index, values=g_dist.values,
                                    title=f"Gender Distribution ({selected_year})", hole=0.5,
                                    color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
                    fig_g1.update_traces(textfont_color='#e2e8f0', marker_line_color='rgba(0,0,0,0)')
                    wrap_chart(fig_g1, height=380)

                with c2_g:
                    top_p = year_df['Program1'].value_counts().head(8).index
                    gp = (year_df[year_df['Program1'].isin(top_p)]
                          .groupby(['Gender', 'Program1'], observed=True)
                          .size().reset_index(name='Count'))
                    fig_g2 = px.bar(gp, x='Program1', y='Count', color='Gender',
                                    title=f"Program Preference by Gender ({selected_year})", barmode='group',
                                    color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
                    wrap_chart(fig_g2, height=380, xaxis_extra={'tickangle': -30})

                st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
                g_stats = (
                    year_df.groupby('Gender', observed=True)
                    .agg(
                        Total=('Status', 'count'),
                        Submitted=('Status', lambda x: x.str.contains('Submitted|Submit', na=False, case=False).sum()),
                        Confirmed=('_IsConfirmed', 'sum')
                    )
                    .reset_index()
                )
                g_stats['Conversion_%'] = (g_stats['Confirmed'] / g_stats['Total'] * 100).round(1).fillna(0)
                fig_g3 = px.bar(g_stats, x='Gender', y='Conversion_%', text_auto=True,
                                title=f"Conversion Rate by Gender (%) ({selected_year})",
                                color_discrete_sequence=['#a78bfa'])
                fig_g3.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
                wrap_chart(fig_g3, height=400)
            else:
                st.info("Gender data not available for this year.")

        elif selected_metric == "📚 Board & Stream":
            st.markdown(f"### 📚 Board & Stream Analysis — AY {selected_year}")
            str_cols = year_df.select_dtypes(include=['object', 'category']).columns.tolist()
            gseb_mask = pd.Series(False, index=year_df.index)
            cbse_mask = pd.Series(False, index=year_df.index)
            icse_mask = pd.Series(False, index=year_df.index)
            for col in str_cols:
                col_upper = year_df[col].astype(str).str.upper()
                gseb_mask = gseb_mask | col_upper.str.contains('GSEB', na=False)
                cbse_mask = cbse_mask | col_upper.str.contains('CBSE', na=False)
                icse_mask = icse_mask | col_upper.str.contains('ICSE', na=False)
            g_cnt = int(gseb_mask.sum())
            c_cnt = int(cbse_mask.sum())
            i_cnt = int(icse_mask.sum())
            o_cnt = max(0, len(year_df) - g_cnt - c_cnt - i_cnt)

            board_yr = pd.DataFrame({
                'Board': ['GSEB', 'CBSE', 'ICSE', 'Other'],
                'Count': [g_cnt, c_cnt, i_cnt, o_cnt],
            })
            board_yr = board_yr[board_yr['Count'] > 0].reset_index(drop=True)

            c1_b, c2_b = st.columns(2)
            with c1_b:
                fig_b1 = px.bar(
                    board_yr, x='Board', y='Count', text_auto=True,
                    title=f"Students by Board ({selected_year})",
                    color='Board',
                    color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
                )
                fig_b1.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
                wrap_chart(fig_b1, height=420)

            with c2_b:
                fig_b2 = px.pie(
                    board_yr, names='Board', values='Count',
                    title=f"Board Distribution ({selected_year})", hole=0.48,
                    color='Board',
                    color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
                )
                fig_b2.update_traces(
                    textfont_color='#e2e8f0',
                    textinfo='label+percent',
                    marker_line_color='rgba(0,0,0,0.15)',
                    marker_line_width=2,
                )
                wrap_chart(fig_b2, height=420)

# ====================== FOOTER ======================
st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
st.success("✅ Dashboard loaded successfully")
