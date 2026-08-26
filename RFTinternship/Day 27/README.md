# 📱 Day 27 -- Social Media Trend Analyzer

## 📌 Project Overview

This project was completed as part of my **RFT Python Internship at GOW
AI Academy**.

The **Social Media Trend Analyzer** is designed to analyze social media
post data and extract meaningful insights from user activity,
engagement, hashtags, posting behavior, content categories, and
sentiment.

The application reads social media post data from a **CSV file**,
identifies trending hashtags, analyzes the most active users,
calculates engagement metrics, detects popular posting times, performs
sentiment analysis, generates multiple visualizations, and exports an
analytics report as a CSV file.

The project also includes an advanced and interactive **Streamlit
dashboard** with search, filters, KPI metrics, charts, and downloadable
analytics results.

------------------------------------------------------------------------

## 🎯 Objectives

The main objectives of this project are:

-   Read social media post data from a CSV file
-   Analyze social media posts and user activity
-   Identify the top trending hashtags
-   Find the most active users
-   Calculate engagement using:
    -   Likes
    -   Comments
    -   Shares
-   Detect the most popular posting time
-   Analyze daily engagement trends
-   Analyze content category distribution
-   Perform sentiment analysis
-   Classify posts into:
    -   Positive
    -   Neutral
    -   Negative
-   Generate visual analytics charts
-   Export the analytics report to CSV
-   Build an interactive Streamlit dashboard
-   Add search and filtering functionality

------------------------------------------------------------------------

## 📂 Project Files

```text
Day 27/
│
├── social_media_trend_analyzer.ipynb
├── social_media_trend_analyzer.py
├── app.py
├── requirements.txt
│
├── social_media_posts.csv
├── social_media_analytics_report.csv
│
├── top_hashtags_chart.png
├── daily_engagement_trend.png
├── content_category_distribution.png
├── sentiment_distribution.png
│
└── README.md
````

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* Matplotlib
* Streamlit
* TextBlob

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## 📄 Dataset

The project uses a CSV dataset containing social media post information.

Each row represents a social media post and can contain information
such as:

* Post ID
* User Name
* Post Content
* Hashtags
* Likes
* Comments
* Shares
* Content Category
* Posting Date and Time

The dataset is analyzed to identify trends, engagement patterns, user
activity, and sentiment.

---

## 🧠 Social Media Analysis Process

The analysis workflow consists of the following steps:

### 1. Data Loading

The application reads social media post data from a CSV file using
Pandas.

The dataset is loaded into a DataFrame for cleaning, processing, and
analysis.

---

### 2. Data Preprocessing

The social media dataset is prepared for analysis.

This includes processing relevant fields such as:

* User information
* Post content
* Hashtags
* Likes
* Comments
* Shares
* Content categories
* Posting date and time

Date and time information is also processed to support posting-time
and daily engagement analysis.

---

### 3. Hashtag Analysis

The application extracts hashtags from social media posts and counts
their frequency.

This helps identify the most frequently used and trending hashtags.

The results are visualized using the:

```text
top_hashtags_chart.png
```

---

### 4. Active User Analysis

The project analyzes the number of posts created by each user.

Users are ranked based on their posting activity to identify the most
active users in the dataset.

---

### 5. Engagement Analysis

An engagement metric is calculated using social media interactions.

The analysis considers:

* Likes
* Comments
* Shares

The total engagement can be represented as:

```text
Engagement = Likes + Comments + Shares
```

This provides a simple measure of how much interaction each post
receives.

---

### 6. Daily Engagement Trend

The application groups engagement data by date to analyze how audience
interaction changes over time.

This helps identify:

* High-engagement days
* Low-engagement days
* Overall engagement patterns
* Changes in social media activity

The results are visualized using:

```text
daily_engagement_trend.png
```

---

### 7. Popular Posting Time Analysis

The posting timestamp is analyzed to determine when users are most
active.

The application identifies the most popular posting time based on the
frequency of posts.

This can help understand when social media activity is highest.

---

### 8. Content Category Analysis

Posts are grouped according to their content categories.

The application calculates the distribution of posts across different
categories and visualizes the results.

The generated chart is:

```text
content_category_distribution.png
```

This helps understand what types of content are most common in the
dataset.

---

## ⭐ Bonus Challenge -- Sentiment Analysis

The project includes sentiment analysis of social media post content.

Each post is analyzed and classified into one of the following
categories:

* Positive
* Neutral
* Negative

The sentiment classification helps analyze the overall tone of social
media content.

The results are visualized using:

```text
sentiment_distribution.png
```

---

## 📊 Generated Visualizations

The project generates four analytics charts:

### 1. 📊 Top Trending Hashtags

Displays the most frequently used hashtags in the social media
dataset.

```text
top_hashtags_chart.png
```

### 2. 📈 Daily Engagement Trend

Shows how total engagement changes across different dates.

```text
daily_engagement_trend.png
```

### 3. 🥧 Content Category Distribution

Shows the proportion of posts belonging to different content
categories.

```text
content_category_distribution.png
```

### 4. 😊 Sentiment Distribution

Shows the distribution of:

* Positive posts
* Neutral posts
* Negative posts

```text
sentiment_distribution.png
```

---

## 🖥️ Bonus Challenge -- Interactive Streamlit Dashboard

An advanced and interactive **Streamlit application** was created for
social media trend analysis.

The dashboard provides a modern interface for exploring social media
data and analytics results.

### Dashboard Features

* Upload a social media CSV dataset
* View dataset information
* Search social media posts
* Filter posts dynamically
* Analyze top trending hashtags
* Identify the most active users
* View engagement metrics
* Analyze daily engagement trends
* View content category distribution
* Detect popular posting times
* Perform sentiment analysis
* View Positive, Neutral, and Negative sentiment distribution
* Explore interactive charts
* Download analytics reports
* View key performance metrics in a dashboard layout

The application also includes an improved user interface designed to
make social media analytics easier to explore and understand.

### Run the Dashboard Locally

Open the terminal inside the project folder and run:

```bash
streamlit run app.py
```

Streamlit will generate a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your browser to use the Social Media Trend Analyzer.

---

## 📤 Analytics Report Export

The project generates and exports an analytics report as:

```text
social_media_analytics_report.csv
```

The exported report can contain useful social media analytics results
generated during the analysis process.

This makes it possible to save and reuse the results outside the
application.

---

## 📚 Key Learnings

Through this project, I practiced and improved my understanding of:

* Working with CSV files in Python
* Data analysis using Pandas
* Data preprocessing
* Social media data analysis
* Hashtag extraction and frequency analysis
* User activity analysis
* Engagement calculation
* Time-based data analysis
* Daily trend analysis
* Content category analysis
* Sentiment analysis
* Data visualization using Matplotlib
* Generating and saving PNG charts
* Exporting analytics results to CSV
* Building interactive applications using Streamlit
* Implementing search functionality
* Implementing dashboard filters
* Designing a modern and user-friendly analytics dashboard

---

## 🚀 How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shreya934-bot/rftinternship.git
```

