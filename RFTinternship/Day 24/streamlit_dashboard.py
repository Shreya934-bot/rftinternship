import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ==================================================
# DAY 24 - WEATHER DATA ANALYTICS DASHBOARD
# ==================================================

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Data Analytics Dashboard")
st.write(
    "Interactive analysis of weather patterns, temperatures, "
    "and city-wise trends."
)


# ==================================================
# LOAD AND CLEAN DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("weather_data.csv")

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df["Temperature"] = df["Temperature"].fillna(
        df["Temperature"].median()
    )

    df["Humidity"] = df["Humidity"].fillna(
        df["Humidity"].median()
    )

    df["Weather"] = df["Weather"].fillna(
        df["Weather"].mode()[0]
    )

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("🔎 Filters")

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

selected_weather = st.sidebar.multiselect(
    "Select Weather Type",
    sorted(df["Weather"].unique()),
    default=sorted(df["Weather"].unique())
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df[
    (df["City"].isin(selected_cities))
    & (df["Weather"].isin(selected_weather))
]

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]


# ==================================================
# CHECK FOR EMPTY DATA
# ==================================================

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ==================================================
# CALCULATIONS
# ==================================================

city_average = (
    filtered_df.groupby("City")["Temperature"]
    .mean()
    .sort_values(ascending=False)
)

daily_temperature = (
    filtered_df.groupby("Date")["Temperature"]
    .mean()
)

hottest_city = city_average.idxmax()
coldest_city = city_average.idxmin()

rainy_count = (
    filtered_df["Weather"] == "Rainy"
).sum()

sunny_count = (
    filtered_df["Weather"] == "Sunny"
).sum()


# ==================================================
# KEY METRICS
# ==================================================

st.subheader("📊 Weather Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Weather Records",
    len(filtered_df)
)

col2.metric(
    "Average Temperature",
    f"{filtered_df['Temperature'].mean():.2f} °C"
)

col3.metric(
    "🔥 Hottest City",
    hottest_city
)

col4.metric(
    "❄️ Coldest City",
    coldest_city
)


col5, col6, col7 = st.columns(3)

col5.metric(
    "🌧️ Rainy Records",
    rainy_count
)

col6.metric(
    "☀️ Sunny Records",
    sunny_count
)

col7.metric(
    "🏙️ Cities Analyzed",
    filtered_df["City"].nunique()
)


st.divider()


# ==================================================
# TEMPERATURE TREND
# ==================================================

st.subheader("🌡️ Temperature Trend")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    daily_temperature.index,
    daily_temperature.values,
    marker="o"
)

ax.set_title("Average Temperature Trend Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Average Temperature (°C)")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


# ==================================================
# WEATHER DISTRIBUTION
# ==================================================

st.subheader("🌧️ Weather Distribution")

weather_counts = filtered_df["Weather"].value_counts()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        weather_counts.values,
        labels=weather_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Weather Distribution")

    st.pyplot(fig)


with col2:
    st.write("### Weather Counts")
    st.dataframe(
        weather_counts.rename("Count"),
        use_container_width=True
    )


# ==================================================
# AVERAGE TEMPERATURE PER CITY
# ==================================================

st.subheader("📊 Average Temperature per City")

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    city_average.index,
    city_average.values
)

ax.set_title("Average Temperature per City")
ax.set_xlabel("City")
ax.set_ylabel("Average Temperature (°C)")

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig)


# ==================================================
# CITY-WISE ANALYSIS TABLE
# ==================================================

st.subheader("🏙️ City-wise Temperature Analysis")

city_summary = (
    filtered_df.groupby("City")
    .agg(
        Average_Temperature=("Temperature", "mean"),
        Maximum_Temperature=("Temperature", "max"),
        Minimum_Temperature=("Temperature", "min"),
        Average_Humidity=("Humidity", "mean")
    )
    .round(2)
    .sort_values(
        "Average_Temperature",
        ascending=False
    )
)

st.dataframe(
    city_summary,
    use_container_width=True
)


# ==================================================
# BONUS - MOVING AVERAGE PREDICTION
# ==================================================

st.subheader("🔮 Tomorrow's Temperature Prediction")

if len(daily_temperature) >= 7:

    prediction = daily_temperature.tail(7).mean()

    st.metric(
        "Predicted Tomorrow's Average Temperature",
        f"{prediction:.2f} °C"
    )

    st.info(
        "Prediction is calculated using the average "
        "temperature of the most recent 7 days."
    )

else:
    st.warning(
        "Not enough date records for a 7-day moving "
        "average prediction."
    )


# ==================================================
# FILTERED DATA
# ==================================================

st.subheader("📋 Filtered Weather Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ==================================================
# DOWNLOAD FILTERED REPORT
# ==================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Weather Report",
    data=csv,
    file_name="filtered_weather_report.csv",
    mime="text/csv"
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🚀 Built as part of the RFT Python Internship "
    "Day 24 – Weather Data Analytics System"
)