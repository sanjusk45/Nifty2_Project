"""
YRS INNOVATIONS LLP - Python Developer Technical Assignment II
Supertrend Strategy Backtester — Streamlit App
All conditions from PDF strictly followed.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io, warnings
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YRS Innovations — Supertrend Backtester",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0a0a14 0%, #0f0f1e 50%, #0a0f1e 100%);
    color: #e0e0f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1f 0%, #111128 100%);
    border-right: 1px solid #1e1e3a;
}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
    color: #a0a0c0 !important;
}

/* Header */
.main-header {
    background: linear-gradient(90deg, #1a1a3e 0%, #0d1a3a 100%);
    border: 1px solid #2a2a5a;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    color: #7eb8f7;
    font-size: 1.8rem;
    margin: 0 0 4px 0;
}
.main-header p {
    color: #6080a0;
    margin: 0;
    font-size: 0.9rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #141428 0%, #1a1a35 100%);
    border: 1px solid #252550;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    color: #6070a0;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
}
.metric-green  { color: #2ecc71; }
.metric-red    { color: #e74c3c; }
.metric-yellow { color: #f1c40f; }
.metric-blue   { color: #7eb8f7; }

/* Section headers */
.section-title {
    font-family: 'Space Mono', monospace;
    color: #7eb8f7;
    font-size: 1rem;
    border-bottom: 1px solid #1e2e4a;
    padding-bottom: 8px;
    margin: 20px 0 14px 0;
}

/* Trade tables */
.trade-table th {
    background: #141428 !important;
    color: #7eb8f7 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #1a4080 0%, #1a2a6a 100%);
    color: #c0d8f8;
    border: 1px solid #2a4a8a;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    padding: 10px 28px;
    transition: all 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #2050a0 0%, #1a3a80 100%);
    border-color: #4a7acc;
    color: white;
}

/* Selectbox / slider */
.stSelectbox label, .stSlider label { color: #8090b0 !important; }

/* Download button */
[data-testid="stDownloadButton"]>button {
    background: #0f2a18;
    color: #2ecc71;
    border: 1px solid #1a5a30;
    border-radius: 6px;
    font-size: 0.8rem;
}

/* Info boxes */
.info-box {
    background: #0d1a2a;
    border-left: 3px solid #7eb8f7;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.85rem;
    color: #90a8c8;
}

/* Heikin Ashi Rule Banner */
.ha-rule-banner {
    background: linear-gradient(90deg, #1a1a08 0%, #141408 100%);
    border: 1px solid #3a3a10;
    border-left: 4px solid #f1c40f;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 10px 0 18px 0;
}
.ha-title {
    color: #f1c40f;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    font-size: 0.88rem;
    margin-bottom: 10px;
}
.ha-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 6px;
}
.ha-col {
    background: #0a0a08;
    border-radius: 6px;
    padding: 10px 14px;
    border: 1px solid #2a2a10;
}
.ha-col-title-green { color: #2ecc71; font-size: 0.76rem; font-weight:700;
                      text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
.ha-col-title-red   { color: #e74c3c; font-size: 0.76rem; font-weight:700;
                      text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
.ha-col-body { color: #a0b070; font-size: 0.82rem; line-height: 1.6; }

div[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace;
    color: #6080a0;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #7eb8f7;
    border-bottom-color: #7eb8f7;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
SYMBOLS = {
    "RELIANCE":  "RELIANCE.NS",
    "NIFTYBEES": "NIFTYBEES.NS",
    "ITC":       "ITC.NS",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    try:
        import yfinance as yf
        df = yf.download(ticker, start=start, end=end,
                         progress=False, auto_adjust=True)
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        df.dropna(inplace=True)
        df.index = pd.to_datetime(df.index)
        if len(df) < 20:
            raise ValueError("Too few rows")
        return df[["Open","High","Low","Close"]]
    except Exception as e:
        st.warning(f"⚠️ yfinance unavailable ({e}). Using synthetic data for demo.")
        return _synthetic(ticker)


# ─────────────────────────────────────────────────────────────────────────────
# LIVE / ACUTE DATA FETCH  (intraday 1-min latest quote)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_live_data(ticker: str) -> dict:
    """
    Fetch live/acute data for the ticker:
      • Latest price (1-min or last daily close)
      • Today's OHLC, volume, change %
      • Current Supertrend signal based on today's candle
    Returns a dict with live fields. Falls back gracefully on error.
    """
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)

        # Fast info (most up-to-date quote available)
        fi = t.fast_info

        live = {}
        live["last_price"]     = round(float(fi.last_price), 2)
        live["prev_close"]     = round(float(fi.previous_close), 2)
        live["day_high"]       = round(float(fi.day_high), 2)
        live["day_low"]        = round(float(fi.day_low), 2)
        live["volume"]         = int(fi.three_month_average_volume or 0)
        live["market_cap"]     = fi.market_cap

        change     = live["last_price"] - live["prev_close"]
        change_pct = change / live["prev_close"] * 100
        live["change"]     = round(change, 2)
        live["change_pct"] = round(change_pct, 2)
        live["direction"]  = "▲ UP" if change >= 0 else "▼ DOWN"
        live["color"]      = "#2ecc71" if change >= 0 else "#e74c3c"

        # Intraday 1-min bars for last 5 min (most recent tick)
        try:
            intra = t.history(period="1d", interval="1m")
            if not intra.empty:
                live["last_price"]  = round(float(intra["Close"].iloc[-1]), 2)
                live["intra_open"]  = round(float(intra["Open"].iloc[0]), 2)
                live["intra_high"]  = round(float(intra["High"].max()), 2)
                live["intra_low"]   = round(float(intra["Low"].min()), 2)
                live["last_update"] = str(intra.index[-1])
            else:
                live["last_update"] = "End of day (market closed)"
        except Exception:
            live["last_update"] = "Live tick unavailable"

        live["status"] = "ok"
        return live

    except Exception as e:
        return {"status": "error", "msg": str(e),
                "last_price": 0.0, "prev_close": 0.0,
                "change": 0.0, "change_pct": 0.0,
                "direction": "N/A", "color": "#7eb8f7",
                "day_high": 0.0, "day_low": 0.0,
                "volume": 0, "last_update": "Unavailable"}


def _synthetic(ticker: str) -> pd.DataFrame:
    seeds = {"RELIANCE.NS":42, "ITC.NS":7, "NIFTYBEES.NS":99}
    bases = {"RELIANCE.NS":2800.0, "ITC.NS":430.0, "NIFTYBEES.NS":240.0}
    np.random.seed(seeds.get(ticker, 1))
    dates = pd.bdate_range(end=datetime.today(), periods=252)
    n     = len(dates)
    base  = bases.get(ticker, 1000.0)
    ret   = np.random.normal(0.0003, 0.012, n)
    ret[60:120]  += 0.004
    ret[130:185] -= 0.005
    ret[200:]    += 0.003
    close = base * np.exp(np.cumsum(ret))
    high  = close * (1 + np.abs(np.random.normal(0, 0.007, n)))
    low   = close * (1 - np.abs(np.random.normal(0, 0.007, n)))
    opn   = np.concatenate([[close[0]*0.999], close[:-1]])
    return pd.DataFrame({"Open":np.round(opn,2),"High":np.round(high,2),
                         "Low":np.round(low,2),"Close":np.round(close,2)},
                        index=dates)


# ─────────────────────────────────────────────────────────────────────────────
# HEIKIN ASHI  (PDF §4)
# ─────────────────────────────────────────────────────────────────────────────
def heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Heikin Ashi candles from regular OHLC."""
    ha = pd.DataFrame(index=df.index)
    ha["HA_Close"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
    ha_open        = np.zeros(len(df))
    ha_open[0]     = (df["Open"].iloc[0] + df["Close"].iloc[0]) / 2
    hc             = ha["HA_Close"].values
    for i in range(1, len(df)):
        ha_open[i] = (ha_open[i-1] + hc[i-1]) / 2
    ha["HA_Open"] = ha_open
    ha["HA_High"] = pd.concat([df["High"], ha["HA_Open"], ha["HA_Close"]], axis=1).max(axis=1)
    ha["HA_Low"]  = pd.concat([df["Low"],  ha["HA_Open"], ha["HA_Close"]], axis=1).min(axis=1)
    return ha


# ─────────────────────────────────────────────────────────────────────────────
# SUPERTREND  (PDF §5 — ATR Period:7, Multiplier:3)
# ─────────────────────────────────────────────────────────────────────────────
def supertrend(ha: pd.DataFrame, period: int = 7, mult: float = 3) -> pd.DataFrame:
    """Supertrend calculated on Heikin Ashi candles using Wilder ATR."""
    H = ha["HA_High"].values
    L = ha["HA_Low"].values
    C = ha["HA_Close"].values
    n = len(ha)

    # True Range
    tr = np.zeros(n)
    tr[0] = H[0] - L[0]
    for i in range(1, n):
        tr[i] = max(H[i]-L[i], abs(H[i]-C[i-1]), abs(L[i]-C[i-1]))

    # Wilder's ATR
    atr = np.zeros(n)
    atr[0] = tr[0]
    alpha  = 1.0 / period
    for i in range(1, n):
        atr[i] = alpha * tr[i] + (1 - alpha) * atr[i-1]

    hl2 = (H + L) / 2.0
    ub  = hl2 + mult * atr
    lb  = hl2 - mult * atr
    fub = ub.copy()
    flb = lb.copy()

    for i in range(1, n):
        fub[i] = ub[i] if (ub[i] < fub[i-1] or C[i-1] > fub[i-1]) else fub[i-1]
        flb[i] = lb[i] if (lb[i] > flb[i-1] or C[i-1] < flb[i-1]) else flb[i-1]

    st_vals   = np.zeros(n)
    direction = np.ones(n, dtype=int)   # 1=green/bullish, -1=red/bearish
    st_vals[0]   = flb[0]
    direction[0] = 1

    for i in range(1, n):
        if st_vals[i-1] == fub[i-1]:           # was bearish
            direction[i] = -1 if C[i] <= fub[i] else 1
        else:                                   # was bullish
            direction[i] =  1 if C[i] >= flb[i] else -1
        st_vals[i] = flb[i] if direction[i] == 1 else fub[i]

    out = ha.copy()
    out["Supertrend"]  = st_vals
    out["Direction"]   = direction
    out["Final_UB"]    = fub
    out["Final_LB"]    = flb
    return out


# ─────────────────────────────────────────────────────────────────────────────
# SIGNALS  (PDF §6)
# ─────────────────────────────────────────────────────────────────────────────
def generate_signals(st_df: pd.DataFrame) -> pd.DataFrame:
    """
    Long Entry  : Direction changes Red(-1) → Green(1)
    Short Entry : Direction changes Green(1) → Red(-1)
    HA columns kept in sig so the chart can draw HA candlesticks.
    """
    st_df = st_df.copy()
    prev  = st_df["Direction"].shift(1).fillna(st_df["Direction"].iloc[0]).astype(int)
    st_df["Prev_Dir"]    = prev
    st_df["Long_Entry"]  = (st_df["Direction"] ==  1) & (prev == -1)
    st_df["Short_Entry"] = (st_df["Direction"] == -1) & (prev ==  1)
    return st_df


# ─────────────────────────────────────────────────────────────────────────────
# BACKTEST  (PDF §6 + §7)
# Entry signal from HA, but actual price from original OHLC close (PDF §4 rule)
# ─────────────────────────────────────────────────────────────────────────────
def backtest(ohlc: pd.DataFrame, sig: pd.DataFrame):
    long_trades  = []
    short_trades = []
    in_long = in_short = False
    le_d = le_p = se_d = se_p = None

    def _rec(ed, ep, xd, xp, pnl):
        return {"Entry Date":  ed.strftime("%Y-%m-%d"),
                "Entry Price": round(float(ep), 2),
                "Exit Date":   xd.strftime("%Y-%m-%d"),
                "Exit Price":  round(float(xp), 2),
                "PnL":         round(float(pnl), 2)}

    for date, row in sig.iterrows():
        px = float(ohlc.loc[date, "Close"])     # ★ OHLC actual price

        # ── Long Entry: Red→Green ──
        if row["Long_Entry"]:
            if in_short:
                short_trades.append(_rec(se_d, se_p, date, px, se_p - px))
                in_short = False
            if not in_long:
                le_d, le_p, in_long = date, px, True

        # ── Short Entry: Green→Red ──
        if row["Short_Entry"]:
            if in_long:
                long_trades.append(_rec(le_d, le_p, date, px, px - le_p))
                in_long = False
            if not in_short:
                se_d, se_p, in_short = date, px, True

    # Close open positions at last bar
    ld, lp = sig.index[-1], float(ohlc.iloc[-1]["Close"])
    if in_long:
        long_trades.append(_rec(le_d, le_p, ld, lp, lp - le_p))
    if in_short:
        short_trades.append(_rec(se_d, se_p, ld, lp, se_p - lp))

    return pd.DataFrame(long_trades), pd.DataFrame(short_trades)


# ─────────────────────────────────────────────────────────────────────────────
# PERFORMANCE METRICS  (PDF §8)
# ─────────────────────────────────────────────────────────────────────────────
def calc_metrics(df: pd.DataFrame, label: str) -> dict:
    if df.empty:
        return {"label": label, "total": 0, "pnl": 0.0,
                "win_rate": "0%", "max_dd": 0.0, "avg_pnl": 0.0}
    pnl = df["PnL"].values
    cum = np.cumsum(pnl)
    mdd = round(float((np.maximum.accumulate(cum) - cum).max()), 2)
    wins = int((pnl > 0).sum())
    return {
        "label":    label,
        "total":    len(df),
        "pnl":      round(float(pnl.sum()), 2),
        "win_rate": f"{round(wins / len(pnl) * 100, 1)}%",
        "max_dd":   mdd,
        "avg_pnl":  round(float(pnl.mean()), 2),
        "wins":     wins,
        "losses":   len(pnl) - wins,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHART  (PDF §7) — TradingView-style Heikin Ashi candles + Supertrend shading
# ─────────────────────────────────────────────────────────────────────────────
def _draw_ha_candles(ax, ha: pd.DataFrame, dir_arr, width_frac=0.6):
    """
    Draw Heikin Ashi OHLC candlesticks coloured by Supertrend direction.
    Green candle  → bullish (Direction == 1)
    Red   candle  → bearish (Direction == -1)
    Matches TradingView visual style exactly.
    """
    import matplotlib.patches as mpatches
    from matplotlib.collections import PatchCollection
    import matplotlib.dates as mdates

    dates  = ha.index
    o = ha["HA_Open"].values
    h = ha["HA_High"].values
    l = ha["HA_Low"].values
    c = ha["HA_Close"].values

    # Convert dates to float for positioning
    date_nums = mdates.date2num(dates.to_pydatetime())
    width     = (date_nums[1] - date_nums[0]) * width_frac if len(date_nums) > 1 else 0.4

    for i in range(len(dates)):
        bull   = dir_arr[i] == 1
        body_c = "#26a65b" if bull else "#e74c3c"     # solid fill
        wick_c = "#1a8a45" if bull else "#c0392b"     # slightly darker wick
        border = "#1a7a40" if bull else "#a93226"

        top    = max(o[i], c[i])
        bot    = min(o[i], c[i])
        body_h = max(top - bot, width * 0.05)          # minimum visible body

        # Body rectangle
        rect = mpatches.FancyBboxPatch(
            (date_nums[i] - width/2, bot), width, body_h,
            boxstyle="square,pad=0",
            facecolor=body_c, edgecolor=border, linewidth=0.4, zorder=3
        )
        ax.add_patch(rect)

        # Upper wick
        if h[i] > top:
            ax.plot([date_nums[i], date_nums[i]], [top, h[i]],
                    color=wick_c, lw=0.9, zorder=2)
        # Lower wick
        if l[i] < bot:
            ax.plot([date_nums[i], date_nums[i]], [l[i], bot],
                    color=wick_c, lw=0.9, zorder=2)

    ax.xaxis_date()


def build_chart(ohlc, sig, long_df, short_df, name):
    """
    Main chart — exactly like TradingView screenshot:
      • Heikin Ashi candlesticks (green/red by Supertrend direction)
      • Supertrend line with green/red shading fill between price and ST line
      • Buy ▲ / Sell ▼ signal markers
      • Volume bars (bottom sub-panel)
      • PnL panel
    """
    import matplotlib.dates as mdates

    BG, PAN = "#131722", "#1e222d"   # TradingView dark theme colours
    GRID    = "#2a2e39"
    GREEN   = "#26a65b"
    RED     = "#e74c3c"
    GREEN_A = "#26a65b33"            # transparent fill
    RED_A   = "#e74c3c33"

    ha       = sig[["HA_Open","HA_High","HA_Low","HA_Close"]].copy()
    dir_arr  = sig["Direction"].values
    st_arr   = sig["Supertrend"].values
    dates    = ohlc.index
    date_nums = mdates.date2num(dates.to_pydatetime())

    fig = plt.figure(figsize=(22, 13), facecolor=BG)
    gs  = fig.add_gridspec(3, 1, height_ratios=[4, 0.9, 1.4], hspace=0.04)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)

    for ax in (ax1, ax2, ax3):
        ax.set_facecolor(PAN)
        ax.tick_params(colors="#787b86", labelsize=8.5)
        ax.yaxis.label.set_color("#787b86")
        ax.xaxis.label.set_color("#787b86")
        for sp in ax.spines.values():
            sp.set_edgecolor(GRID)
        ax.grid(color=GRID, linewidth=0.5, alpha=0.8)

    # ── 1. HEIKIN ASHI CANDLESTICKS ──────────────────────────────────────────
    _draw_ha_candles(ax1, ha, dir_arr, width_frac=0.55)

    # ── 2. SUPERTREND LINE + SHADING (TradingView style) ────────────────────
    ha_close = ha["HA_Close"].values

    for i in range(1, len(sig)):
        c = GREEN if dir_arr[i] == 1 else RED
        ax1.plot([date_nums[i-1], date_nums[i]],
                 [st_arr[i-1], st_arr[i]],
                 color=c, lw=1.8, zorder=4, solid_capstyle="round")

    # Shaded fill between HA_Close and Supertrend (like TradingView)
    bull_mask = dir_arr == 1
    bear_mask = ~bull_mask

    ax1.fill_between(date_nums, ha_close, st_arr,
                     where=bull_mask,
                     color=GREEN, alpha=0.12, zorder=1, interpolate=True)
    ax1.fill_between(date_nums, ha_close, st_arr,
                     where=bear_mask,
                     color=RED, alpha=0.12, zorder=1, interpolate=True)

    # ── 3. BUY / SELL SIGNAL MARKERS (PDF §7) ────────────────────────────────
    if not long_df.empty:
        entry_dn = mdates.date2num(pd.to_datetime(long_df["Entry Date"]).dt.to_pydatetime())
        exit_dn  = mdates.date2num(pd.to_datetime(long_df["Exit Date"]).dt.to_pydatetime())
        ep = long_df["Entry Price"].astype(float).values
        xp = long_df["Exit Price"].astype(float).values
        ax1.scatter(entry_dn, ep * 0.998, marker="^", color=GREEN,
                    s=220, zorder=8, edgecolors="white", linewidths=0.7,
                    label="Long Entry ▲  (OHLC price)")
        ax1.scatter(exit_dn,  xp * 1.002, marker="v", color="#f39c12",
                    s=220, zorder=8, edgecolors="white", linewidths=0.7,
                    label="Long Exit ▼  (OHLC price)")

    if not short_df.empty:
        entry_dn = mdates.date2num(pd.to_datetime(short_df["Entry Date"]).dt.to_pydatetime())
        exit_dn  = mdates.date2num(pd.to_datetime(short_df["Exit Date"]).dt.to_pydatetime())
        ep = short_df["Entry Price"].astype(float).values
        xp = short_df["Exit Price"].astype(float).values
        ax1.scatter(entry_dn, ep * 1.002, marker="v", color=RED,
                    s=220, zorder=8, edgecolors="white", linewidths=0.7,
                    label="Short Entry ▼  (OHLC price)")
        ax1.scatter(exit_dn,  xp * 0.998, marker="^", color="#9b59b6",
                    s=220, zorder=8, edgecolors="white", linewidths=0.7,
                    label="Short Exit ▲  (OHLC price)")

    # Title & labels
    ax1.set_title(
        f"{name}  ·  Heikin Ashi Candles  +  Supertrend (ATR=7, Mult=3)\n"
        f"⚠  Signal: Heikin Ashi direction change  |  Entry/Exit Price: Original OHLC Close",
        color="#d1d4dc", fontsize=11, fontweight="bold", pad=10, loc="left"
    )
    ax1.set_ylabel("Price (₹)", fontsize=10)
    leg = ax1.legend(loc="upper left", fontsize=8.5,
                     facecolor="#1e222d", edgecolor="#363a45",
                     labelcolor="#c8cdd8", framealpha=0.95)
    plt.setp(ax1.get_xticklabels(), visible=False)

    # ── 4. VOLUME BAR PANEL ───────────────────────────────────────────────────
    if "Volume" in ohlc.columns:
        vol = ohlc["Volume"].values
    else:
        # Estimate volume-like activity from range for visual effect
        vol = ((ohlc["High"] - ohlc["Low"]) / ohlc["Close"] * 1e7).values

    vol_colors = [GREEN if dir_arr[i] == 1 else RED for i in range(len(dates))]
    ax2.bar(date_nums, vol, color=vol_colors, alpha=0.7, width=0.55)
    ax2.set_ylabel("Vol", fontsize=8)
    ax2.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1e3:.0f}K")
    )
    ax2.set_ylim(0, max(vol) * 1.2 if len(vol) > 0 else 1)
    plt.setp(ax2.get_xticklabels(), visible=False)

    # ── 5. PnL PANEL ─────────────────────────────────────────────────────────
    all_t = []
    if not long_df.empty:
        t = long_df[["Exit Date","PnL"]].copy(); all_t.append(t)
    if not short_df.empty:
        t = short_df[["Exit Date","PnL"]].copy(); all_t.append(t)
    if all_t:
        comb = pd.concat(all_t).sort_values("Exit Date")
        comb["Exit Date"] = pd.to_datetime(comb["Exit Date"])
        comb["PnL"]       = comb["PnL"].astype(float)
        comb["Cum"]       = comb["PnL"].cumsum()
        exit_nums = mdates.date2num(comb["Exit Date"].dt.to_pydatetime())
        bc = [GREEN if p > 0 else RED for p in comb["PnL"]]
        ax3.bar(exit_nums, comb["PnL"].values, color=bc, alpha=0.75, width=2.0)
        ax3.plot(exit_nums, comb["Cum"].values, color="#f1c40f",
                 linewidth=2, label="Cumulative PnL", zorder=5)
        ax3.axhline(0, color="#555577", lw=0.8, ls="--")
        ax3.legend(loc="upper left", fontsize=8.5,
                   facecolor="#1e222d", edgecolor="#363a45",
                   labelcolor="#c8cdd8")
        ax3.fill_between(exit_nums, 0, comb["Cum"].values,
                         where=(comb["Cum"].values >= 0),
                         color="#f1c40f", alpha=0.08, interpolate=True)
        ax3.fill_between(exit_nums, 0, comb["Cum"].values,
                         where=(comb["Cum"].values < 0),
                         color=RED, alpha=0.08, interpolate=True)

    ax3.set_ylabel("PnL (₹)", fontsize=9)
    ax3.set_xlabel("Date", fontsize=9)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.setp(ax3.get_xticklabels(), rotation=0, ha="center")

    plt.tight_layout(rect=[0, 0, 1, 1])
    buf = io.BytesIO()
    plt.savefig(buf, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close()
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# HEIKIN ASHI COMPARISON CHART  — shows HA vs original OHLC side by side
# ─────────────────────────────────────────────────────────────────────────────
def build_ha_comparison_chart(ohlc: pd.DataFrame, ha: pd.DataFrame,
                               sig: pd.DataFrame, name: str):
    """
    Two-panel TradingView-style candlestick chart:
      TOP    : Original OHLC candlesticks  — green/red bars (actual entry/exit price source)
      BOTTOM : Heikin Ashi candlesticks    — green/red bars + Supertrend line + signals
    """
    import matplotlib.dates as mdates
    import matplotlib.patches as mpatches

    BG, PAN = "#131722", "#1e222d"

    fig, (ax_ohlc, ax_ha) = plt.subplots(
        2, 1, figsize=(22, 14), sharex=True,
        gridspec_kw={"height_ratios": [1, 1], "hspace": 0.06}
    )
    fig.patch.set_facecolor(BG)
    for ax in (ax_ohlc, ax_ha):
        ax.set_facecolor(PAN)
        ax.tick_params(colors="#787b86", labelsize=9)
        ax.yaxis.label.set_color("#787b86")
        ax.xaxis.label.set_color("#787b86")
        for sp in ax.spines.values():
            sp.set_edgecolor("#2a2e39")

    dir_arr = sig["Direction"].values
    st_arr  = sig["Supertrend"].values
    dates   = ohlc.index
    dnums   = mdates.date2num(dates.to_pydatetime())
    w       = (dnums[1] - dnums[0]) * 0.55 if len(dnums) > 1 else 0.4

    # ─────────────────────────────────────────────────────
    # Helper: draw_candles — TradingView style
    # ─────────────────────────────────────────────────────
    def draw_candles(ax, O, H, L, C, bull_cond, dn, width):
        for i in range(len(dn)):
            bull   = bool(bull_cond[i])
            # TradingView exact colours
            if bull:
                body_col = "#26a65b"   # solid green body
                wick_col = "#1e8449"
                edge_col = "#1a7a40"
            else:
                body_col = "#e74c3c"   # solid red body
                wick_col = "#c0392b"
                edge_col = "#a93226"

            top    = max(O[i], C[i])
            bot    = min(O[i], C[i])
            body_h = max(top - bot, (H[i]-L[i]) * 0.012 + 0.01)

            # Body
            rect = mpatches.FancyBboxPatch(
                (dn[i] - width/2, bot), width, body_h,
                boxstyle="square,pad=0",
                facecolor=body_col, edgecolor=edge_col, linewidth=0.4, zorder=4
            )
            ax.add_patch(rect)
            # Upper wick
            if H[i] > top:
                ax.plot([dn[i], dn[i]], [top, H[i]], color=wick_col, lw=1.0, zorder=3)
            # Lower wick
            if L[i] < bot:
                ax.plot([dn[i], dn[i]], [L[i], bot], color=wick_col, lw=1.0, zorder=3)
        ax.xaxis_date()
        ax.set_xlim(dnums[0] - w, dnums[-1] + w)
        ax.set_ylim(min(L)*0.995, max(H)*1.005)

    # ─────────────────────────────────────────────────────
    # TOP PANEL — Original OHLC candlesticks
    # Candle colour: green if Close >= Open, red if Close < Open
    # ─────────────────────────────────────────────────────
    O  = ohlc["Open"].values
    H  = ohlc["High"].values
    L  = ohlc["Low"].values
    C  = ohlc["Close"].values
    ohlc_bull = C >= O   # standard OHLC colour rule

    draw_candles(ax_ohlc, O, H, L, C, ohlc_bull, dnums, w)

    # Supertrend shading on OHLC panel (matches TradingView)
    for i in range(1, len(sig)):
        bull = dir_arr[i] == 1
        col  = "#26a65b" if bull else "#e74c3c"
        ax_ohlc.plot([dnums[i-1], dnums[i]], [st_arr[i-1], st_arr[i]],
                     color=col, lw=1.8, zorder=5)
    # Fill between price and supertrend
    st_series = sig["Supertrend"].values
    cl_series = ohlc["Close"].values
    for i in range(1, len(sig)):
        bull = dir_arr[i] == 1
        fill = "#26a65b22" if bull else "#e74c3c22"
        ax_ohlc.fill_between(
            [dnums[i-1], dnums[i]],
            [st_series[i-1], st_series[i]],
            [cl_series[i-1], cl_series[i]],
            color=fill, zorder=1
        )

    ax_ohlc.set_title(
        f"{name}  ·  ① ORIGINAL OHLC CANDLESTICKS  —  Actual Entry & Exit Price Source",
        color="#d1d4dc", fontsize=12, fontweight="bold", pad=10
    )
    ax_ohlc.set_ylabel("Price (₹)", fontsize=10)
    ax_ohlc.grid(alpha=0.07, color="#363a45", linestyle="-")

    # Legend patches
    from matplotlib.lines import Line2D
    ohlc_legend = [
        mpatches.Patch(color="#26a65b", label="Bullish Candle (Close ≥ Open)"),
        mpatches.Patch(color="#e74c3c", label="Bearish Candle (Close < Open)"),
        Line2D([0],[0], color="#26a65b", lw=2, label="Supertrend Green"),
        Line2D([0],[0], color="#e74c3c", lw=2, label="Supertrend Red"),
    ]
    ax_ohlc.legend(handles=ohlc_legend, loc="upper left", fontsize=8.5,
                   facecolor="#1e222d", edgecolor="#363a45", labelcolor="#d1d4dc", framealpha=0.9)
    ax_ohlc.text(0.01, 0.04,
                 "★  Entry & Exit prices taken from OHLC Close  (NOT from Heikin Ashi)",
                 transform=ax_ohlc.transAxes, fontsize=9, color="#f1c40f", style="italic",
                 bbox=dict(boxstyle="round,pad=0.35", facecolor="#14140a", edgecolor="#3a3a10", alpha=0.95))
    plt.setp(ax_ohlc.get_xticklabels(), visible=False)

    # ─────────────────────────────────────────────────────
    # BOTTOM PANEL — Heikin Ashi candlesticks
    # Candle colour: by Supertrend direction (like TradingView HA)
    # ─────────────────────────────────────────────────────
    HO = ha["HA_Open"].values
    HH = ha["HA_High"].values
    HL = ha["HA_Low"].values
    HC = ha["HA_Close"].values

    draw_candles(ax_ha, HO, HH, HL, HC, dir_arr == 1, dnums, w)

    # Supertrend line + shading on HA panel
    for i in range(1, len(sig)):
        bull = dir_arr[i] == 1
        col  = "#26a65b" if bull else "#e74c3c"
        ax_ha.plot([dnums[i-1], dnums[i]], [st_arr[i-1], st_arr[i]],
                   color=col, lw=1.8, zorder=5)
    ha_close = ha["HA_Close"].values
    for i in range(1, len(sig)):
        bull = dir_arr[i] == 1
        fill = "#26a65b22" if bull else "#e74c3c22"
        ax_ha.fill_between(
            [dnums[i-1], dnums[i]],
            [st_series[i-1], st_series[i]],
            [ha_close[i-1], ha_close[i]],
            color=fill, zorder=1
        )

    # Buy/Sell signal markers (signals come from HA direction changes)
    lmask = sig["Long_Entry"].values
    smask = sig["Short_Entry"].values
    if lmask.any():
        ax_ha.scatter(dnums[lmask], HL[lmask] * 0.997,
                      marker="^", color="#26a65b", s=220, zorder=8,
                      label="Long Entry ▲ (HA Signal)", edgecolors="white", linewidths=0.8)
    if smask.any():
        ax_ha.scatter(dnums[smask], HH[smask] * 1.003,
                      marker="v", color="#e74c3c", s=220, zorder=8,
                      label="Short Entry ▼ (HA Signal)", edgecolors="white", linewidths=0.8)

    ax_ha.set_title(
        f"{name}  ·  ② HEIKIN ASHI CANDLESTICKS  —  Signal Generation Source  (Supertrend Direction Changes)",
        color="#26a65b", fontsize=12, fontweight="bold", pad=10
    )
    ax_ha.set_ylabel("HA Price (₹)", fontsize=10)
    ax_ha.set_xlabel("Date", fontsize=10)
    ax_ha.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax_ha.grid(alpha=0.07, color="#363a45", linestyle="-")

    ha_legend = [
        mpatches.Patch(color="#26a65b", label="Bullish HA Candle (Supertrend Green)"),
        mpatches.Patch(color="#e74c3c", label="Bearish HA Candle (Supertrend Red)"),
        Line2D([0],[0], marker="^", color="w", markerfacecolor="#26a65b", markersize=10, label="Long Entry ▲"),
        Line2D([0],[0], marker="v", color="w", markerfacecolor="#e74c3c", markersize=10, label="Short Entry ▼"),
    ]
    ax_ha.legend(handles=ha_legend, loc="upper left", fontsize=8.5,
                 facecolor="#1e222d", edgecolor="#363a45", labelcolor="#d1d4dc", framealpha=0.9)
    ax_ha.text(0.01, 0.04,
               "▲▼  Buy/Sell signals generated from HA Supertrend  |  Red→Green = Long  ·  Green→Red = Short",
               transform=ax_ha.transAxes, fontsize=9, color="#26a65b", style="italic",
               bbox=dict(boxstyle="round,pad=0.35", facecolor="#081208", edgecolor="#1a4020", alpha=0.95))

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    buf.seek(0)
    return buf


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — metric card HTML
# ─────────────────────────────────────────────────────────────────────────────
def metric_card(label, value, color_class="metric-blue"):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color_class}">{value}</div>
    </div>"""


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    selected_stock = st.selectbox(
        "📌 Select Instrument",
        list(SYMBOLS.keys()),
        help="RELIANCE, NIFTYBEES,ITC"
    )

    st.markdown("**📅 Date Range**")
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=396)   # 1 year + 1 month
    start_str  = start_date.strftime("%Y-%m-%d")
    end_str    = end_date.strftime("%Y-%m-%d")
    st.caption(f"`{start_str}` → `{end_str}` *(1Y 1M)*")

    st.markdown("**📐 Supertrend Parameters** *(Fixed as per PDF)*")
    st.info("ATR Period : **7**\nMultiplier : **3**")

    st.markdown("---")
    run_btn = st.button("▶  Run Backtest", use_container_width=True)
    live_btn = st.button("🔄  Refresh Live Data", use_container_width=True,
                         help="Fetches the latest quote without re-running the full backtest")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem;color:#404060;line-height:1.6'>
    <b style='color:#5060a0'>Strategy Rules</b><br>
    • Signal from <b>Heikin Ashi</b><br>
    • Price from original <b>OHLC</b><br>
    • Long: Red→Green<br>
    • Short: Green→Red<br>
    • Supertrend ATR=7, Mult=3
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📈 Supertrend Strategy Backtester</h1>
    <p>YRS Innovations LLP · Python Developer Assignment II · Heikin Ashi + Supertrend (ATR=7, Mult=3)</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────────────────────────────────────
if not run_btn and not live_btn:
    st.markdown("""
    <div class="info-box">
        👈 Select an instrument from the sidebar and click <b>▶ Run Backtest</b> to begin.
        All three instruments (RELIANCE ,NIFTYBEES ,ITC) can be analysed individually.
        Use <b>🔄 Refresh Live Data</b> for a quick live quote without a full backtest.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        ("RELIANCE.NS", "Reliance Industries", "Large-cap energy & retail conglomerate"),
        ("NIFTYBEES.NS","Nippon Nifty BeES ETF", "Tracks Nifty 50 — passive index fund"),
        ("ITC.NS",      "ITC Limited",          "FMCG, hotels, agribusiness, paperboards"),
    ]
    for col, (ticker, title, desc) in zip([col1,col2,col3], cards):
        col.markdown(f"""
        <div class="metric-card" style="text-align:left;padding:20px">
            <div style="font-family:'Space Mono',monospace;color:#7eb8f7;
                        font-size:0.85rem;margin-bottom:6px">{ticker}</div>
            <div style="color:#d0d8f0;font-weight:600;margin-bottom:4px">{title}</div>
            <div style="color:#506080;font-size:0.8rem">{desc}</div>
        </div>""", unsafe_allow_html=True)