### Step 2: Navigate to the Project Folder

```bash
cd RFTinternship/Day\ 27
```

### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 4: Run the Python Analysis Script

```bash
python social_media_trend_analyzer.py
```

This will process the dataset and generate the analytics results and
visualization files.

### Step 5: Run the Streamlit Application

```bash
streamlit run app.py
```

---

## 📌 Project Outcome

This project successfully demonstrates an end-to-end **Social Media
Trend Analyzer**.

The system analyzes social media data and generates meaningful insights
through:

* CSV data processing
* Social media post analysis
* Trending hashtag detection
* Active user identification
* Engagement calculation
* Popular posting time analysis
* Daily engagement trend analysis
* Content category distribution analysis
* Sentiment classification
* Positive, Neutral, and Negative sentiment analysis
* Analytics report generation
* CSV export
* Automated chart generation
* Interactive Streamlit dashboard development
* Search and filtering functionality

The project demonstrates how Python, data analysis, visualization, and
interactive dashboards can be combined to transform raw social media
data into useful insights.

---

## 👩‍💻 About Me

I am **Shreya Verma**, a Computer Science Engineering student
specializing in **Artificial Intelligence & Machine Learning**.

I am passionate about building practical projects in:

* Machine Learning
* Data Science
* Data Analytics
* Artificial Intelligence
* Python Development

This project is part of my continuous hands-on learning journey during
the **RFT Python Internship at GOW AI Academy**.

---

## 🔗 Connect With Me

* **GitHub:** [https://github.com/Shreya934-bot](https://github.com/Shreya934-bot)
* **LinkedIn:** [https://www.linkedin.com/in/shreya-verma-2b73b6290](https://www.linkedin.com/in/shreya-verma-2b73b6290)

---

⭐ **Day 27 of the RFT Python Internship -- Social Media Trend Analyzer**


