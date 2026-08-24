from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Fraud Detection Intelligence",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# CUSTOM STYLING
# ==================================================
st.markdown(
    """
    <style>
        .stApp {
            background: #0e1117;
        }

        [data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #263244;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1450px;
        }

        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            letter-spacing: -0.03em;
        }

        .hero-subtitle {
            color: #aab7c8;
            font-size: 1.05rem;
            margin-bottom: 1.2rem;
        }

        .section-label {
            color: #9aa9bd;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.25rem;
        }

        .stMetric {
            background: linear-gradient(135deg, #162235 0%, #101827 100%);
            border: 1px solid #2a3a52;
            padding: 1rem;
            border-radius: 16px;
        }

        div[data-testid="stMetricLabel"] {
            color: #b8c5d6;
        }

        div[data-testid="stMetricValue"] {
            color: #f4f7fb;
        }

        .insight-card {
            background: #111827;
            border: 1px solid #27364c;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            min-height: 130px;
        }

        .insight-card h4 {
            margin: 0 0 0.5rem 0;
        }

        .insight-card p {
            color: #aebacc;
            margin: 0;
            line-height: 1.5;
        }

        .stDownloadButton > button,
        .stButton > button {
            border-radius: 9px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# CONSTANTS
# ==================================================
RISK_ORDER = ["Low", "Medium", "High"]
RISK_COLORS = {
    "Low": "#22c55e",
    "Medium": "#f59e0b",
    "High": "#ef4444",
}


# ==================================================
# LOAD AND PROCESS DATA
# ==================================================
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "transactions_dataset.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path.name}. "
            "Place transactions_dataset.csv beside this Streamlit file."
        )

    df = pd.read_csv(data_path)

    required_columns = [
        "Transaction_ID",
        "Transaction_Date",
        "Account_ID",
        "Transaction_Category",
        "Amount",
        "Payment_Method",
        "City",
        "Status",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing_columns)
        )

    # Basic cleaning
    df["Transaction_Date"] = pd.to_datetime(
        df["Transaction_Date"],
        errors="coerce",
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce",
    ).fillna(0)

    text_columns = [
        "Transaction_ID",
        "Account_ID",
        "Transaction_Category",
        "Payment_Method",
        "City",
        "Status",
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    # ------------------------------------------------
    # INVESTIGATION FLAGS
    # ------------------------------------------------
    # Detect exact duplicate records before removing them.
    df["Exact_Duplicate"] = df.duplicated(keep=False)

    # Detect transactions that repeat the same account,
    # amount and transaction date.
    df["Duplicate_Flag"] = df.duplicated(
        subset=["Account_ID", "Amount", "Transaction_Date"],
        keep=False,
    )

    # Frequent account activity.
    account_transaction_counts = df.groupby("Account_ID")[
        "Transaction_ID"
    ].transform("count")

    df["Transaction_Count_For_Account"] = account_transaction_counts
    df["Frequent_Account_Flag"] = account_transaction_counts >= 5

    # High-value flag.
    df["High_Value_Flag"] = df["Amount"] > 10000

    # Status flag.
    normalized_status = df["Status"].str.lower()
    df["Unsuccessful_Status_Flag"] = normalized_status.isin(
        ["failed", "pending"]
    )

    # ------------------------------------------------
    # RISK SCORING
    # ------------------------------------------------
    df["Risk_Score"] = 0

    df.loc[df["Amount"] > 10000, "Risk_Score"] += 40
    df.loc[
        df["Amount"].between(5000, 10000, inclusive="both"),
        "Risk_Score",
    ] += 20
    df.loc[df["Duplicate_Flag"], "Risk_Score"] += 30
    df.loc[df["Frequent_Account_Flag"], "Risk_Score"] += 30
    df.loc[df["Unsuccessful_Status_Flag"], "Risk_Score"] += 10

    df["Risk_Score"] = df["Risk_Score"].clip(0, 100)

    df["Risk_Level"] = pd.cut(
        df["Risk_Score"],
        bins=[-1, 20, 50, 100],
        labels=RISK_ORDER,
    )

    # Explain why a transaction is suspicious.
    def build_risk_reason(row):
        reasons = []

        if row["High_Value_Flag"]:
            reasons.append("High-value amount")

        if row["Duplicate_Flag"]:
            reasons.append("Duplicate transaction pattern")

        if row["Frequent_Account_Flag"]:
            reasons.append("Frequent account activity")

        if row["Unsuccessful_Status_Flag"]:
            reasons.append("Failed or pending status")

        return " • ".join(reasons) if reasons else "No major risk signal"

    df["Risk_Reasons"] = df.apply(build_risk_reason, axis=1)

    # Investigation priority.
    df["Suspicious_Flag"] = (
        (df["Risk_Level"].astype(str) == "High")
        | df["High_Value_Flag"]
        | df["Duplicate_Flag"]
    )

    return df


try:
    df = load_data()
except Exception as error:
    st.error("Unable to load the transaction dataset.")
    st.exception(error)
    st.stop()


# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.title("🔐 Investigation Controls")
st.sidebar.caption(
    "Filter the dataset and focus the dashboard on the transactions you want to investigate."
)

with st.sidebar.expander("📂 Core Filters", expanded=True):
    categories = sorted(df["Transaction_Category"].dropna().unique())
    selected_categories = st.multiselect(
        "Transaction Category",
        options=categories,
        default=categories,
    )

    cities = sorted(df["City"].dropna().unique())
    selected_cities = st.multiselect(
        "City",
        options=cities,
        default=cities,
    )

    payment_methods = sorted(df["Payment_Method"].dropna().unique())
    selected_payment_methods = st.multiselect(
        "Payment Method",
        options=payment_methods,
        default=payment_methods,
    )

    statuses = sorted(df["Status"].dropna().unique())
    selected_statuses = st.multiselect(
        "Transaction Status",
        options=statuses,
        default=statuses,
    )

with st.sidebar.expander("💰 Amount & Risk", expanded=True):
    amount_min = float(df["Amount"].min())
    amount_max = float(df["Amount"].max())

    amount_range = st.slider(
        "Transaction Amount",
        min_value=amount_min,
        max_value=amount_max,
        value=(amount_min, amount_max),
    )

    selected_risk_levels = st.multiselect(
        "Risk Level",
        options=RISK_ORDER,
        default=RISK_ORDER,
    )

    suspicious_only = st.checkbox(
        "Show suspicious transactions only",
        value=False,
    )

with st.sidebar.expander("📅 Date & Search", expanded=True):
    valid_dates = df["Transaction_Date"].dropna()

    selected_date_range = None

    if not valid_dates.empty:
        selected_date_range = st.date_input(
            "Transaction Date Range",
            value=(
                valid_dates.min().date(),
                valid_dates.max().date(),
            ),
            min_value=valid_dates.min().date(),
            max_value=valid_dates.max().date(),
        )

    search_text = st.text_input(
        "Search Transaction or Account ID",
        placeholder="Example: ACC1001 or TXN001",
    )

st.sidebar.divider()

if st.sidebar.button("🔄 Reset Dashboard Filters", use_container_width=True):
    st.rerun()


# ==================================================
# APPLY FILTERS
# ==================================================
filtered_df = df[
    df["Transaction_Category"].isin(selected_categories)
    & df["City"].isin(selected_cities)
    & df["Payment_Method"].isin(selected_payment_methods)
    & df["Status"].isin(selected_statuses)
    & df["Amount"].between(amount_range[0], amount_range[1])
    & df["Risk_Level"].astype(str).isin(selected_risk_levels)
].copy()

if selected_date_range and len(selected_date_range) == 2:
    start_date = pd.Timestamp(selected_date_range[0])
    end_date = pd.Timestamp(selected_date_range[1])

    filtered_df = filtered_df[
        filtered_df["Transaction_Date"].between(
            start_date,
            end_date + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1),
        )
    ]

if suspicious_only:
    filtered_df = filtered_df[filtered_df["Suspicious_Flag"]].copy()

if search_text:
    search_mask = (
        filtered_df["Account_ID"]
        .str.contains(search_text, case=False, na=False)
        | filtered_df["Transaction_ID"]
        .str.contains(search_text, case=False, na=False)
    )

    filtered_df = filtered_df[search_mask].copy()


# ==================================================
# HELPER FUNCTIONS
# ==================================================
def currency(value):
    return f"₹{value:,.0f}"


def style_figure(fig, height=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#d9e2ef"),
        margin=dict(l=20, r=20, t=55, b=20),
        height=height,
        legend_title_text="",
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.08)",
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.08)",
    )

    return fig


# ==================================================
# HEADER
# ==================================================
st.markdown(
    '<div class="hero-title">🔐 Fraud Detection Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    'Advanced transaction monitoring, anomaly detection, risk scoring and investigation insights.'
    '</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"Showing {len(filtered_df):,} of {len(df):,} transactions"
)

st.divider()


# ==================================================
# KPI METRICS
# ==================================================
total_transactions = len(filtered_df)
total_amount = filtered_df["Amount"].sum()
average_amount = filtered_df["Amount"].mean() if total_transactions else 0
high_value_transactions = int(filtered_df["High_Value_Flag"].sum())
high_risk_transactions = int(
    (filtered_df["Risk_Level"].astype(str) == "High").sum()
)
suspicious_transactions = int(filtered_df["Suspicious_Flag"].sum())

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

kpi1.metric("💳 Transactions", f"{total_transactions:,}")
kpi2.metric("💰 Total Value", currency(total_amount))
kpi3.metric("📊 Avg Amount", currency(average_amount))
kpi4.metric("🚨 High Value", f"{high_value_transactions:,}")
kpi5.metric("⚠️ High Risk", f"{high_risk_transactions:,}")
kpi6.metric("🔎 Suspicious", f"{suspicious_transactions:,}")

st.divider()


# ==================================================
# EMPTY STATE
# ==================================================
if filtered_df.empty:
    st.warning(
        "No transactions match the current filters. "
        "Adjust the investigation controls in the sidebar."
    )
    st.stop()


# ==================================================
# TABS
# ==================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Command Center",
        "🚨 Investigation",
        "👤 Account Intelligence",
        "📈 Trends & Patterns",
        "📥 Reports",
    ]
)


# ==================================================
# TAB 1 — COMMAND CENTER
# ==================================================
with tab1:
    st.subheader("📊 Transaction Command Center")

    left, right = st.columns(2)

    with left:
        category_data = (
            filtered_df["Transaction_Category"]
            .value_counts()
            .rename_axis("Transaction_Category")
            .reset_index(name="Transactions")
        )

        fig_category = px.bar(
            category_data,
            x="Transaction_Category",
            y="Transactions",
            text="Transactions",
            color="Transactions",
            title="Transaction Volume by Category",
            color_continuous_scale="Blues",
        )

        fig_category.update_traces(textposition="outside")
        fig_category.update_coloraxes(showscale=False)
        st.plotly_chart(
            style_figure(fig_category, 430),
            use_container_width=True,
        )

    with right:
        risk_data = (
            filtered_df["Risk_Level"]
            .astype(str)
            .value_counts()
            .reindex(RISK_ORDER, fill_value=0)
            .rename_axis("Risk_Level")
            .reset_index(name="Transactions")
        )

        fig_risk = px.pie(
            risk_data,
            names="Risk_Level",
            values="Transactions",
            hole=0.58,
            title="Risk Distribution",
            color="Risk_Level",
            color_discrete_map=RISK_COLORS,
        )

        st.plotly_chart(
            style_figure(fig_risk, 430),
            use_container_width=True,
        )

    st.subheader("💰 Top 10 Highest Transactions")

    top_10 = (
        filtered_df.nlargest(10, "Amount")
        .sort_values("Amount")
        .copy()
    )

    fig_top = px.bar(
        top_10,
        x="Amount",
        y="Transaction_ID",
        orientation="h",
        color="Risk_Level",
        color_discrete_map=RISK_COLORS,
        text="Amount",
        title="Largest Transactions in the Current Investigation",
        hover_data=[
            "Account_ID",
            "Transaction_Category",
            "City",
            "Payment_Method",
            "Status",
            "Risk_Score",
        ],
    )

    fig_top.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
    )

    st.plotly_chart(
        style_figure(fig_top, 480),
        use_container_width=True,
    )

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    top_category = (
        filtered_df["Transaction_Category"].mode().iloc[0]
        if not filtered_df.empty
        else "N/A"
    )

    highest_city = (
        filtered_df["City"].mode().iloc[0]
        if not filtered_df.empty
        else "N/A"
    )

    riskiest_transaction = filtered_df.loc[
        filtered_df["Risk_Score"].idxmax()
    ]

    with insight_col1:
        st.markdown(
            f"""
            <div class="insight-card">
                <h4>📂 Most Active Category</h4>
                <p><b>{top_category}</b> currently has the highest transaction activity in the selected data.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_col2:
        st.markdown(
            f"""
            <div class="insight-card">
                <h4>🏙️ Activity Hotspot</h4>
                <p><b>{highest_city}</b> has the highest transaction volume under the current filters.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_col3:
        st.markdown(
            f"""
            <div class="insight-card">
                <h4>🎯 Highest Risk Signal</h4>
                <p><b>{riskiest_transaction["Transaction_ID"]}</b> has a risk score of <b>{riskiest_transaction["Risk_Score"]}</b>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==================================================
# TAB 2 — INVESTIGATION
# ==================================================
with tab2:
    st.subheader("🚨 Suspicious Transaction Investigation")

    suspicious_df = (
        filtered_df[filtered_df["Suspicious_Flag"]]
        .sort_values(["Risk_Score", "Amount"], ascending=[False, False])
        .copy()
    )

    inv1, inv2, inv3, inv4 = st.columns(4)
    inv1.metric("Suspicious", len(suspicious_df))
    inv2.metric(
        "Duplicate Patterns",
        int(suspicious_df["Duplicate_Flag"].sum()),
    )
    inv3.metric(
        "Frequent Accounts",
        int(suspicious_df["Frequent_Account_Flag"].sum()),
    )
    inv4.metric(
        "Failed/Pending",
        int(suspicious_df["Unsuccessful_Status_Flag"].sum()),
    )

    st.markdown("### Investigation Queue")

    display_columns = [
        "Transaction_ID",
        "Transaction_Date",
        "Account_ID",
        "Transaction_Category",
        "Amount",
        "Payment_Method",
        "City",
        "Status",
        "Risk_Score",
        "Risk_Level",
        "Risk_Reasons",
    ]

    st.dataframe(
        suspicious_df[display_columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Amount": st.column_config.NumberColumn(
                "Amount",
                format="₹%d",
            ),
            "Risk_Score": st.column_config.ProgressColumn(
                "Risk Score",
                min_value=0,
                max_value=100,
                format="%d",
            ),
        },
    )

    st.markdown("### Risk Score Distribution")

    fig_risk_score = px.histogram(
        filtered_df,
        x="Risk_Score",
        nbins=11,
        color="Risk_Level",
        barmode="stack",
        color_discrete_map=RISK_COLORS,
        title="How Risk Scores Are Distributed",
    )

    st.plotly_chart(
        style_figure(fig_risk_score, 420),
        use_container_width=True,
    )


# ==================================================
# TAB 3 — ACCOUNT INTELLIGENCE
# ==================================================
with tab3:
    st.subheader("👤 Account Intelligence")

    account_summary = (
        filtered_df.groupby("Account_ID")
        .agg(
            Transaction_Count=("Transaction_ID", "count"),
            Total_Amount=("Amount", "sum"),
            Average_Amount=("Amount", "mean"),
            Max_Transaction=("Amount", "max"),
            Max_Risk_Score=("Risk_Score", "max"),
            Suspicious_Transactions=("Suspicious_Flag", "sum"),
        )
        .reset_index()
        .sort_values(
            ["Suspicious_Transactions", "Transaction_Count"],
            ascending=[False, False],
        )
    )

    acc_left, acc_right = st.columns([1.15, 0.85])

    with acc_left:
        st.markdown("### 🔥 Top Accounts by Activity")

        top_accounts = (
            account_summary.nlargest(10, "Transaction_Count")
            .sort_values("Transaction_Count")
        )

        fig_accounts = px.bar(
            top_accounts,
            x="Transaction_Count",
            y="Account_ID",
            orientation="h",
            color="Max_Risk_Score",
            color_continuous_scale="Reds",
            title="Top 10 Most Active Accounts",
            hover_data=[
                "Total_Amount",
                "Average_Amount",
                "Max_Transaction",
                "Suspicious_Transactions",
            ],
        )

        st.plotly_chart(
            style_figure(fig_accounts, 470),
            use_container_width=True,
        )

    with acc_right:
        st.markdown("### 🎯 Account Risk Ranking")

        top_risk_accounts = account_summary.nlargest(
            10,
            "Max_Risk_Score",
        ).copy()

        st.dataframe(
            top_risk_accounts[
                [
                    "Account_ID",
                    "Transaction_Count",
                    "Total_Amount",
                    "Max_Risk_Score",
                    "Suspicious_Transactions",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Total_Amount": st.column_config.NumberColumn(
                    "Total Amount",
                    format="₹%d",
                ),
                "Max_Risk_Score": st.column_config.ProgressColumn(
                    "Max Risk",
                    min_value=0,
                    max_value=100,
                    format="%d",
                ),
            },
        )

    st.markdown("### Full Account Summary")

    st.dataframe(
        account_summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total_Amount": st.column_config.NumberColumn(
                "Total Amount",
                format="₹%d",
            ),
            "Average_Amount": st.column_config.NumberColumn(
                "Average Amount",
                format="₹%d",
            ),
            "Max_Transaction": st.column_config.NumberColumn(
                "Maximum Transaction",
                format="₹%d",
            ),
            "Max_Risk_Score": st.column_config.ProgressColumn(
                "Max Risk Score",
                min_value=0,
                max_value=100,
                format="%d",
            ),
        },
    )


