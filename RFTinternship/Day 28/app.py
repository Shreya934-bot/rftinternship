import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st




st.set_page_config(
    page_title="Shreya Verma | Portfolio Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# BRAND SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.02em;
    }

    .stApp {
        background:
            radial-gradient(circle at 90% 5%, rgba(124, 92, 255, 0.09), transparent 24%),
            radial-gradient(circle at 5% 20%, rgba(0, 200, 180, 0.06), transparent 20%);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,.18);
    }

    .brand-mark {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .15rem;
    }

    .brand-sub {
        color: #858585;
        font-size: .76rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 1.8rem;
    }

    .hero {
        padding: 1.8rem 0 .9rem 0;
    }

    .eyebrow {
        color: #777;
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: .5rem;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2.1rem, 4vw, 3.8rem);
        line-height: 1.02;
        font-weight: 700;
        margin: 0;
    }

    .hero-copy {
        color: #777;
        max-width: 720px;
        font-size: 1rem;
        line-height: 1.7;
        margin-top: .75rem;
    }

    .section-kicker {
        color: #777;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: -.45rem;
    }

    .insight {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128,128,128,.18);
        border-radius: 16px;
        background: rgba(128,128,128,.045);
        min-height: 95px;
    }

    .insight-label {
        color: #777;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .09em;
        text-transform: uppercase;
    }

    .insight-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: .3rem;
    }

    .insight-copy {
        color: #777;
        font-size: .8rem;
        margin-top: .25rem;
    }

    .footer {
        color: #777;
        text-align: center;
        font-size: .76rem;
        padding: 2rem 0 1rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.16);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        background: rgba(128,128,128,.035);
    }

    .stDownloadButton button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA FUNCTIONS
# ============================================================

REQUIRED_COLUMNS = {"Date", "Ticker", "Sector", "Close", "Quantity"}


@st.cache_data
def load_data(file_bytes=None):
    if file_bytes is None:
        default_file = Path("stock_prices.csv")
        if not default_file.exists():
            raise FileNotFoundError(
                "No stock_prices.csv found. Upload a CSV from the sidebar."
            )
        df = pd.read_csv(default_file)
    else:
        df = pd.read_csv(io.BytesIO(file_bytes))

    df.columns = df.columns.str.strip()

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(sorted(missing))}"
        )

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    df["Ticker"] = df["Ticker"].astype(str).str.strip().str.upper()
    df["Sector"] = df["Sector"].astype(str).str.strip()

    df = df.dropna(
        subset=["Date", "Ticker", "Sector", "Close", "Quantity"]
    )

    df = df[
        (df["Close"] > 0) &
        (df["Quantity"] > 0)
    ].copy()

    return df.sort_values(["Ticker", "Date"]).reset_index(drop=True)


def build_portfolio(df):
    first = (
        df.sort_values("Date")
        .groupby("Ticker", as_index=False)
        .first()
    )

    last = (
        df.sort_values("Date")
        .groupby("Ticker", as_index=False)
        .last()
    )

    portfolio = first[
        ["Ticker", "Sector", "Quantity", "Close"]
    ].rename(columns={"Close": "Buy Price"})

    latest = last[
        ["Ticker", "Close"]
    ].rename(columns={"Close": "Current Price"})

    portfolio = portfolio.merge(latest, on="Ticker")

    portfolio["Investment"] = (
        portfolio["Buy Price"] * portfolio["Quantity"]
    )
    portfolio["Current Value"] = (
        portfolio["Current Price"] * portfolio["Quantity"]
    )
    portfolio["Profit/Loss"] = (
        portfolio["Current Value"] - portfolio["Investment"]
    )
    portfolio["Return %"] = (
        portfolio["Profit/Loss"] /
        portfolio["Investment"] * 100
    )

    total = portfolio["Investment"].sum()
    portfolio["Allocation %"] = (
        portfolio["Investment"] / total * 100
        if total else 0
    )

    return portfolio.sort_values(
        "Return %", ascending=False
    ).reset_index(drop=True)


def build_daily(df):
    data = df.copy()
    data["Position Value"] = data["Close"] * data["Quantity"]

    daily = (
        data.groupby("Date", as_index=False)
        .agg(Portfolio_Value=("Position Value", "sum"))
        .sort_values("Date")
    )

    daily["Daily Return %"] = (
        daily["Portfolio_Value"].pct_change() * 100
    )

    starting = daily["Portfolio_Value"].iloc[0]

    daily["Cumulative Return %"] = (
        (daily["Portfolio_Value"] / starting) - 1
    ) * 100

    daily["Running Peak"] = (
        daily["Portfolio_Value"].cummax()
    )

    daily["Drawdown %"] = (
        (daily["Portfolio_Value"] /
         daily["Running Peak"]) - 1
    ) * 100

    daily["Rolling Volatility %"] = (
        daily["Daily Return %"]
        .rolling(10)
        .std()
        * np.sqrt(252)
    )

    return daily


