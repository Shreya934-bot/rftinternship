import re
from io import BytesIO
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SV | Invoice Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --bg: #0b0d10;
        --panel: #111419;
        --panel-soft: #15191f;
        --border: #252a31;
        --text: #f1f3f5;
        --muted: #8b939e;
        --subtle: #606975;
        --accent: #d7a86e;
        --accent-soft: rgba(215, 168, 110, 0.10);
        --danger: #df7777;
        --success: #78b69a;
    }

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1480px;
        padding: 34px 42px 55px 42px;
    }

    [data-testid="stSidebar"] {
        background: #0e1013;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 28px;
    }

    /* Remove Streamlit's default top decoration */
    [data-testid="stDecoration"] {
        display: none;
    }

    /* Brand */
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 46px;
    }

    .brand-mark {
        width: 40px;
        height: 40px;
        border: 1px solid #3a3f47;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #15181d;
        color: #f3f3f3;
        font-family: "Space Grotesk", sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: .5px;
    }

    .brand-name {
        color: #e8eaed;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.2px;
    }

    /* Hero */
    .eyebrow {
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 2.2px;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .hero-title {
        margin: 0;
        font-family: "Space Grotesk", sans-serif;
        font-size: clamp(2.2rem, 4vw, 3.6rem);
        line-height: 1.02;
        font-weight: 600;
        letter-spacing: -1.8px;
        color: var(--text);
    }

    .hero-copy {
        margin-top: 12px;
        color: var(--muted);
        max-width: 720px;
        line-height: 1.65;
        font-size: 15px;
    }

    .hero-meta {
        margin-top: 18px;
        color: var(--subtle);
        font-size: 12px;
    }

    /* KPI strip */
    .metric {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 13px;
        padding: 17px 18px;
        min-height: 106px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        font-weight: 700;
    }

    .metric-value {
        margin-top: 9px;
        color: var(--text);
        font-family: "Space Grotesk", sans-serif;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: -.5px;
    }

    .metric-note {
        color: var(--subtle);
        margin-top: 5px;
        font-size: 11px;
    }

    /* Section headings */
    .section-kicker {
        color: var(--subtle);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.7px;
        margin: 30px 0 7px;
    }

    .section-title {
        color: var(--text);
        font-family: "Space Grotesk", sans-serif;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* Insight */
    .insight {
        background: var(--panel);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 11px;
        padding: 15px 17px;
        margin: 22px 0 26px;
        color: #c5cad1;
        font-size: 13px;
        line-height: 1.6;
    }

    .insight strong {
        color: var(--text);
    }

    .empty-state {
        border: 1px dashed #343a43;
        border-radius: 14px;
        padding: 46px 30px;
        text-align: center;
        background: #101318;
    }

    .empty-title {
        color: var(--text);
        font-family: "Space Grotesk", sans-serif;
        font-size: 21px;
        font-weight: 600;
    }

    .empty-copy {
        color: var(--muted);
        margin: 8px auto 0;
        max-width: 570px;
        line-height: 1.6;
        font-size: 13px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        border-bottom: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        color: var(--muted);
        font-weight: 600;
        font-size: 13px;
        padding: 0 16px;
    }

    .stTabs [aria-selected="true"] {
        color: var(--text);
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background: #111419 !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 9px !important;
    }

    [data-testid="stFileUploader"] {
        border: 1px dashed #3a4048;
        border-radius: 11px;
        background: #111419;
        padding: 10px;
    }

    /* Buttons */
    .stDownloadButton button,
    .stButton button {
        border-radius: 9px;
        border: 1px solid #343a42;
        background: #161a20;
        color: #e7e9ec;
        font-weight: 600;
    }

    .stDownloadButton button:hover,
    .stButton button:hover {
        border-color: #5a6069;
        color: #fff;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 11px;
        overflow: hidden;
    }

    /* Alerts */
    .stAlert {
        border-radius: 10px;
    }

    /* Sidebar labels */
    .sidebar-label {
        color: var(--subtle);
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-size: 10px;
        font-weight: 700;
        margin: 16px 0 8px;
    }

    .sidebar-note {
        color: var(--subtle);
        font-size: 11px;
        line-height: 1.55;
    }

    /* Hide unnecessary Streamlit chrome */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

def parse_amount(value):
    if pd.isna(value):
        return 0.0

    text = str(value).replace(",", "")
    text = re.sub(r"[^\d.\-]", "", text)

    try:
        return float(text)
    except ValueError:
        return 0.0

def parse_date(value):
    if value is None or pd.isna(value):
        return pd.NaT

    if str(value).strip() == "":
        return pd.NaT

    return pd.to_datetime(
        value,
        errors="coerce",
        dayfirst=True,
    )

def money(value):
    return f"₹{float(value):,.0f}"

def extract_field(text, patterns):
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        if match:
            return match.group(1).strip()

    return ""

def extract_pdf(file):
    if PdfReader is None:
        raise RuntimeError(
            "PDF support requires pypdf. Install it with: pip install pypdf"
        )

    reader = PdfReader(
        BytesIO(file.getvalue())
    )

    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    invoice_number = extract_field(
        text,
        [
            r"Invoice\s*(?:No|Number|#)\s*[:\-]?\s*([A-Z0-9\-/]+)",
            r"INV(?:OICE)?\s*[:#\-]?\s*([A-Z0-9\-/]+)",
        ],
    )

    customer = extract_field(
        text,
        [
            r"Customer\s*Name\s*[:\-]\s*(.+)",
            r"Bill\s*To\s*[:\-]\s*(.+)",
            r"Customer\s*[:\-]\s*(.+)",
        ],
    )

    email_match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text,
        flags=re.IGNORECASE,
    )

    email = (
        email_match.group(0)
        if email_match
        else ""
    )

    invoice_date = parse_date(
        extract_field(
            text,
            [
                r"Invoice\s*Date\s*[:\-]?\s*([^\n]+)",
            ],
        )
    )

    due_date = parse_date(
        extract_field(
            text,
            [
                r"Due\s*Date\s*[:\-]?\s*([^\n]+)",
            ],
        )
    )

    items = []

    pattern = re.compile(
        r"^(.+?)\s*\|\s*"
        r"(\d+(?:\.\d+)?)\s*\|\s*"
        r"[₹$]?\s*([\d,]+(?:\.\d+)?)\s*\|\s*"
        r"[₹$]?\s*([\d,]+(?:\.\d+)?)$"
    )

    for raw_line in text.splitlines():
        match = pattern.match(raw_line.strip())

        if not match:
            continue

        if re.search(
            r"item|description",
            match.group(1),
            flags=re.IGNORECASE,
        ):
            continue

        items.append(match.groups())

    calculated_total = sum(
        parse_amount(item[3])
        for item in items
    )

    total_matches = re.findall(
        r"(?:Grand\s+)?Total\s*[:\-]?\s*[₹$]?\s*"
        r"([\d,]+(?:\.\d+)?)",
        text,
        flags=re.IGNORECASE,
    )

    invoice_total = (
        parse_amount(total_matches[-1])
        if total_matches
        else calculated_total
    )

    return {
        "Invoice Number": invoice_number,
        "Customer Name": customer,
        "Customer Email": email,
        "Invoice Date": invoice_date,
        "Due Date": due_date,
        "Items": "; ".join(
            item[0]
            for item in items
        ),
        "Item Count": len(items),
        "Calculated Total": calculated_total,
        "Invoice Total": invoice_total,
        "Source File": file.name,
        "Source Type": "PDF",
    }

def process_csv(file):
    raw = pd.read_csv(file)

    required = {
        "Invoice Number",
        "Customer Name",
        "Invoice Date",
    }

    missing = required - set(raw.columns)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    optional = [
        "Customer Email",
        "Due Date",
        "Item",
        "Quantity",
        "Unit Price",
        "Amount",
        "Tax",
    ]

    for column in optional:
        if column not in raw.columns:
            raw[column] = ""

    raw["Invoice Date"] = raw["Invoice Date"].map(
        parse_date
    )

    raw["Due Date"] = raw["Due Date"].map(
        parse_date
    )

    raw["Quantity"] = pd.to_numeric(
        raw["Quantity"],
        errors="coerce",
    ).fillna(1)

    for column in [
        "Unit Price",
        "Amount",
        "Tax",
    ]:
        raw[column] = raw[column].map(
            parse_amount
        )

    if raw["Amount"].eq(0).all():
        raw["Amount"] = (
            raw["Quantity"] * raw["Unit Price"]
            + raw["Tax"]
        )

    records = []

    for invoice_number, group in raw.groupby(
        "Invoice Number",
        sort=False,
    ):
        first = group.iloc[0]

        items = [
            str(item).strip()
            for item in group["Item"]
            if str(item).strip()
        ]

        total = float(
            group["Amount"].sum()
        )

        records.append(
            {
                "Invoice Number": invoice_number,
                "Customer Name": first["Customer Name"],
                "Customer Email": first["Customer Email"],
                "Invoice Date": first["Invoice Date"],
                "Due Date": first["Due Date"],
                "Items": "; ".join(items),
                "Item Count": len(items),
                "Calculated Total": total,
                "Invoice Total": total,
                "Source File": file.name,
                "Source Type": "CSV",
            }
        )

    return pd.DataFrame(records)

def add_status(data, as_of):
    result = data.copy()

    result["Due Date"] = pd.to_datetime(
        result["Due Date"],
        errors="coerce",
    )

    selected_date = pd.Timestamp(
        as_of
    ).normalize()

    result["Days Overdue"] = (
        selected_date - result["Due Date"]
    ).dt.days.fillna(0).clip(
        lower=0
    ).astype(int)

    result["Payment Status"] = np.where(
        result["Due Date"].notna()
        & (
            result["Due Date"]
            < selected_date
        ),
        "Overdue",
        "Current",
    )

    return result

def chart_layout(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans",
            color="#aeb5bf",
            size=12,
        ),
        title=dict(
            font=dict(
                family="Space Grotesk",
                size=16,
                color="#eef0f2",
            )
        ),
        hoverlabel=dict(
            bgcolor="#171b21",
            bordercolor="#343a42",
            font=dict(
                color="#f2f3f4"
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#252a31",
        zeroline=False,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#1d2229",
        linecolor="#252a31",
        zeroline=False,
    )

    return fig

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-mark">SV</div>
        <div class="brand-name">SHREYA VERMA / DATA PROJECTS</div>
    </div>

    <h1 class="hero-title">Invoice Intelligence</h1>

    <div class="hero-copy">
        A focused workspace for turning invoice files into structured
        financial records, payment-status insights, and export-ready reports.
    </div>

    <div class="hero-meta">
        CSV processing · PDF extraction · overdue monitoring · reporting
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-label">Data source</div>',
        unsafe_allow_html=True,
    )

    source_type = st.radio(
        "Input format",
        ["CSV", "PDF"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if source_type == "CSV":
        uploaded = st.file_uploader(
            "Upload invoice CSV",
            type=["csv"],
            label_visibility="collapsed",
        )
    else:
        uploaded = st.file_uploader(
            "Upload invoice PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

    st.markdown(
        '<div class="sidebar-label">Analysis date</div>',
        unsafe_allow_html=True,
    )

    as_of = st.date_input(
        "Check overdue as of",
        value=date.today(),
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Expected CSV fields</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-note">
        Required: Invoice Number, Customer Name, Invoice Date.<br><br>
        Optional: Customer Email, Due Date, Item, Quantity,
        Unit Price, Amount and Tax.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-note">
        Built with Python, Pandas, NumPy, Plotly,
        Streamlit and pypdf.<br><br>
        Shreya Verma · 2026
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# EMPTY STATE
# ============================================================

if not uploaded:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-title">Start with your invoice data</div>
            <div class="empty-copy">
                Upload a CSV containing invoice records or one or more
                text-based PDF invoices. The workspace will stay empty
                until a dataset is submitted, keeping the analysis tied
                to the data you actually provide.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-kicker">Workflow</div>'
        '<div class="section-title">From invoice files to usable insight</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">01 · Extract</div>
                <div class="metric-value">Structure</div>
                <div class="metric-note">
                    Capture invoice, customer, date, item and amount fields.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">02 · Review</div>
                <div class="metric-value">Monitor</div>
                <div class="metric-note">
                    Surface overdue invoices and payment exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            """
            <div class="metric">
                <div class="metric-label">03 · Export</div>
                <div class="metric-value">Report</div>
                <div class="metric-note">
                    Download consolidated records and summary reports.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()

# ============================================================
# PROCESS INPUT
# ============================================================

try:

    if source_type == "CSV":
        data = process_csv(uploaded)

    else:
        records = []

        for file in uploaded:
            try:
                records.append(
                    extract_pdf(file)
                )
            except Exception as error:
                st.warning(
                    f"Could not process {file.name}: {error}"
                )

        data = pd.DataFrame(records)

    if data.empty:
        st.error(
            "No invoice records could be extracted from the uploaded files."
        )
        st.stop()

    data = add_status(
        data,
        as_of,
    )

except Exception as error:
    st.error(
        f"Processing failed: {error}"
    )
    st.stop()

# ============================================================
# SUMMARY VALUES
# ============================================================

total_invoices = len(data)
total_value = data["Invoice Total"].sum()
average_value = data["Invoice Total"].mean()

overdue = data[
    data["Payment Status"] == "Overdue"
]

overdue_count = len(overdue)
overdue_value = overdue["Invoice Total"].sum()

customer_count = data[
    "Customer Name"
].nunique()

current_value = data.loc[
    data["Payment Status"] == "Current",
    "Invoice Total",
].sum()

# ============================================================
# KPI ROW
# ============================================================

metric_columns = st.columns(5)

metrics = [
    (
        "Invoices",
        f"{total_invoices:,}",
        "Processed records",
    ),
    (
        "Invoice value",
        money(total_value),
        "Total document value",
    ),
    (
        "Average",
        money(average_value),
        "Average invoice",
    ),
    (
        "Overdue",
        f"{overdue_count:,}",
        money(overdue_value) + " exposed",
    ),
    (
        "Customers",
        f"{customer_count:,}",
        "Unique customers",
    ),
]

for column, (label, value, note) in zip(
    metric_columns,
    metrics,
):
    with column:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# CONTEXTUAL INSIGHT
# ============================================================

if overdue_count:
    insight_text = (
        f"<strong>{overdue_count} invoice(s)</strong> are overdue as of "
        f"<strong>{as_of.strftime('%d %b %Y')}</strong>, representing "
        f"<strong>{money(overdue_value)}</strong> in outstanding value."
    )
else:
    insight_text = (
        f"No invoices are overdue as of "
        f"<strong>{as_of.strftime('%d %b %Y')}</strong>."
    )

st.markdown(
    f'<div class="insight">{insight_text}</div>',
    unsafe_allow_html=True,
)

# ============================================================
# TABS
# ============================================================

overview_tab, overdue_tab, explorer_tab, reports_tab = st.tabs(
    [
        "Overview",
        "Overdue",
        "Explorer",
        "Reports",
    ]
)

# ============================================================
# OVERVIEW
# ============================================================

with overview_tab:

    st.markdown(
        '<div class="section-kicker">Portfolio view</div>'
        '<div class="section-title">Invoice performance at a glance</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    monthly = data.copy()

    monthly["Month"] = pd.to_datetime(
        monthly["Invoice Date"],
        errors="coerce",
    ).dt.to_period("M").astype(str)

    monthly = (
        monthly.groupby(
            "Month",
            as_index=False,
        )["Invoice Total"]
        .sum()
    )

    with left:

        fig = px.bar(
            monthly,
            x="Month",
            y="Invoice Total",
            title="Invoice value by month",
        )

        fig.update_traces(
            marker_color="#d7a86e",
            hovertemplate=(
                "%{x}<br>"
                "Value: ₹%{y:,.0f}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
        )

    customer_values = (
        data.groupby(
            "Customer Name",
            as_index=False,
        )["Invoice Total"]
        .sum()
        .sort_values(
            "Invoice Total",
            ascending=True,
        )
        .tail(8)
    )

    with right:

        fig = px.bar(
            customer_values,
            x="Invoice Total",
            y="Customer Name",
            orientation="h",
            title="Highest-value customers",
        )

        fig.update_traces(
            marker_color="#8e98a6",
            hovertemplate=(
                "%{y}<br>"
                "Value: ₹%{x:,.0f}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
        )

    left, right = st.columns(2)

    with left:

        status_data = (
            data["Payment Status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Invoices")
        )

        fig = px.pie(
            status_data,
            names="Status",
            values="Invoices",
            hole=0.66,
            title="Payment status mix",
        )

        fig.update_traces(
            marker=dict(
                colors=[
                    "#d7a86e",
                    "#5f6874",
                ]
            ),
            textinfo="percent",
            hovertemplate=(
                "%{label}: %{value} invoices"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
        )

    with right:

        timeline = data.copy()

        timeline["Invoice Date"] = pd.to_datetime(
            timeline["Invoice Date"],
            errors="coerce",
        )

        timeline = (
            timeline.groupby(
                "Invoice Date",
                as_index=False,
            )["Invoice Total"]
            .sum()
            .sort_values("Invoice Date")
        )

        fig = px.line(
            timeline,
            x="Invoice Date",
            y="Invoice Total",
            markers=True,
            title="Invoice value over time",
        )

        fig.update_traces(
            line=dict(
                color="#d7a86e",
                width=2,
            ),
            marker=dict(
                size=6,
                color="#d7a86e",
            ),
            hovertemplate=(
                "%{x|%d %b %Y}<br>"
                "Value: ₹%{y:,.0f}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-kicker">Financial exposure</div>'
        '<div class="section-title">Current versus overdue value</div>',
        unsafe_allow_html=True,
    )

    exposure = pd.DataFrame(
        {
            "Status": [
                "Current",
                "Overdue",
            ],
            "Value": [
                current_value,
                overdue_value,
            ],
        }
    )

    fig = go.Figure(
        go.Bar(
            x=exposure["Status"],
            y=exposure["Value"],
            marker_color=[
                "#6f9d88",
                "#b86e6e",
            ],
            hovertemplate=(
                "%{x}<br>"
                "Value: ₹%{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="Invoice value by payment status",
        showlegend=False,
    )

    st.plotly_chart(
        chart_layout(fig, 340),
        use_container_width=True,
    )

# ============================================================
# OVERDUE
# ============================================================

with overdue_tab:

    st.markdown(
        '<div class="section-kicker">Collections</div>'
        '<div class="section-title">Overdue invoice monitor</div>',
        unsafe_allow_html=True,
    )

    if overdue.empty:

        st.success(
            f"No overdue invoices as of {as_of.strftime('%d %b %Y')}."
        )

    else:

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Overdue invoices",
                f"{overdue_count:,}",
            )

        with b:
            st.metric(
                "Outstanding value",
                money(overdue_value),
            )

        with c:
            st.metric(
                "Average overdue",
                money(
                    overdue_value / overdue_count
                ),
            )

        overdue_display = overdue[
            [
                "Invoice Number",
                "Customer Name",
                "Invoice Date",
                "Due Date",
                "Invoice Total",
                "Days Overdue",
            ]
        ].copy()

        overdue_display["Invoice Total"] = (
            overdue_display["Invoice Total"]
            .map(money)
        )

        st.dataframe(
            overdue_display,
            use_container_width=True,
            hide_index=True,
        )

        overdue_chart = (
            overdue.groupby(
                "Customer Name",
                as_index=False,
            )["Invoice Total"]
            .sum()
            .sort_values(
                "Invoice Total",
                ascending=True,
            )
        )

        fig = px.bar(
            overdue_chart,
            x="Invoice Total",
            y="Customer Name",
            orientation="h",
            title="Overdue exposure by customer",
        )

        fig.update_traces(
            marker_color="#b86e6e",
            hovertemplate=(
                "%{y}<br>"
                "Overdue value: ₹%{x:,.0f}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True,
        )

# ============================================================
# EXPLORER
# ============================================================

with explorer_tab:

    st.markdown(
        '<div class="section-kicker">Records</div>'
        '<div class="section-title">Search and inspect invoices</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns([1.5, 1, 1])

    with f1:

        query = st.text_input(
            "Search",
            placeholder="Invoice number, customer or item",
        )

    with f2:

        selected_status = st.multiselect(
            "Payment status",
            sorted(
                data["Payment Status"]
                .dropna()
                .unique()
            ),
        )

    with f3:

        minimum_value = st.number_input(
            "Minimum invoice value",
            min_value=0.0,
            value=0.0,
            step=1000.0,
        )

    filtered = data.copy()

    if query:

        searchable = (
            filtered[
                [
                    "Invoice Number",
                    "Customer Name",
                    "Customer Email",
                    "Items",
                ]
            ]
            .fillna("")
            .astype(str)
        )

        mask = searchable.apply(
            lambda column: column.str.contains(
                query,
                case=False,
                na=False,
            )
        ).any(axis=1)

        filtered = filtered[mask]

    if selected_status:

        filtered = filtered[
            filtered["Payment Status"].isin(
                selected_status
            )
        ]

    filtered = filtered[
        filtered["Invoice Total"]
        >= minimum_value
    ]

    st.caption(
        f"Showing {len(filtered):,} of "
        f"{len(data):,} invoice(s)"
    )

    display_columns = [
        "Invoice Number",
        "Customer Name",
        "Invoice Date",
        "Due Date",
        "Items",
        "Invoice Total",
        "Payment Status",
        "Days Overdue",
        "Source Type",
    ]

    display_data = filtered[
        display_columns
    ].copy()

    display_data["Invoice Total"] = (
        display_data["Invoice Total"]
        .map(money)
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# REPORTS
# ============================================================

with reports_tab:

    st.markdown(
        '<div class="section-kicker">Export</div>'
        '<div class="section-title">Report center</div>',
        unsafe_allow_html=True,
    )

    summary = pd.DataFrame(
        [
            {
                "Total Invoices": total_invoices,
                "Total Amount": total_value,
                "Average Invoice": average_value,
                "Overdue Invoices": overdue_count,
                "Overdue Amount": overdue_value,
                "Unique Customers": customer_count,
            }
        ]
    )

    report_columns = st.columns(4)

    report_items = [
        (
            "Consolidated report",
            data,
            "consolidated_invoice_report.csv",
            "All processed invoice records.",
        ),
        (
            "Overdue report",
            overdue,
            "overdue_invoices.csv",
            "Invoices requiring follow-up.",
        ),
        (
            "Summary report",
            summary,
            "invoice_summary_report.csv",
            "High-level financial metrics.",
        ),
        (
            "Processed dataset",
            data,
            "processed_invoices.csv",
            "Full processed dataset.",
        ),
    ]

    for column, (
        title,
        frame,
        filename,
        description,
    ) in zip(
        report_columns,
        report_items,
    ):

        with column:

            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-label">{title}</div>
                    <div class="metric-note">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.download_button(
                "Download CSV",
                frame.to_csv(
                    index=False
                ).encode("utf-8"),
                filename,
                "text/csv",
                use_container_width=True,
            )

    st.markdown(
        '<div class="section-kicker">Processed data</div>'
        '<div class="section-title">Consolidated invoice records</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        display:flex;
        justify-content:space-between;
        color:#606975;
        font-size:11px;
        padding-top:4px;
    ">
        <span>Shreya Verma · Data Projects</span>
        <span>Invoice Intelligence</span>
    </div>
    """,
    unsafe_allow_html=True,
)
