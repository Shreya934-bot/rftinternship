# 💰 Smart Expense Tracker & Budget Analyzer

## 📌 Day 29 – RFT Python Internship

### 🎯 Task Overview

The task for Day 29 was to build a **Smart Expense Tracker & Budget Analyzer** using Python.

The objective was to import monthly expense data, automatically categorize expenses, calculate savings, generate budget insights, visualize spending patterns, export analytical reports, and estimate future expenses.

---

## 💡 Tasks Completed

### 📂 Data Processing

- Read monthly expense data from a CSV file
- Processed and analyzed expense records using Pandas
- Converted expense dates for monthly and daily analysis
- Validated required dataset columns
- Handled invalid dates and expense amounts
- Prepared the dataset for analysis

---

### 🏷️ Automatic Expense Categorization

Expenses were automatically categorized using description-based keyword matching.

Categories include:

- Food & Dining
- Transport
- Shopping
- Bills & Utilities
- Entertainment
- Health
- Education
- Travel
- Rent & Housing
- Personal Care
- Other

This allows raw expense descriptions to be transformed into meaningful spending categories.

---

### 💵 Monthly Savings Analysis

Monthly financial metrics were calculated from the expense data.

The analysis includes:

- Total monthly expenses
- Monthly income
- Monthly savings
- Savings rate
- Average expense
- Largest expense
- Total number of transactions

---

### 🎯 Budget Analysis

Actual spending was compared against predefined category budgets.

The budget analysis identifies:

- Budget amount
- Actual spending
- Remaining budget
- Budget variance
- Budget utilization percentage
- Categories that are over budget
- Categories that remain within budget

---

## 📊 Visualizations Generated

The project generates the following visualizations:

### 1. 📈 Monthly Spending Trend

Shows how total expenses change across different months.

### 2. 📊 Top Expense Categories

Identifies the categories where the highest amount of money is being spent.

### 3. 🥧 Spending Distribution by Category

Displays the percentage contribution of each expense category to total spending.

### 4. 📉 Daily Spending Analysis

Shows daily changes in expense amounts over time.

### 5. 🎯 Budget vs Actual Spending

Compares planned category budgets with actual expenses.

### 6. 📅 Spending by Day of Week

Analyzes which days of the week account for higher spending.

---

## 📥 Expense Report

The analyzed expense data is exported into separate CSV reports.

Generated reports include:

- Cleaned expense dataset
- Monthly expense summary
- Category expense summary
- Daily expense summary
- Budget analysis

These reports can be used for further financial analysis and record keeping.

---

## ⭐ Bonus Challenge

### 🔮 Expense Prediction

A simple trend-based prediction system was implemented to estimate the next month's expenses.

The prediction uses the latest three months of expense data and applies a linear trend to estimate future spending.

This provides a basic view of whether expenses may continue increasing or decreasing.

> ⚠️ The prediction is an educational estimate and should not be treated as financial advice.

---

### 🖥️ Streamlit Dashboard

An interactive Streamlit dashboard was also developed for exploring the expense data.

The dashboard includes:

- Expense overview metrics
- Monthly spending analysis
- Category-wise spending analysis
- Daily spending trends
- Budget analysis
- Over-budget alerts
- Expense prediction
- Transaction search
- Category filters
- CSV report download

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook

---

## 📂 Project Structure

```text
Day 29/
│
├── expense_tracker.py
├── app.py
├── Day29_Smart_Expense_Tracker.ipynb
├── sample_expenses.csv
├── cleaned_expenses.csv
├── monthly_expense_summary.csv
├── category_expense_summary.csv
├── daily_expense_summary.csv
├── budget_analysis.csv
├── monthly_spending_trend.png
├── category_spending.png
├── category_distribution.png
├── daily_spending.png
├── budget_vs_actual.png
├── weekday_spending.png
├── requirements.txt
└── README.md
```

---

## 📚 Concepts Practiced

* CSV File Handling
* Data Validation
* Data Cleaning
* Missing Value Handling
* Data Filtering
* Automatic Categorization
* Expense Analysis
* Budget Analysis
* Savings Calculation
* Percentage Calculation
* GroupBy Operations
* Data Aggregation
* Monthly Analysis
* Daily Analysis
* Time-Series Analysis
* Trend Analysis
* Expense Prediction
* Data Visualization
* Matplotlib
* Plotly
* Interactive Dashboards
* Streamlit
* Search and Filters
* CSV Report Export
* Jupyter Notebook

---

## 🎯 Key Learning Outcomes

Through this project, I practiced how to:

* Analyze monthly expense data using Python
* Clean and validate CSV datasets
* Automatically categorize expenses
* Calculate total spending and monthly savings
* Calculate savings rate
* Compare actual expenses with category budgets
* Identify over-budget spending
* Analyze daily and monthly spending trends
* Generate meaningful financial visualizations
* Create a basic trend-based expense prediction
* Build an interactive analytics dashboard using Streamlit
* Add search and filtering functionality to a dashboard
* Export cleaned data and analytical reports as CSV files
* Document an end-to-end Python data analytics project

---

## ✅ Task Completion Status

* [x] Import monthly expense data from CSV
* [x] Validate and clean expense data
* [x] Categorize expenses automatically
* [x] Calculate monthly expenses
* [x] Calculate monthly savings
* [x] Calculate savings rate
* [x] Generate budget summary
* [x] Detect over-budget categories
* [x] Generate Monthly Spending Trend
* [x] Generate Top Expense Categories chart
* [x] Generate Spending Distribution chart
* [x] Generate Daily Spending Analysis
* [x] Generate Budget vs Actual chart
* [x] Generate Spending by Day of Week chart
* [x] Export cleaned expense data
* [x] Export monthly expense summary
* [x] Export category expense summary
* [x] Export daily expense summary
* [x] Export budget analysis
* [x] Implement expense prediction
* [x] Build a Streamlit dashboard
* [x] Add search and filtering
* [x] Create Jupyter Notebook implementation

---

## 🚀 Day 29 Completed

This project was completed as part of the **RFT Python Internship**.

**Day 29 focuses on combining Python data analysis, expense categorization, budgeting, savings analysis, visualization, trend prediction, report generation, and interactive dashboard development into a single end-to-end project.** 💰📊