def moving_average_analysis(df, window):
    rows = []

    for ticker, group in df.groupby("Ticker"):
        group = group.sort_values("Date")
        closes = group["Close"]

        latest = closes.iloc[-1]
        ma = closes.tail(window).mean()

        if latest > ma:
            trend = "UP"
        elif latest < ma:
            trend = "DOWN"
        else:
            trend = "SIDEWAYS"

        distance = ((latest - ma) / ma) * 100

        rows.append(
            {
                "Ticker": ticker,
                "Latest Price": latest,
                f"{window}D MA": ma,
                "Distance from MA %": distance,
                "Trend": trend,
            }
        )

    return pd.DataFrame(rows)


def format_currency(value):
    return f"₹{value:,.0f}"


def style_figure(fig, title=None):
    fig.update_layout(
        title=title,
        template="plotly_white",
        margin=dict(l=10, r=10, t=55, b=10),
        hovermode="x unified",
        font=dict(family="DM Sans"),
    )
    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="brand-mark">SHREYA VERMA</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="brand-sub">Data • ML • Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Portfolio Input")

    uploaded_file = st.file_uploader(
        "Upload stock CSV",
        type=["csv"],
        help="Required: Date, Ticker, Sector, Close, Quantity",
    )

    st.markdown("---")
    st.markdown("### Filters")

    date_placeholder = st.empty()
    ticker_placeholder = st.empty()
    sector_placeholder = st.empty()

    st.markdown("---")
    st.markdown("### Analysis")

    ma_window = st.slider(
        "Moving average window",
        min_value=3,
        max_value=30,
        value=5,
        step=1,
    )

    risk_free_rate = st.number_input(
        "Risk-free rate (%)",
        min_value=0.0,
        max_value=20.0,
        value=0.0,
        step=0.5,
    )


# ============================================================
# LOAD DATA
# ============================================================

file_bytes = uploaded_file.getvalue() if uploaded_file else None

try:
    df = load_data(file_bytes)
except Exception as error:
    st.error(f"Unable to load portfolio data: {error}")
    st.stop()


# ============================================================
# FILTERS
# ============================================================

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = date_placeholder.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

selected_tickers = ticker_placeholder.multiselect(
    "Stocks",
    sorted(df["Ticker"].unique()),
    default=sorted(df["Ticker"].unique()),
)

selected_sectors = sector_placeholder.multiselect(
    "Sectors",
    sorted(df["Sector"].unique()),
    default=sorted(df["Sector"].unique()),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

filtered = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date) &
    (df["Ticker"].isin(selected_tickers)) &
    (df["Sector"].isin(selected_sectors))
].copy()

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()


# ============================================================
# CALCULATIONS
# ============================================================

portfolio = build_portfolio(filtered)
daily = build_daily(filtered)

total_investment = portfolio["Investment"].sum()
current_value = portfolio["Current Value"].sum()
profit_loss = current_value - total_investment
overall_return = (
    profit_loss / total_investment * 100
    if total_investment else 0
)

best = portfolio.iloc[0]
worst = portfolio.iloc[-1]

daily_returns = daily["Daily Return %"].dropna()

annualized_volatility = (
    daily_returns.std() * np.sqrt(252)
    if len(daily_returns) > 1 else 0
)

mean_daily_return = (
    daily_returns.mean()
    if len(daily_returns) else 0
)

sharpe = (
    ((mean_daily_return * 252) - risk_free_rate) /
    annualized_volatility
    if annualized_volatility else 0
)

max_drawdown = daily["Drawdown %"].min()

winning_days = (
    (daily_returns > 0).sum()
    if len(daily_returns) else 0
)

losing_days = (
    (daily_returns < 0).sum()
    if len(daily_returns) else 0
)

win_rate = (
    winning_days / len(daily_returns) * 100
    if len(daily_returns) else 0
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Day 28 · Python Internship Journey</div>
        <div class="hero-title">Portfolio Intelligence.</div>
        <div class="hero-copy">
            A focused view of portfolio performance, allocation, risk and
            momentum — built as a practical data analytics project.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Analysis window: {start_date.strftime('%d %b %Y')} — "
    f"{end_date.strftime('%d %b %Y')} · "
    f"{len(portfolio)} holdings · {len(filtered):,} price records"
)


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Portfolio Value",
    format_currency(current_value),
)

k2.metric(
    "Profit / Loss",
    format_currency(profit_loss),
    f"{overall_return:.2f}%",
)

