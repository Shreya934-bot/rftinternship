# 🌦️ Day 24 – Weather Data Analytics System

## 📌 Project Overview

This project was completed as part of my **RFT Python Internship at GOW AI Academy**.

The **Weather Data Analytics System** analyzes weather data from a CSV dataset to identify temperature patterns, compare cities, analyze weather conditions, and generate meaningful insights.

The project includes data analysis, visualization, report generation, temperature prediction using a moving average, and an interactive dashboard built using **Streamlit**.

---

## 🎯 Objectives

The main objectives of this project are:

- Read and analyze weather data from a CSV file
- Calculate the average temperature for each city
- Identify the hottest city
- Identify the coldest city
- Count rainy days
- Count sunny days
- Analyze temperature trends over time
- Visualize weather condition distribution
- Compare average temperatures across cities
- Export the final analysis report as a CSV file
- Predict tomorrow's temperature using a moving average
- Build an interactive Streamlit dashboard

---

## 📂 Project Files

```text
Day 24/
│
├── weather_data.csv
├── weather_analytics.py
├── weather_analytics.ipynb
├── streamlit_dashboard.py
├── final_weather_report.csv
├── temperature_trend.png
├── weather_distribution.png
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

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## 📊 Dataset Analysis

The weather dataset contains information related to different cities and their weather conditions.

The analysis includes:

* City-wise temperature analysis
* Daily temperature trends
* Weather condition analysis
* Rainy day count
* Sunny day count
* Average temperature calculation
* Hottest city identification
* Coldest city identification

---

## 📈 Visualizations

### 🌡️ Temperature Trend

A line chart is used to visualize changes in temperature over time and identify weather patterns.

**Output:**

```text
temperature_trend.png
```

### 🌧️ Weather Distribution

A chart is used to show the distribution of different weather conditions in the dataset.

For example:

* Sunny
* Rainy
* Cloudy
* Other weather conditions

**Output:**

```text
weather_distribution.png
```

### 📊 Average Temperature per City

A comparison chart is used to analyze the average temperature across different cities.

This helps identify:

* The hottest city
* The coldest city
* Temperature differences between cities

---

## 🔥 Key Analysis Performed

### 1. Average Temperature per City

The dataset is grouped by city to calculate the average temperature.

```python
df.groupby("City")["Temperature"].mean()
```

---

### 2. Hottest City

The city with the highest average temperature is identified from the dataset.

---

### 3. Coldest City

The city with the lowest average temperature is identified from the dataset.

---

### 4. Rainy Days Count

The total number of days with rainy weather is calculated.

---

### 5. Sunny Days Count

The total number of days with sunny weather is calculated.

---

### 6. Temperature Trend Analysis

A line chart is used to visualize how temperature changes over time.

---

## 🔮 Bonus Challenge – Temperature Prediction

A **moving average** approach is used to estimate tomorrow's temperature based on recent temperature values.

The moving average helps smooth short-term fluctuations and identify the general temperature trend.

---

## 🖥️ Interactive Streamlit Dashboard

As a bonus challenge, an interactive dashboard was created using **Streamlit**.

The dashboard allows users to explore weather analytics in an interactive and user-friendly interface.

### Dashboard Features

* View weather dataset
* Analyze key weather metrics
* View average temperature by city
* Identify hottest and coldest cities
* Analyze rainy and sunny days
* Explore temperature trends
* View weather distribution
* Interact with filters
* View moving average temperature prediction

### Run the Dashboard Locally

Open the terminal inside the project folder and run:

```bash
streamlit run streamlit_dashboard.py
```

Streamlit will generate a local URL, usually:

```text
http://localhost:8501
```

Open this URL in your browser to view the dashboard.

---

## 📄 Final Report

The final analysis report is exported as:

```text
final_weather_report.csv
```

This report contains the processed results and important weather analysis findings.

---

## 📚 Key Learnings

Through this project, I practiced and improved my understanding of:

* Working with CSV files
* Data analysis using Pandas
* Data grouping and aggregation
* Calculating averages
* Finding maximum and minimum values
* Data filtering
* Weather data analysis
* Data visualization using Matplotlib
* Line charts
* Bar charts
* Pie charts
* Time-series trend analysis
* Moving average calculations
* Basic temperature prediction
* Exporting reports to CSV
* Building interactive dashboards using Streamlit

---

## 🚀 How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shreya934-bot/rftinternship.git
```

### Step 2: Navigate to the Project Folder

```bash
cd RFTinternship/Day 24
```

### Step 3: Install Required Libraries

```bash
pip install pandas matplotlib streamlit
```

### Step 4: Run the Python Analysis

```bash
python weather_analytics.py
```

### Step 5: Run the Streamlit Dashboard

```bash
streamlit run streamlit_dashboard.py
```

---

## 📌 Project Outcome

This project successfully demonstrates an end-to-end **Weather Data Analytics System**.

The system transforms raw weather data into meaningful insights through:

* Data processing
* Statistical analysis
* Temperature comparison
* Weather condition analysis
* Data visualization
* Report generation
* Moving average prediction
* Interactive dashboard development

---

## 👩‍💻 About Me

I am **Shreya Verma**, a Computer Science Engineering student specializing in **Artificial Intelligence & Machine Learning**.

I am passionate about building practical projects in:

* Machine Learning
* Data Science
* Data Analytics
* Artificial Intelligence
* Python Development

This project is part of my continuous hands-on learning journey during the **RFT Python Internship at GOW AI Academy**.

---

## 🔗 Connect With Me

* **GitHub:** [https://github.com/Shreya934-bot](https://github.com/Shreya934-bot)
* **LinkedIn:** [https://www.linkedin.com/in/shreya-verma-2b73b6290](https://www.linkedin.com/in/shreya-verma-2b73b6290)

---

⭐ **Day 24 of the RFT Python Internship – Weather Data Analytics System**

```

This README is suitable for GitHub and clearly includes the **main task + both bonus challenges**, especially your working Streamlit dashboard. 
```
