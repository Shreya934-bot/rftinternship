import streamlit as st
import pandas as pd
import plotly.express as px
import re
from io import StringIO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SocialPulse | Trend Intelligence",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* MAIN BACKGROUND */
    .stApp {
        background: #0B1020;
        color: #EAF0FF;
    }

    /* REMOVE TOP PADDING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #11182B;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #EAF0FF;
    }

    /* HERO */
    .hero {
        padding: 2.2rem 2.5rem;
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                rgba(124, 92, 255, 0.35),
                rgba(0, 210, 255, 0.18),
                rgba(255, 77, 166, 0.18)
            );
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 1.8rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #B7C2E3;
        margin-top: 0.5rem;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.12);
        font-size: 0.8rem;
    }

    /* SECTION TITLES */
    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* METRICS */
    div[data-testid="stMetric"] {
        background: #141D33;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9FAED2;
    }

    div[data-testid="stMetricValue"] {
        color: #F4F7FF;
        font-size: 1.7rem;
        font-weight: 700;
    }

    /* CARDS */
    .insight-card {
        background: #141D33;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1.2rem;
        border-radius: 18px;
        height: 100%;
    }

    .insight-label {
        color: #8FA0C9;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .insight-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.4rem;
        color: #FFFFFF;
    }

    /* FOOTER */
    .footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        color: #8E9BBC;
        font-size: 0.9rem;
    }

    /* BUTTON */
    .stDownloadButton > button {
        border-radius: 10px;
        border: none;
        font-weight: 600;
        padding: 0.55rem 1rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

POSITIVE_WORDS = [
    "love", "loved", "amazing", "fantastic",
    "great", "happy", "excited", "wonderful",
    "excellent", "inspiring", "achievement",
    "awesome", "brilliant", "best"
]

NEGATIVE_WORDS = [
    "disappointing", "frustrating", "poor",
    "problems", "not happy", "improvement",
    "issues", "bad", "worst", "hate",
    "terrible", "failed"
]


def analyze_sentiment(text):

    text = str(text).lower()

    positive_score = sum(
        word in text
        for word in POSITIVE_WORDS
    )

    negative_score = sum(
        word in text
        for word in NEGATIVE_WORDS
    )

    if positive_score > negative_score:
        return "Positive"

    elif negative_score > positive_score:
        return "Negative"

    return "Neutral"


# ============================================================
# DATA PROCESSING
# ============================================================

@st.cache_data
def process_data(file):

    df = pd.read_csv(file)

    # Remove duplicate posts
    if "Post_ID" in df.columns:
        df = df.drop_duplicates(subset="Post_ID")

    # Convert engagement columns
    for col in ["Likes", "Comments", "Shares"]:

        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    # Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # Time
    if "Time" in df.columns:
        df["Posting_Hour"] = pd.to_datetime(
            df["Time"],
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

    else:
        df["Posting_Hour"] = 0

    # Total Engagement
    df["Total_Engagement"] = (
        df["Likes"]
        + df["Comments"]
        + df["Shares"]
    )

    # Sentiment
    if "Content" in df.columns:

        df["Sentiment"] = df["Content"].apply(
            analyze_sentiment
        )

    else:
        df["Sentiment"] = "Neutral"

    return df


# ============================================================
# HASHTAG FUNCTION
# ============================================================

def get_hashtag_data(data):

    all_hashtags = []

    if "Hashtags" not in data.columns:
        return pd.DataFrame(
            columns=["Hashtag", "Count"]
        )

    for hashtags in data["Hashtags"].dropna():

        tags = re.findall(
            r"#\w+",
            str(hashtags)
        )

        all_hashtags.extend(
            [tag.lower() for tag in tags]
        )

    if not all_hashtags:

        return pd.DataFrame(
            columns=["Hashtag", "Count"]
        )

    hashtag_df = (
        pd.Series(all_hashtags)
        .value_counts()
        .reset_index()
    )

    hashtag_df.columns = [
        "Hashtag",
        "Count"
    ]

    return hashtag_df


# ============================================================
# SIDEBAR BRANDING
# ============================================================

with st.sidebar:

    st.markdown("""
    # 📱 SocialPulse

    ### Trend Intelligence

    ---
    """)

    st.caption(
        "Analyze conversations, discover trends "
        "and understand engagement."
    )

    st.markdown("### 📂 Data Source")

    uploaded_file = st.file_uploader(
        "Upload Social Media CSV",
        type=["csv"]
    )

    st.markdown("---")

    st.markdown(
        "### 🎛️ Intelligence Filters"
    )


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
📱 SocialPulse
</div>

<div class="hero-subtitle">
Social Media Trend Intelligence Dashboard
</div>

<div class="hero-badge">
Python • Analytics • NLP • Interactive Intelligence
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# NO FILE STATE
# ============================================================

if uploaded_file is None:

    st.markdown("""
    <div class="insight-card">

    <h2>Welcome to SocialPulse 👋</h2>

    Upload your social media dataset to unlock:

    <br><br>

    🔥 Trending Hashtag Intelligence<br>
    👥 Active User Analysis<br>
    💬 Engagement Analytics<br>
    🕒 Posting Time Insights<br>
    📈 Daily Engagement Trends<br>
    🥧 Content Category Distribution<br>
    😊 Sentiment Analysis<br>
    📥 Downloadable Analytics Reports

    </div>
    """, unsafe_allow_html=True)

    st.info(
        "👈 Upload social_media_posts.csv "
        "from the sidebar to begin."
    )

    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

df = process_data(uploaded_file)

if df.empty:

    st.error("The uploaded dataset is empty.")

    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:

    # Users
    users = sorted(
        df["User"]
        .dropna()
        .unique()
    ) if "User" in df.columns else []

    selected_users = st.multiselect(
        "👤 Users",
        options=users,
        default=users
    )

    # Categories
    categories = sorted(
        df["Category"]
        .dropna()
        .unique()
    ) if "Category" in df.columns else []

    selected_categories = st.multiselect(
        "🏷️ Categories",
        options=categories,
        default=categories
    )

    # Sentiment
    sentiments = [
        "Positive",
        "Neutral",
        "Negative"
    ]

    selected_sentiments = st.multiselect(
        "😊 Sentiment",
        options=sentiments,
        default=sentiments
    )

    # Date range
    if df["Date"].notna().any():

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()

        date_range = st.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    else:

        date_range = None

    st.markdown("---")

    st.markdown(
        "### 👩‍💻 Built by Shreya Verma"
    )

    st.caption(
        "AI • Machine Learning • Data Analytics"
    )

    st.markdown(
        "Day 27 • Python Internship Journey"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_users:

    filtered_df = filtered_df[
        filtered_df["User"].isin(
            selected_users
        )
    ]

if selected_categories:

    filtered_df = filtered_df[
        filtered_df["Category"].isin(
            selected_categories
        )
    ]

if selected_sentiments:

    filtered_df = filtered_df[
        filtered_df["Sentiment"].isin(
            selected_sentiments
        )
    ]

if date_range and len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered_df = filtered_df[
        (
            filtered_df["Date"]
            >= start_date
        )
        &
        (
            filtered_df["Date"]
            <= end_date
        )
    ]


if filtered_df.empty:

    st.warning(
        "No posts match the selected filters."
    )

    st.stop()


# ============================================================
# SEARCH
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 Explore the Conversation'
    '</div>',
    unsafe_allow_html=True
)

search_query = st.text_input(
    "Search by keyword, user or hashtag",
    placeholder="Try AI, Python, @username or #MachineLearning..."
)

if search_query:

    search_columns = [
        col for col in [
            "Content",
            "User",
            "Hashtags",
            "Category"
        ]
        if col in filtered_df.columns
    ]

    mask = pd.Series(
        False,
        index=filtered_df.index
    )

    for col in search_columns:

        mask |= (
            filtered_df[col]
            .astype(str)
            .str.contains(
                search_query,
                case=False,
                na=False
            )
        )

    filtered_df = filtered_df[mask]


if filtered_df.empty:

    st.warning(
        "No posts found for your search."
    )

    st.stop()


# ============================================================
# KPI METRICS
# ============================================================

total_posts = len(filtered_df)

total_engagement = (
    filtered_df["Total_Engagement"].sum()
)

average_engagement = (
    filtered_df["Total_Engagement"].mean()
)

top_hashtag_df = get_hashtag_data(
    filtered_df
)

top_hashtag = (
    top_hashtag_df.iloc[0]["Hashtag"]
    if not top_hashtag_df.empty
    else "N/A"
)

most_active_user = (
    filtered_df["User"]
    .value_counts()
    .index[0]
)

most_popular_hour = (
    filtered_df["Posting_Hour"]
    .value_counts()
    .index[0]
)


st.markdown(
    '<div class="section-title">'
    '⚡ Intelligence Snapshot'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "Total Posts",
    f"{total_posts:,}"
)

m2.metric(
    "Total Engagement",
    f"{total_engagement:,.0f}"
)

m3.metric(
    "Avg. Engagement",
    f"{average_engagement:,.0f}"
)

m4.metric(
    "🔥 Top Trend",
    top_hashtag
)

m5.metric(
    "👤 Most Active",
    most_active_user
)


# ============================================================
# QUICK INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Insights'
    '</div>',
    unsafe_allow_html=True
)

popular_time = (
    f"{int(most_popular_hour):02d}:00 – "
    f"{(int(most_popular_hour) + 1) % 24:02d}:00"
)

positive_pct = (
    (
        filtered_df["Sentiment"]
        .eq("Positive")
        .mean()
    )
    * 100
)


c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-label">
    🕒 Peak Posting Window
    </div>

    <div class="insight-value">
    {popular_time}
    </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-label">
    😊 Positive Conversation
    </div>

    <div class="insight-value">
    {positive_pct:.1f}%
    </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    top_category = (
        filtered_df["Category"]
        .value_counts()
        .index[0]
    )

    st.markdown(f"""
    <div class="insight-card">

    <div class="insight-label">
    🏷️ Leading Category
    </div>

    <div class="insight-value">
    {top_category}
    </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHART THEME
# ============================================================

CHART_TEMPLATE = "plotly_dark"


# ============================================================
# TOP HASHTAGS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔥 Trending Hashtag Intelligence'
    '</div>',
    unsafe_allow_html=True
)

top_10_hashtags = (
    get_hashtag_data(
        filtered_df
    )
    .head(10)
)

fig_hashtags = px.bar(
    top_10_hashtags,
    x="Count",
    y="Hashtag",
    orientation="h",
    text="Count",
    title="Top 10 Trending Hashtags",
    template=CHART_TEMPLATE
)

fig_hashtags.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    height=450,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    fig_hashtags,
    use_container_width=True
)


# ============================================================
# DAILY ENGAGEMENT + CATEGORY
# ============================================================

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">'
        '📈 Daily Engagement Trend'
        '</div>',
        unsafe_allow_html=True
    )

    daily_engagement = (
        filtered_df
        .groupby("Date")
        ["Total_Engagement"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    fig_daily = px.line(
        daily_engagement,
        x="Date",
        y="Total_Engagement",
        markers=True,
        template=CHART_TEMPLATE
    )

    fig_daily.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )


with right:

    st.markdown(
        '<div class="section-title">'
        '🥧 Content Category Mix'
        '</div>',
        unsafe_allow_html=True
    )

    category_data = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_data.columns = [
        "Category",
        "Posts"
    ]

    fig_category = px.pie(
        category_data,
        names="Category",
        values="Posts",
        hole=0.55,
        template=CHART_TEMPLATE
    )

    fig_category.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ============================================================
# USERS + POSTING TIME
# ============================================================

left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">'
        '👥 Most Active Users'
        '</div>',
        unsafe_allow_html=True
    )

    active_users = (
        filtered_df["User"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    active_users.columns = [
        "User",
        "Posts"
    ]

    fig_users = px.bar(
        active_users,
        x="Posts",
        y="User",
        orientation="h",
        text="Posts",
        template=CHART_TEMPLATE
    )

    fig_users.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_users,
        use_container_width=True
    )


with right:

    st.markdown(
        '<div class="section-title">'
        '🕒 Posting Time Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    hourly_data = (
        filtered_df["Posting_Hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    hourly_data.columns = [
        "Hour",
        "Posts"
    ]

    fig_time = px.bar(
        hourly_data,
        x="Hour",
        y="Posts",
        template=CHART_TEMPLATE
    )

    fig_time.update_xaxes(
        dtick=1
    )

    fig_time.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True
    )


# ============================================================
# ENGAGEMENT BREAKDOWN
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💬 Engagement Breakdown'
    '</div>',
    unsafe_allow_html=True
)

engagement_breakdown = pd.DataFrame({
    "Metric": [
        "Likes",
        "Comments",
        "Shares"
    ],
    "Count": [
        filtered_df["Likes"].sum(),
        filtered_df["Comments"].sum(),
        filtered_df["Shares"].sum()
    ]
})

fig_engagement = px.bar(
    engagement_breakdown,
    x="Metric",
    y="Count",
    text="Count",
    template=CHART_TEMPLATE
)

fig_engagement.update_layout(
    height=380
)

st.plotly_chart(
    fig_engagement,
    use_container_width=True
)


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '😊 Conversation Sentiment'
    '</div>',
    unsafe_allow_html=True
)

sentiment_data = (
    filtered_df["Sentiment"]
    .value_counts()
    .reindex(
        [
            "Positive",
            "Neutral",
            "Negative"
        ],
        fill_value=0
    )
    .reset_index()
)

sentiment_data.columns = [
    "Sentiment",
    "Posts"
]

fig_sentiment = px.bar(
    sentiment_data,
    x="Sentiment",
    y="Posts",
    text="Posts",
    template=CHART_TEMPLATE
)

fig_sentiment.update_layout(
    height=400
)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)


# ============================================================
# DETAILED POST EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📋 Social Conversation Explorer'
    '</div>',
    unsafe_allow_html=True
)

display_columns = [
    col for col in [
        "Post_ID",
        "Date",
        "Time",
        "User",
        "Content",
        "Hashtags",
        "Category",
        "Likes",
        "Comments",
        "Shares",
        "Total_Engagement",
        "Sentiment"
    ]
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[
        display_columns
    ].sort_values(
        "Total_Engagement",
        ascending=False
    ),
    use_container_width=True,
    height=450
)


# ============================================================
# ANALYTICS REPORT
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📥 Export Intelligence'
    '</div>',
    unsafe_allow_html=True
)

sentiment_counts = (
    filtered_df["Sentiment"]
    .value_counts()
)

top_category = (
    filtered_df["Category"]
    .value_counts()
    .index[0]
)

analytics_report = pd.DataFrame({
    "Metric": [
        "Total Posts",
        "Total Likes",
        "Total Comments",
        "Total Shares",
        "Total Engagement",
        "Average Engagement per Post",
        "Top Trending Hashtag",
        "Most Active User",
        "Most Popular Posting Time",
        "Top Content Category",
        "Positive Posts",
        "Neutral Posts",
        "Negative Posts"
    ],

    "Value": [
        len(filtered_df),
        filtered_df["Likes"].sum(),
        filtered_df["Comments"].sum(),
        filtered_df["Shares"].sum(),
        filtered_df["Total_Engagement"].sum(),
        round(
            filtered_df[
                "Total_Engagement"
            ].mean(),
            2
        ),
        top_hashtag,
        most_active_user,
        popular_time,
        top_category,
        sentiment_counts.get(
            "Positive",
            0
        ),
        sentiment_counts.get(
            "Neutral",
            0
        ),
        sentiment_counts.get(
            "Negative",
            0
        )
    ]
})


report_csv = analytics_report.to_csv(
    index=False
)

filtered_csv = filtered_df.to_csv(
    index=False
)


download_1, download_2 = st.columns(2)

with download_1:

    st.download_button(
        label="📊 Download Analytics Report",
        data=report_csv,
        file_name=(
            "social_media_analytics_report.csv"
        ),
        mime="text/csv",
        use_container_width=True
    )


with download_2:

    st.download_button(
        label="📥 Download Filtered Posts",
        data=filtered_csv,
        file_name=(
            "filtered_social_media_posts.csv"
        ),
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<b>SocialPulse — Social Media Trend Intelligence</b>

<br><br>

Built with ❤️ using Python, Pandas, NLP & Streamlit

<br>

© 2026 Shreya Verma • Day 27 Python Internship Journey

</div>
""", unsafe_allow_html=True)