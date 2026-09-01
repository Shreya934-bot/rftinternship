import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import tempfile

from expense_tracker import (
    load_dataset,
    prepare_data,
    category_summary,
    monthly_summary,
    daily_summary,
    budget_analysis,
    predict_next_month,
    DEFAULT_BUDGETS,
)

# ============================================================
# PAGE + BRANDING
# ============================================================

st.set_page_config(
    page_title="SV | Smart Expense Tracker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #080b12;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.brand {
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom: 4px;
}

.brand-mark {
    width:48px;
    height:48px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#8b5cf6,#06b6d4);
    color:white;
    font-family:'Space Grotesk';
    font-weight:700;
    font-size:18px;
    box-shadow:0 10px 30px rgba(99,102,241,.25);
}

.brand-name {
    font-family:'Space Grotesk';
    font-size:1.15rem;
    font-weight:700;
    color:#f8fafc;
}

.hero-title {
    font-family:'Space Grotesk';
    font-size:3rem;
    line-height:1.05;
    font-weight:700;
    color:#f8fafc;
    margin:0;
}

.hero-sub {
    color:#94a3b8;
    font-size:1.05rem;
    margin-top:10px;
    max-width:760px;
}

.section-title {
    font-family:'Space Grotesk';
    font-size:1.35rem;
    font-weight:700;
    color:#f8fafc;
    margin-top:12px;
}