k3.metric(
    "Best Performer",
    best["Ticker"],
    f"{best['Return %']:.2f}%",
)

k4.metric(
    "Max Drawdown",
    f"{max_drawdown:.2f}%",
)

k5.metric(
    "Annualized Volatility",
    f"{annualized_volatility:.2f}%",
)


# ============================================================
# QUICK INSIGHTS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<div class="section-kicker">Signal board</div>',
    unsafe_allow_html=True,
)
st.subheader("What the portfolio is saying")

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">Strongest holding</div>
            <div class="insight-value">{best['Ticker']}</div>
            <div class="insight-copy">
                Return of {best['Return %']:.2f}% across the selected window.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i2:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">Largest allocation</div>
            <div class="insight-value">
                {portfolio.iloc[portfolio['Allocation %'].idxmax()]['Ticker']}
            </div>
            <div class="insight-copy">
                {portfolio['Allocation %'].max():.1f}% of initial investment.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with i3:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">Positive trading days</div>
            <div class="insight-value">{win_rate:.1f}%</div>
            <div class="insight-copy">
                {winning_days} positive vs {losing_days} negative sessions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TABS
# ============================================================

tab_overview, tab_holdings, tab_risk, tab_momentum, tab_export = st.tabs(
    [
        "Overview",
        "Holdings",
        "Risk & Returns",
        "Momentum",
        "Export",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with tab_overview:

    st.markdown("### Portfolio trajectory")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily["Date"],
            y=daily["Portfolio_Value"],
            mode="lines",
            name="Portfolio Value",
            line=dict(width=3),
        )
    )

    fig.update_yaxes(tickprefix="₹", separatethousands=True)
    fig.update_xaxes(title="")
    fig = style_figure(
        fig,
        "Portfolio Value Over Time",
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Sector allocation")

        sector = (
            portfolio.groupby("Sector", as_index=False)
            .agg(
                Investment=("Investment", "sum"),
                Current_Value=("Current Value", "sum"),
            )
        )

        fig_sector = px.pie(
            sector,
            names="Sector",
            values="Investment",
            hole=0.62,
        )

        fig_sector.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        fig_sector = style_figure(
            fig_sector,
            "Initial Investment Allocation",
        )

        st.plotly_chart(fig_sector, use_container_width=True)

    with right:
        st.markdown("### Stock returns")

        returns = portfolio.sort_values("Return %")

        fig_returns = px.bar(
            returns,
            x="Return %",
            y="Ticker",
            orientation="h",
            text="Return %",
        )

        fig_returns.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
        )

        fig_returns = style_figure(
            fig_returns,
            "Performance by Holding",
        )

        st.plotly_chart(fig_returns, use_container_width=True)


# ============================================================
# HOLDINGS
# ============================================================

