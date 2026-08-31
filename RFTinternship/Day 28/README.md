# 📈 Stock Market Portfolio Analyzer

**Day 28 — Python Internship Journey**

A complete Python-based stock portfolio analysis project that reads historical stock data from CSV, calculates portfolio performance, visualizes investment trends, and provides a Streamlit dashboard.

## ✨ Features

- Read stock price data from CSV
- Calculate investment and current portfolio value
- Calculate Profit/Loss for each stock
- Calculate return percentage for every stock
- Identify best and worst performing stocks
- Calculate overall portfolio return
- Generate portfolio growth analysis
- Analyze daily portfolio returns
- Analyze sector-wise investment
- Bonus: Moving Average based next-day trend signal
- Interactive Streamlit dashboard
- CSV report download

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit

## 📁 Project Structure

```text
Day28_Stock_Portfolio_Analyzer/
│
├── app.py
├── portfolio_analyzer.py
├── stock_prices.csv
├── requirements.txt
├── README.md
│
└── charts/
    ├── portfolio_growth.png
    ├── sector_investment.png
    └── daily_return.png
```

## 📄 CSV Format

The analyzer expects these columns:

```text
Date,Ticker,Sector,Close,Quantity
```

Example:

```text
2026-07-01,TCS,IT,3200,5
```

## 🚀 Run the Python Analyzer

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python portfolio_analyzer.py
```

The script generates:

- `portfolio_report.csv`
- `daily_returns.csv`
- charts inside `charts/`

## 🌐 Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard provides:

1. Portfolio summary cards
2. Stock-level performance table
3. Portfolio growth chart
4. Sector investment chart
5. Daily return chart
6. Moving Average trend signal
7. CSV upload
8. Report download

## 🧠 How the Calculations Work

### Investment

```text
Investment = Buy Price × Quantity
```

### Current Value

```text
Current Value = Current Price × Quantity
```

### Profit/Loss

```text
Profit/Loss = Current Value − Investment
```

### Return

```text
Return % = (Profit/Loss / Investment) × 100
```

### Moving Average

The bonus feature compares the latest closing price with the average closing price over the selected window.

```text
Latest Price > Moving Average → UP
Latest Price < Moving Average → DOWN
```

This is intentionally a simple educational signal, not a financial forecasting model.

## 📊 Expected Output

The project answers questions such as:

- Which stock performed best?
- Which stock performed worst?
- How much money was invested?
- What is the current portfolio value?
- What is the overall return?
- Which sector has the largest allocation?
- How did portfolio value change over time?
- What was the daily return?
- Is the latest price above or below its moving average?

## ⚠️ Disclaimer

This project is for educational and portfolio purposes only. The moving-average signal is not financial advice and should not be treated as a guaranteed prediction of future stock prices.

---

### 👩‍💻 Python Internship — Day 28

Built as part of a hands-on Python internship journey, progressing from data analysis to interactive dashboards and practical ML concepts.
