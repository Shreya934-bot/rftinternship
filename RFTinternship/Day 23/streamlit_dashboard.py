# Day 23 - Bonus Challenge
# Interactive Employee Performance Dashboard using Streamlit

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Employee Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Performance Analytics Dashboard")
st.write("Interactive dashboard for analyzing employee performance and attendance.")


@st.cache_data
def load_data():
    data = pd.read_csv("employees_performance_dataset.csv")

    data = data.drop_duplicates()
    data["Department"] = data["Department"].fillna(data["Department"].mode()[0])
    data["Performance_Score"] = data["Performance_Score"].fillna(
        data["Performance_Score"].median()
    )
    data["Attendance_Percentage"] = data["Attendance_Percentage"].fillna(
        data["Attendance_Percentage"].median()
    )
    data["Joining_Date"] = pd.to_datetime(data["Joining_Date"])

    return data


df = load_data()


# Sidebar Filters
st.sidebar.header("🔎 Filters")

selected_departments = st.sidebar.multiselect(
    "Select Department",
    options=sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

performance_range = st.sidebar.slider(
    "Performance Score Range",
    float(df["Performance_Score"].min()),
    float(df["Performance_Score"].max()),
    (
        float(df["Performance_Score"].min()),
        float(df["Performance_Score"].max())
    )
)

attendance_range = st.sidebar.slider(
    "Attendance Range",
    float(df["Attendance_Percentage"].min()),
    float(df["Attendance_Percentage"].max()),
    (
        float(df["Attendance_Percentage"].min()),
        float(df["Attendance_Percentage"].max())
    )
)


filtered_df = df[
    (df["Department"].isin(selected_departments))
    & (df["Performance_Score"].between(
        performance_range[0], performance_range[1]
    ))
    & (df["Attendance_Percentage"].between(
        attendance_range[0], attendance_range[1]
    ))
]


# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", len(filtered_df))
col2.metric(
    "Average Performance",
    f"{filtered_df['Performance_Score'].mean():.2f}"
)
col3.metric(
    "Average Attendance",
    f"{filtered_df['Attendance_Percentage'].mean():.2f}%"
)
col4.metric(
    "Low Attendance",
    len(filtered_df[filtered_df["Attendance_Percentage"] < 75])
)


st.divider()


# Department Performance
st.subheader("🏢 Department-wise Average Performance")

department_performance = (
    filtered_df.groupby("Department")["Performance_Score"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(department_performance.index, department_performance.values)
ax.set_title("Department-wise Average Performance")
ax.set_xlabel("Department")
ax.set_ylabel("Average Performance Score")
plt.xticks(rotation=30, ha="right")
st.pyplot(fig)


# Top 10 Performers
st.subheader("🏆 Top 10 Performers")

top_10 = (
    filtered_df.sort_values("Performance_Score", ascending=False)
    .head(10)
)

st.dataframe(
    top_10[
        ["Employee_ID", "Employee_Name", "Department",
         "Performance_Score", "Attendance_Percentage"]
    ],
    use_container_width=True
)


# Attendance Distribution
st.subheader("📈 Attendance Analysis")

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(filtered_df["Attendance_Percentage"], bins=10)
ax.set_title("Attendance Distribution")
ax.set_xlabel("Attendance Percentage")
ax.set_ylabel("Number of Employees")
st.pyplot(fig)


# Department Distribution
st.subheader("🥧 Department Distribution")

department_counts = filtered_df["Department"].value_counts()

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(
    department_counts.values,
    labels=department_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Employee Distribution by Department")
st.pyplot(fig)


# Low Attendance Employees
st.subheader("⚠️ Employees with Attendance Below 75%")

low_attendance = filtered_df[
    filtered_df["Attendance_Percentage"] < 75
]

if low_attendance.empty:
    st.success("No employees with attendance below 75% in the selected data.")
else:
    st.dataframe(
        low_attendance[
            ["Employee_ID", "Employee_Name", "Department",
             "Attendance_Percentage", "Performance_Score"]
        ],
        use_container_width=True
    )


# Download Filtered Report
st.subheader("📥 Download Report")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Employee Report",
    data=csv,
    file_name="filtered_employee_report.csv",
    mime="text/csv"
)