# ==================================================
# TAB 4 — TRENDS & PATTERNS
# ==================================================
with tab4:
    st.subheader("📈 Transaction Trends & Behavioral Patterns")

    trend_df = filtered_df.dropna(
        subset=["Transaction_Date"]
    ).copy()

    trend_df["Date"] = trend_df["Transaction_Date"].dt.date

    daily_data = (
        trend_df.groupby("Date")
        .agg(
            Transactions=("Transaction_ID", "count"),
            Total_Amount=("Amount", "sum"),
            Average_Risk=("Risk_Score", "mean"),
        )
        .reset_index()
        .sort_values("Date")
    )

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        fig_trend = px.line(
            daily_data,
            x="Date",
            y="Transactions",
            markers=True,
            title="Daily Transaction Volume",
        )

        st.plotly_chart(
            style_figure(fig_trend, 420),
            use_container_width=True,
        )

    with trend_col2:
        fig_amount_trend = px.area(
            daily_data,
            x="Date",
            y="Total_Amount",
            title="Daily Transaction Value",
        )

        st.plotly_chart(
            style_figure(fig_amount_trend, 420),
            use_container_width=True,
        )

    pattern_col1, pattern_col2 = st.columns(2)

    with pattern_col1:
        city_data = (
            filtered_df["City"]
            .value_counts()
            .rename_axis("City")
            .reset_index(name="Transactions")
            .sort_values("Transactions")
        )

        fig_city = px.bar(
            city_data,
            x="Transactions",
            y="City",
            orientation="h",
            color="Transactions",
            color_continuous_scale="Teal",
            title="Transaction Activity by City",
        )

        fig_city.update_coloraxes(showscale=False)

        st.plotly_chart(
            style_figure(fig_city, 460),
            use_container_width=True,
        )

    with pattern_col2:
        payment_data = (
            filtered_df.groupby("Payment_Method")
            .agg(
                Transactions=("Transaction_ID", "count"),
                Total_Amount=("Amount", "sum"),
            )
            .reset_index()
        )

        fig_payment = px.scatter(
            payment_data,
            x="Transactions",
            y="Total_Amount",
            size="Transactions",
            color="Payment_Method",
            text="Payment_Method",
            title="Payment Method Activity & Value",
        )

        fig_payment.update_traces(textposition="top center")

        st.plotly_chart(
            style_figure(fig_payment, 460),
            use_container_width=True,
        )


# ==================================================
# TAB 5 — REPORTS
# ==================================================
with tab5:
    st.subheader("📥 Investigation Reports")

    st.write(
        "Export the current filtered dataset or a focused suspicious-transaction report."
    )

    report_col1, report_col2 = st.columns(2)

    filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")

    suspicious_report = (
        filtered_df[filtered_df["Suspicious_Flag"]]
        .sort_values(["Risk_Score", "Amount"], ascending=[False, False])
        .copy()
    )

    suspicious_csv = suspicious_report.to_csv(index=False).encode("utf-8")

    with report_col1:
        st.download_button(
            label="⬇️ Download Filtered Transactions",
            data=filtered_csv,
            file_name="filtered_transactions.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with report_col2:
        st.download_button(
            label="🚨 Download Investigation Report",
            data=suspicious_csv,
            file_name="suspicious_transactions.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()
    st.markdown("### Dataset Preview")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        hide_index=True,
    )


# ==================================================
# FOOTER
# ==================================================
st.divider()

st.caption(
    "Fraud Detection & Transaction Analysis System | "
    "Python • Pandas • Plotly • Streamlit"
)