elif live_btn and not run_btn:
    # Quick live data without full backtest
    ticker = SYMBOLS[selected_stock]
    st.markdown(f"### ⚡ Live Quote — {selected_stock}")
    with st.spinner("Fetching live quote..."):
        live = fetch_live_data(ticker)
    if live["status"] == "ok":
        price_col = live["color"]
        chg_sign  = "+" if live["change"] >= 0 else ""
        lc1, lc2, lc3, lc4, lc5 = st.columns(5)
        lc1.markdown(metric_card("Live Price (₹)",   f"₹{live['last_price']:,.2f}", "metric-yellow"), unsafe_allow_html=True)
        lc2.markdown(metric_card("Change",            f"{chg_sign}{live['change']:,.2f} ({chg_sign}{live['change_pct']:.2f}%)",
                                 "metric-green" if live["change"] >= 0 else "metric-red"), unsafe_allow_html=True)
        lc3.markdown(metric_card("Day High",          f"₹{live['day_high']:,.2f}", "metric-blue"), unsafe_allow_html=True)
        lc4.markdown(metric_card("Day Low",           f"₹{live['day_low']:,.2f}", "metric-blue"), unsafe_allow_html=True)
        lc5.markdown(metric_card("Prev Close",        f"₹{live['prev_close']:,.2f}", "metric-blue"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
            ⏱ Last update: <b style="color:#7eb8f7">{live.get('last_update','N/A')}</b>
            &nbsp;|&nbsp; <b style="color:{price_col}">{live['direction']}</b>
        </div>""", unsafe_allow_html=True)
        st.info("Run a full backtest to see the Supertrend signal alongside live data.")

else:
    ticker = SYMBOLS[selected_stock]

    with st.spinner(f"Fetching data & running backtest for {selected_stock}..."):

        # 1. Data — original OHLC (used for actual entry/exit prices)
        ohlc = fetch_data(ticker, start_str, end_str)

        # 2. Heikin Ashi (PDF §4) — used ONLY for signal generation
        ha = heikin_ashi(ohlc)

        # 3. Supertrend on HA (PDF §5) — signals derived from HA candles
        st_df = supertrend(ha, period=7, mult=3)

        # 4. Signals from HA direction changes (PDF §6)
        sig = generate_signals(st_df)

        # 5. Backtest — signal from HA, but entry/exit PRICE from original OHLC (PDF §4 ⚠ rule)
        long_df, short_df = backtest(ohlc, sig)

        # 6. Metrics (PDF §8)
        lm = calc_metrics(long_df,  "Long")
        sm = calc_metrics(short_df, "Short")

        # 7. Charts
        chart_buf    = build_chart(ohlc, sig, long_df, short_df, selected_stock)
        ha_chart_buf = build_ha_comparison_chart(ohlc, ha, sig, selected_stock)

    # ── LIVE / ACUTE DATA PANEL ───────────────────────────────────────────────
    st.markdown('<div class="section-title">⚡ Live / Acute Market Data</div>',
                unsafe_allow_html=True)

    with st.spinner("Fetching live quote..."):
        live = fetch_live_data(ticker)

    if live["status"] == "ok":
        # Current Supertrend signal from latest historical bar
        last_dir   = int(sig["Direction"].iloc[-1])
        live_signal = "🟢 BUY (Bullish)" if last_dir == 1 else "🔴 SELL (Bearish)"
        signal_col  = "#2ecc71" if last_dir == 1 else "#e74c3c"

        price_col = live["color"]
        arrow     = live["direction"]
        chg_sign  = "+" if live["change"] >= 0 else ""

        lc1, lc2, lc3, lc4, lc5, lc6 = st.columns(6)
        lc1.markdown(metric_card("Live Price (₹)",
                                 f"₹{live['last_price']:,.2f}",
                                 "metric-yellow"), unsafe_allow_html=True)
        lc2.markdown(metric_card("Change",
                                 f"{chg_sign}{live['change']:,.2f} ({chg_sign}{live['change_pct']:.2f}%)",
                                 "metric-green" if live["change"] >= 0 else "metric-red"),
                     unsafe_allow_html=True)
        lc3.markdown(metric_card("Day High",
                                 f"₹{live['day_high']:,.2f}", "metric-blue"),
                     unsafe_allow_html=True)
        lc4.markdown(metric_card("Day Low",
                                 f"₹{live['day_low']:,.2f}", "metric-blue"),
                     unsafe_allow_html=True)
        lc5.markdown(metric_card("Prev Close",
                                 f"₹{live['prev_close']:,.2f}", "metric-blue"),
                     unsafe_allow_html=True)
        lc6.markdown(metric_card("Supertrend Signal", live_signal, "metric-green" if last_dir == 1 else "metric-red"),
                     unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-box" style="border-left-color:{signal_col};margin-top:8px">
            <span style="color:#a0b0c0;font-size:0.82rem">
            ⏱ Last update: <b style="color:#7eb8f7">{live.get('last_update','N/A')}</b>
            &nbsp;|&nbsp; Direction: <b style="color:{price_col}">{arrow}</b>
            &nbsp;|&nbsp; Current Supertrend: <b style="color:{signal_col}">{live_signal}</b>
            &nbsp;|&nbsp; <span style="color:#506080">Prices from yfinance NSE feed</span>
            </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Live data unavailable: {live.get('msg','Unknown error')}. "
                   "Backtested data is still shown below.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SUMMARY BAR ──────────────────────────────────────────────────────────
    st.markdown(f"### 📊 Results — {selected_stock}")
    st.caption(f"Data: {ohlc.index[0].date()} → {ohlc.index[-1].date()} "
               f"| {len(ohlc)} trading days")

    # ── ⚠ HEIKIN ASHI IMPORTANT RULE BANNER ─────────────────────────────────
    st.markdown("""
    <div class="ha-rule-banner">
        <div class="ha-title">⚠️  CANDLESTICK RULE — PDF §4 : Heikin Ashi Strategy</div>
        <div class="ha-grid">
            <div class="ha-col">
                <div class="ha-col-title-green">✅ Signal Source — Heikin Ashi Candles</div>
                <div class="ha-col-body">
                    • Supertrend indicator calculated on HA (Open, High, Low, Close)<br>
                    • Long Entry signal: HA Supertrend changes <b>Red → Green</b><br>
                    • Short Entry signal: HA Supertrend changes <b>Green → Red</b><br>
                    • HA smooths price action → cleaner trend signals
                </div>
            </div>
            <div class="ha-col">
                <div class="ha-col-title-red">📌 Price Source — Original OHLC Candles</div>
                <div class="ha-col-body">
                    • Actual Entry Price = Original OHLC <b>Close</b> at signal bar<br>
                    • Actual Exit Price  = Original OHLC <b>Close</b> at exit bar<br>
                    • PnL calculated using real market prices, not HA prices<br>
                    • Ensures realistic trade execution prices
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Chart", "🕯️ HA vs OHLC", "🟢 Long Trades", "🔴 Short Trades", "📋 Summary"
    ])

    # ────────── TAB 1 : CHART ────────────────────────────────────────────────
    with tab1:
        st.image(chart_buf, use_container_width=True)
        chart_buf.seek(0)
        st.download_button(
            "⬇ Download Chart (PNG)",
            data=chart_buf,
            file_name=f"{selected_stock}_supertrend_chart.png",
            mime="image/png"
        )

    # ────────── TAB 2 : HEIKIN ASHI vs OHLC ─────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">🕯️ Heikin Ashi vs Original OHLC — Signal vs Price Source</div>',
                    unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        col_a.markdown("""
        <div class="metric-card" style="text-align:left;padding:16px;border-left:3px solid #2ecc71">
            <div style="color:#2ecc71;font-weight:700;margin-bottom:8px;font-family:'Space Mono',monospace">
                ① HEIKIN ASHI CANDLES
            </div>
            <div style="color:#80a880;font-size:0.83rem;line-height:1.7">
                <b>Formula:</b><br>
                HA Close = (O + H + L + C) / 4<br>
                HA Open  = (prev HA Open + prev HA Close) / 2<br>
                HA High  = max(High, HA Open, HA Close)<br>
                HA Low   = min(Low,  HA Open, HA Close)<br><br>
                <b>Purpose:</b> Smooth out noise → derive Supertrend direction<br>
                <b>Used for:</b> Generating BUY / SELL signals only
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_b.markdown("""
        <div class="metric-card" style="text-align:left;padding:16px;border-left:3px solid #e74c3c">
            <div style="color:#e87060;font-weight:700;margin-bottom:8px;font-family:'Space Mono',monospace">
                ② ORIGINAL OHLC CANDLES
            </div>
            <div style="color:#a08080;font-size:0.83rem;line-height:1.7">
                <b>Source:</b> Yahoo Finance (NSE daily data)<br>
                <b>Columns:</b> Open, High, Low, Close<br><br>
                <b>Entry Price:</b> OHLC Close on signal bar<br>
                <b>Exit Price:</b>  OHLC Close on exit bar<br>
                <b>PnL Calc:</b>   Exit Price − Entry Price (Long)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Entry Price − Exit Price (Short)<br><br>
                <b>Purpose:</b> Realistic execution prices for P&L
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.image(ha_chart_buf, use_container_width=True)

        ha_chart_buf.seek(0)
        st.download_button(
            "⬇ Download HA vs OHLC Chart (PNG)",
            data=ha_chart_buf,
            file_name=f"{selected_stock}_ha_vs_ohlc.png",
            mime="image/png"
        )

        # Show HA data table
        st.markdown('<div class="section-title">Heikin Ashi Data (last 20 bars)</div>',
                    unsafe_allow_html=True)
        ha_display = ha[["HA_Open","HA_High","HA_Low","HA_Close"]].tail(20).copy()
        ha_display.index = ha_display.index.strftime("%Y-%m-%d")
        ha_display.columns = ["HA Open","HA High","HA Low","HA Close"]
        ha_display = ha_display.round(2)

        ohlc_display = ohlc[["Open","High","Low","Close"]].tail(20).copy()
        ohlc_display.index = ohlc_display.index.strftime("%Y-%m-%d")
        ohlc_display = ohlc_display.round(2)

        c1, c2 = st.columns(2)
        with c1:
            st.caption("🟢 Heikin Ashi (Signal Source)")
            st.dataframe(ha_display.style.set_properties(
                **{"background-color":"#0a120a","color":"#80c880"}),
                use_container_width=True, height=300)
        with c2:
            st.caption("📌 Original OHLC (Price Source)")
            st.dataframe(ohlc_display.style.set_properties(
                **{"background-color":"#0f0f1e","color":"#c0cce0"}),
                use_container_width=True, height=300)

    # ────────── TAB 3 : LONG TRADES ──────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">🟢 LONG TRADES METRICS</div>',
                    unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        pnl_color = "metric-green" if lm["pnl"] >= 0 else "metric-red"
        c1.markdown(metric_card("Total Trades",   str(lm["total"]),    "metric-blue"),     unsafe_allow_html=True)
        c2.markdown(metric_card("Total PnL (₹)",  f"₹{lm['pnl']:,.2f}", pnl_color),        unsafe_allow_html=True)
        c3.markdown(metric_card("Win Rate",        lm["win_rate"],      "metric-green"),    unsafe_allow_html=True)
        c4.markdown(metric_card("Max Drawdown",    f"₹{lm['max_dd']:,.2f}", "metric-yellow"), unsafe_allow_html=True)

        if not long_df.empty:
            st.markdown('<div class="section-title">Long Trade Log</div>',
                        unsafe_allow_html=True)

            display_long = long_df[["Entry Date","Entry Price","Exit Date","Exit Price","PnL"]].copy()
            display_long["Result"] = display_long["PnL"].apply(
                lambda x: "✅ Win" if x > 0 else "❌ Loss"
            )

            def color_pnl(val):
                color = "#2ecc71" if val > 0 else "#e74c3c"
                return f"color: {color}; font-weight: bold"

            styled = display_long.style\
                .applymap(color_pnl, subset=["PnL"])\
                .format({"Entry Price":"₹{:.2f}","Exit Price":"₹{:.2f}","PnL":"₹{:.2f}"})\
                .set_properties(**{"background-color":"#0f0f1e","color":"#c0cce0"})
            st.dataframe(styled, use_container_width=True, height=300)

            # CSV download (PDF §7)
            csv_long = long_df[["Entry Date","Entry Price","Exit Date","Exit Price"]].to_csv(index=False)
            st.download_button(
                "⬇ Download Long Trades CSV",
                data=csv_long,
                file_name=f"{selected_stock}_long_trades.csv",
                mime="text/csv"
            )
        else:
            st.info("No long trades generated in this period.")

    # ────────── TAB 4 : SHORT TRADES ─────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">🔴 SHORT TRADES METRICS</div>',
                    unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        pnl_color = "metric-green" if sm["pnl"] >= 0 else "metric-red"
        c1.markdown(metric_card("Total Trades",   str(sm["total"]),    "metric-blue"),      unsafe_allow_html=True)
        c2.markdown(metric_card("Total PnL (₹)",  f"₹{sm['pnl']:,.2f}", pnl_color),         unsafe_allow_html=True)
        c3.markdown(metric_card("Win Rate",        sm["win_rate"],      "metric-green"),     unsafe_allow_html=True)
        c4.markdown(metric_card("Max Drawdown",    f"₹{sm['max_dd']:,.2f}", "metric-yellow"), unsafe_allow_html=True)

        if not short_df.empty:
            st.markdown('<div class="section-title">Short Trade Log</div>',
                        unsafe_allow_html=True)

            display_short = short_df[["Entry Date","Entry Price","Exit Date","Exit Price","PnL"]].copy()
            display_short["Result"] = display_short["PnL"].apply(
                lambda x: "✅ Win" if x > 0 else "❌ Loss"
            )

            def color_pnl2(val):
                color = "#2ecc71" if val > 0 else "#e74c3c"
                return f"color: {color}; font-weight: bold"

            styled2 = display_short.style\
                .applymap(color_pnl2, subset=["PnL"])\
                .format({"Entry Price":"₹{:.2f}","Exit Price":"₹{:.2f}","PnL":"₹{:.2f}"})\
                .set_properties(**{"background-color":"#0f0f1e","color":"#c0cce0"})
            st.dataframe(styled2, use_container_width=True, height=300)

            csv_short = short_df[["Entry Date","Entry Price","Exit Date","Exit Price"]].to_csv(index=False)
            st.download_button(
                "⬇ Download Short Trades CSV",
                data=csv_short,
                file_name=f"{selected_stock}_short_trades.csv",
                mime="text/csv"
            )
        else:
            st.info("No short trades generated in this period.")

    # ────────── TAB 5 : SUMMARY ──────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-title">📋 PERFORMANCE SUMMARY</div>',
                    unsafe_allow_html=True)

        summary_data = {
            "Metric":       ["Total Trades", "Total PnL (₹)", "Win Rate", "Max Drawdown (₹)", "Avg PnL/Trade (₹)"],
            "Long  Trades": [lm["total"], f"₹{lm['pnl']:,.2f}", lm["win_rate"],
                             f"₹{lm['max_dd']:,.2f}", f"₹{lm['avg_pnl']:,.2f}"],
            "Short Trades": [sm["total"], f"₹{sm['pnl']:,.2f}", sm["win_rate"],
                             f"₹{sm['max_dd']:,.2f}", f"₹{sm['avg_pnl']:,.2f}"],
        }
        st.dataframe(
            pd.DataFrame(summary_data).set_index("Metric"),
            use_container_width=True
        )

        st.markdown("---")
        st.markdown('<div class="section-title">ℹ️ Strategy Notes</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box">
        <b>Data Source:</b> Yahoo Finance via <code>yfinance</code> (NSE tickers: .NS suffix)<br><br>
        <b style="color:#f1c40f">⚠️ Candlestick Rule (PDF §4):</b><br>
        &nbsp;&nbsp;• <b>Signal Generation</b> → Heikin Ashi candles (HA_Open, HA_High, HA_Low, HA_Close)<br>
        &nbsp;&nbsp;• <b>Entry / Exit Price</b> → Original OHLC <b>Close</b> price (real market price)<br><br>
        <b>Indicator:</b> Supertrend ATR Period=7, Multiplier=3 (Wilder's EWM smoothing) on HA<br>
        <b>Long Entry:</b> HA Supertrend Red → Green (Direction: -1 → +1)<br>
        <b>Short Entry:</b> HA Supertrend Green → Red (Direction: +1 → -1)<br>
        <b>Max Drawdown:</b> Calculated on cumulative PnL curve<br>
        <b>Open Positions:</b> Closed at last available OHLC bar price
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#303050;font-size:0.78rem;padding:8px'>
    YRS Innovations LLP · Python Developer Assignment II ·
    Supertrend Strategy on Heikin Ashi · NSE Instruments
</div>""", unsafe_allow_html=True)