.kpi {
    background:linear-gradient(145deg,#111827,#0d111a);
    border:1px solid rgba(148,163,184,.12);
    border-radius:20px;
    padding:20px;
    min-height:125px;
    box-shadow:0 12px 30px rgba(0,0,0,.12);
}

.kpi-label {
    color:#94a3b8;
    font-size:.85rem;
    font-weight:600;
}

.kpi-value {
    color:#f8fafc;
    font-family:'Space Grotesk';
    font-size:1.8rem;
    font-weight:700;
    margin-top:8px;
}

.kpi-note {
    color:#64748b;
    font-size:.75rem;
    margin-top:6px;
}

.insight {
    border:1px solid rgba(139,92,246,.22);
    background:linear-gradient(145deg,rgba(139,92,246,.10),rgba(6,182,212,.05));
    border-radius:18px;
    padding:18px 20px;
}

div[data-testid="stFileUploader"] {
    border:1px dashed rgba(139,92,246,.45);
    border-radius:18px;
    padding:8px;
    background:rgba(139,92,246,.04);
}

[data-testid="stSidebar"] {
    background:#0b0f17;
    border-right:1px solid rgba(148,163,184,.10);
}

button[kind="primary"] {
    border-radius:12px;
}

hr {
    border-color:rgba(148,163,184,.10);
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="brand">
    <div class="brand-mark">SV</div>
    <div class="brand-name">SHREYA VERMA · DATA PROJECTS</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">Smart Expense Tracker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">A polished financial analytics workspace for understanding where your money goes, how your budget performs, and what your spending trend may look like next.</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# SIDEBAR — DATASET SUBMISSION
# ============================================================

with st.sidebar:
    st.markdown("##  Dataset")
    uploaded = st.file_uploader(
        "Submit expense CSV",
        type=["csv"],
        help="Required: Date, Description, Amount. Category is optional.",
    )

    st.markdown("---")
    st.markdown("### Analysis Settings")

    income = st.number_input(
        "Monthly income (₹)",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
    )

    budget_mode = st.selectbox(
        "Budget profile",
        ["Balanced", "Custom"],
        index=0,
    )

    st.markdown("---")
    st.caption("Built with Python · Pandas · Plotly · Streamlit")
    st.caption("Build by : SHREYA VERMA")

# IMPORTANT: upload-first behavior
if uploaded is None:
    st.markdown("""
    <div class="insight">
    <b> Welcome.</b><br><br>
    Upload your expense CSV from the sidebar to unlock the analytics workspace.
    <br><br>
    <b>Required columns:</b> Date, Description, Amount<br>
    <b>Optional:</b> Category
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### What you'll get")
    a,b,c = st.columns(3)
    a.info(" **Spending Intelligence**\n\nMonthly, daily and category-level analysis.")
    b.info(" **Budget Control**\n\nActual vs budget with over-spending alerts.")
    c.info(" **Trend Forecast**\n\nSimple next-month expense estimate.")
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================

try:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    df = prepare_data(load_dataset(tmp_path))
except Exception as exc:
    st.error(f"Unable to process this dataset: {exc}")
    st.stop()

if budget_mode == "Balanced":
    budgets = DEFAULT_BUDGETS.copy()
else:
    st.sidebar.markdown("### Custom category budgets")
    budgets = {}
    for category, default in DEFAULT_BUDGETS.items():
        budgets[category] = st.sidebar.number_input(
            category,
            min_value=0.0,
            value=float(default),
            step=500.0,
            key=f"custom_{category}",
        )

total = float(df["Amount"].sum())
savings = float(income - total)
savings_rate = float(savings / income * 100) if income else 0.0
average = float(df["Amount"].mean())
largest = float(df["Amount"].max())

monthly = monthly_summary(df)
categories = category_summary(df)
daily = daily_summary(df)
budget_df = budget_analysis(df, budgets)
prediction = predict_next_month(df)

# ============================================================
# DATASET HEALTH
# ============================================================

st.markdown(
    f"**{uploaded.name}** · {len(df):,} valid transactions · "
    f"{df['Date'].min().strftime('%d %b %Y')} → {df['Date'].max().strftime('%d %b %Y')}"
)

# ============================================================
# KPI CARDS
# ============================================================

cols = st.columns(5)

kpis = [
    (" Total Spent", f"₹{total:,.0f}", "Across submitted data"),
    (" Savings", f"₹{savings:,.0f}", "Income minus expenses"),
    ("Savings Rate", f"{savings_rate:.1f}%", "Based on entered income"),
    (" Transactions", f"{len(df):,}", "Valid expense records"),
    (" Average", f"₹{average:,.0f}", "Average transaction"),
]

for col, (label, value, note) in zip(cols, kpis):
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("")

# ============================================================
# INSIGHT ENGINE
# ============================================================

top_category = categories.iloc[0]["Category"] if not categories.empty else "—"
top_category_amount = categories.iloc[0]["Amount"] if not categories.empty else 0
over = budget_df[budget_df["Status"] == "Over Budget"]

if savings < 0:
    insight_text = f" Your expenses exceed the entered income by ₹{abs(savings):,.0f}. Consider reviewing your highest-spend categories."
elif len(over):
    insight_text = f" You are saving ₹{savings:,.0f}, but {len(over)} budget category(s) are over their configured limits."
else:
    insight_text = f" Your current profile is within budget, with ₹{savings:,.0f} remaining after expenses."

st.markdown(
    f'<div class="insight"><b>Smart insight</b><br>{insight_text}'
    f'<br><span style="color:#94a3b8">Highest spending category: '
    f'<b>{top_category}</b> · ₹{top_category_amount:,.0f}</span></div>',
    unsafe_allow_html=True
)

# ============================================================
# TABS
# ============================================================

tab_overview, tab_budget, tab_transactions, tab_reports = st.tabs(
    [" Overview", " Budget", " Transactions", " Reports"]
)

with tab_overview:
    st.markdown('<div class="section-title">Spending Overview</div>', unsafe_allow_html=True)

    left, right = st.columns([1.55, 1])

    with left:
        fig = px.area(
            monthly,
            x="Month",
            y="Total Expense",
            markers=True,
            title="Monthly Spending Trend",
        )
        fig.update_traces(line_width=3)
        fig.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=10,r=10,t=55,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.pie(
            categories,
            names="Category",
            values="Amount",
            hole=.58,
            title="Where Your Money Goes",
        )
        fig.update_layout(
            template="plotly_dark",
            height=400,
            margin=dict(l=10,r=10,t=55,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            categories.head(10),
            x="Amount",
            y="Category",
            orientation="h",
            title="Top Spending Categories",
        )
        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10,r=10,t=55,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.line(
            daily,
            x="Day",
            y="Daily Expense",
            markers=True,
            title="Daily Spending Activity",
        )
        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10,r=10,t=55,b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">📌 Quick Statistics</div>', unsafe_allow_html=True)
    q1,q2,q3 = st.columns(3)
    q1.metric("Largest Expense", f"₹{largest:,.0f}")
    q2.metric("Top Category", top_category)
    q3.metric("Budget Alerts", f"{len(over)} categories")

    # Prediction
    st.markdown('<div class="section-title">🔮 Expense Forecast</div>', unsafe_allow_html=True)
    if prediction is None:
        st.info("At least 3 months of expense history are needed for the trend estimate.")
    else:
        recent_avg = monthly["Total Expense"].tail(3).mean()
        p1,p2 = st.columns(2)
        p1.metric("Estimated Next Month", f"₹{prediction:,.0f}")
        p2.metric("Recent 3-Month Average", f"₹{recent_avg:,.0f}")
        st.caption("Uses a simple linear trend over the latest three months. Educational estimate only.")

with tab_budget:
    st.markdown('<div class="section-title"> Budget Control Center</div>', unsafe_allow_html=True)

    budget_total = budget_df["Budget"].sum()
    actual_total = budget_df["Actual"].sum()
    utilization = actual_total / budget_total * 100 if budget_total else 0

    a,b,c = st.columns(3)
    a.metric("Configured Budget", f"₹{budget_total:,.0f}")
    b.metric("Actual Spending", f"₹{actual_total:,.0f}")
    c.metric("Budget Utilization", f"{utilization:.1f}%")

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Budget", x=budget_df["Category"], y=budget_df["Budget"]))
    fig.add_trace(go.Bar(name="Actual", x=budget_df["Category"], y=budget_df["Actual"]))
    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        title="Budget vs Actual",
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-35,
    )
    st.plotly_chart(fig, use_container_width=True)

    if len(over):
        st.warning(" Over-budget categories: " + ", ".join(over["Category"].tolist()))
    else:
        st.success(" All configured categories are within budget.")

    display_budget = budget_df.copy()
    display_budget["Budget"] = display_budget["Budget"].map(lambda x: f"₹{x:,.0f}")
    display_budget["Actual"] = display_budget["Actual"].map(lambda x: f"₹{x:,.0f}")
    display_budget["Variance"] = display_budget["Variance"].map(lambda x: f"₹{x:,.0f}")
    display_budget["Used %"] = display_budget["Used %"].map(lambda x: f"{x:.1f}%")
    st.dataframe(display_budget, use_container_width=True, hide_index=True)

with tab_transactions:
    st.markdown('<div class="section-title">🔎 Transaction Explorer</div>', unsafe_allow_html=True)

    s1,s2,s3 = st.columns([1.4,1,1])
    with s1:
        search = st.text_input("Search description", placeholder="e.g. Uber, Amazon, rent...")
    with s2:
        selected_categories = st.multiselect(
            "Categories",
            sorted(df["Category"].unique()),
        )
    with s3:
        min_amount = st.number_input("Minimum amount (₹)", min_value=0.0, value=0.0, step=100.0)

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Description"].str.contains(search, case=False, na=False)]
    if selected_categories:
        filtered = filtered[filtered["Category"].isin(selected_categories)]
    filtered = filtered[filtered["Amount"] >= min_amount]

    st.caption(f"Showing {len(filtered):,} matching transactions")

    st.dataframe(
        filtered[["Date","Description","Category","Amount"]]
        .sort_values("Date", ascending=False)
        .style.format({"Amount":"₹{:,.2f}"}),
        use_container_width=True,
        hide_index=True,
    )

with tab_reports:
    st.markdown('<div class="section-title"> Download Center</div>', unsafe_allow_html=True)

    report_data = {
        "Cleaned Transactions": df,
        "Monthly Summary": monthly,
        "Category Summary": categories,
        "Daily Summary": daily,
        "Budget Analysis": budget_df,
    }

    cols = st.columns(2)
    for i, (label, data) in enumerate(report_data.items()):
        csv = data.to_csv(index=False).encode("utf-8")
        cols[i % 2].download_button(
            f"⬇ {label}",
            csv,
            file_name=label.lower().replace(" ","_") + ".csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("###  Dataset Snapshot")
    st.dataframe(
        df[["Date","Description","Category","Amount"]].head(20),
        use_container_width=True,
        hide_index=True,
    )

st.divider()
st.caption("© 2026 Shreya Verma · Smart Expense Tracker · AI Developer")