with tab_holdings:

    st.markdown("### Holdings intelligence")

    display_df = portfolio[
        [
            "Ticker",
            "Sector",
            "Quantity",
            "Buy Price",
            "Current Price",
            "Investment",
            "Current Value",
            "Profit/Loss",
            "Return %",
            "Allocation %",
        ]
    ].copy()

    st.dataframe(
        display_df.style.format(
            {
                "Buy Price": "₹{:,.2f}",
                "Current Price": "₹{:,.2f}",
                "Investment": "₹{:,.2f}",
                "Current Value": "₹{:,.2f}",
                "Profit/Loss": "₹{:,.2f}",
                "Return %": "{:.2f}%",
                "Allocation %": "{:.2f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Concentration")

    concentration = portfolio.nlargest(
        min(5, len(portfolio)),
        "Allocation %",
    )

    fig_concentration = px.bar(
        concentration,
        x="Ticker",
        y="Allocation %",
        text="Allocation %",
    )

    fig_concentration.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
    )

    fig_concentration = style_figure(
        fig_concentration,
        "Top Portfolio Allocations",
    )

    st.plotly_chart(
        fig_concentration,
        use_container_width=True,
    )


# ============================================================
# RISK & RETURNS
# ============================================================

with tab_risk:

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("Sharpe Ratio", f"{sharpe:.2f}")
    r2.metric("Max Drawdown", f"{max_drawdown:.2f}%")
    r3.metric("Daily Win Rate", f"{win_rate:.1f}%")
    r4.metric("Average Daily Return", f"{mean_daily_return:.3f}%")

    left, right = st.columns(2)

    with left:
        fig_return = px.line(
            daily,
            x="Date",
            y="Daily Return %",
            markers=True,
        )

        fig_return.add_hline(y=0, line_width=1)

        fig_return = style_figure(
            fig_return,
            "Daily Return Profile",
        )

        st.plotly_chart(
            fig_return,
            use_container_width=True,
        )

    with right:
        fig_drawdown = px.area(
            daily,
            x="Date",
            y="Drawdown %",
        )

        fig_drawdown = style_figure(
            fig_drawdown,
            "Portfolio Drawdown",
        )

        st.plotly_chart(
            fig_drawdown,
            use_container_width=True,
        )

    fig_vol = px.line(
        daily,
        x="Date",
        y="Rolling Volatility %",
    )

    fig_vol = style_figure(
        fig_vol,
        "10-Day Rolling Annualized Volatility",
    )

    st.plotly_chart(
        fig_vol,
        use_container_width=True,
    )


# ============================================================
# MOMENTUM
# ============================================================

with tab_momentum:

    st.markdown("### Moving-average trend engine")

    prediction = moving_average_analysis(
        filtered,
        ma_window,
    )

    up_count = (prediction["Trend"] == "UP").sum()
    down_count = (prediction["Trend"] == "DOWN").sum()

    m1, m2, m3 = st.columns(3)

    m1.metric("Window", f"{ma_window} days")
    m2.metric("Bullish Signals", up_count)
    m3.metric("Bearish Signals", down_count)

    st.dataframe(
        prediction.style.format(
            {
                "Latest Price": "₹{:,.2f}",
                f"{ma_window}D MA": "₹{:,.2f}",
                "Distance from MA %": "{:.2f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    selected_for_chart = st.selectbox(
        "Inspect a stock",
        sorted(filtered["Ticker"].unique()),
    )

    stock = (
        filtered[filtered["Ticker"] == selected_for_chart]
        .sort_values("Date")
        .copy()
    )

    stock["Moving Average"] = (
        stock["Close"].rolling(ma_window).mean()
    )

    fig_ma = go.Figure()

    fig_ma.add_trace(
        go.Scatter(
            x=stock["Date"],
            y=stock["Close"],
            mode="lines",
            name="Close",
            line=dict(width=2.5),
        )
    )

    fig_ma.add_trace(
        go.Scatter(
            x=stock["Date"],
            y=stock["Moving Average"],
            mode="lines",
            name=f"{ma_window}D Moving Average",
            line=dict(width=2, dash="dash"),
        )
    )

    fig_ma.update_yaxes(
        tickprefix="₹",
        separatethousands=True,
    )

    fig_ma = style_figure(
        fig_ma,
        f"{selected_for_chart} — Price vs Moving Average",
    )

    st.plotly_chart(
        fig_ma,
        use_container_width=True,
    )

    st.caption(
        "The moving-average signal is an educational momentum indicator, "
        "not a guaranteed prediction or financial advice."
    )


# ============================================================
# EXPORT
# ============================================================

with tab_export:

    st.markdown("### Take the analysis with you")

    portfolio_csv = portfolio.to_csv(index=False).encode("utf-8")
    daily_csv = daily.to_csv(index=False).encode("utf-8")
    prediction_csv = prediction.to_csv(index=False).encode("utf-8")

    e1, e2, e3 = st.columns(3)

    with e1:
        st.download_button(
            "Download portfolio report",
            portfolio_csv,
            "shreya_portfolio_report.csv",
            "text/csv",
            use_container_width=True,
        )

    with e2:
        st.download_button(
            "Download daily returns",
            daily_csv,
            "shreya_daily_returns.csv",
            "text/csv",
            use_container_width=True,
        )

    with e3:
        st.download_button(
            "Download momentum signals",
            prediction_csv,
            "shreya_moving_average_signals.csv",
            "text/csv",
            use_container_width=True,
        )

    st.markdown("---")

    summary = pd.DataFrame(
        {
            "Metric": [
                "Analysis Start",
                "Analysis End",
                "Holdings",
                "Total Investment",
                "Current Value",
                "Profit/Loss",
                "Overall Return",
                "Best Performer",
                "Worst Performer",
                "Max Drawdown",
                "Annualized Volatility",
                "Sharpe Ratio",
            ],
            "Value": [
                start_date.strftime("%d %b %Y"),
                end_date.strftime("%d %b %Y"),
                len(portfolio),
                format_currency(total_investment),
                format_currency(current_value),
                format_currency(profit_loss),
                f"{overall_return:.2f}%",
                f"{best['Ticker']} ({best['Return %']:.2f}%)",
                f"{worst['Ticker']} ({worst['Return %']:.2f}%)",
                f"{max_drawdown:.2f}%",
                f"{annualized_volatility:.2f}%",
                f"{sharpe:.2f}",
            ],
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>SHREYA VERMA</strong> · Data • ML • Analytics<br>
        Day 28 — Python Internship Journey · Built with Python, Pandas,
        Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
