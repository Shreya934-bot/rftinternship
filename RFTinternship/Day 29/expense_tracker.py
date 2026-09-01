
from pathlib import Path
import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "charts"

REQUIRED_COLUMNS = {"Date", "Description", "Amount"}

CATEGORY_RULES = {
    "Food & Dining": ["food","grocery","groceries","swiggy","zomato","restaurant","cafe","coffee","bakery","dining","meal","lunch","dinner","breakfast"],
    "Transport": ["uber","ola","fuel","petrol","diesel","metro","bus","train","cab","transport","parking","toll"],
    "Shopping": ["amazon","flipkart","myntra","shopping","clothes","fashion","shoes","electronics","mall","purchase"],
    "Bills & Utilities": ["electricity","water","internet","wifi","mobile","phone","recharge","gas","utility","bill"],
    "Entertainment": ["movie","netflix","spotify","prime","concert","game","gaming","entertainment"],
    "Health": ["pharmacy","medicine","hospital","doctor","clinic","health","medical","gym"],
    "Education": ["course","book","books","udemy","coursera","education","college","tuition","stationery"],
    "Travel": ["hotel","flight","airbnb","travel","trip","booking","vacation"],
    "Rent & Housing": ["rent","maintenance","housing","hostel"],
    "Personal Care": ["salon","spa","cosmetics","beauty","personal care"],
}

DEFAULT_BUDGETS = {
    "Food & Dining": 10000, "Transport": 5000, "Shopping": 7000,
    "Bills & Utilities": 7000, "Entertainment": 4000, "Health": 4000,
    "Education": 3000, "Travel": 5000, "Rent & Housing": 15000,
    "Personal Care": 2500, "Other": 3000
}

def header():
    print("\n" + "=" * 72)
    print(" SMART EXPENSE TRACKER & BUDGET ANALYZER")
    print("   RFT Python Internship — Day 29")
    print("=" * 72)

def section(title):
    print("\n" + "-" * 72)
    print(title)
    print("-" * 72)

def get_dataset_path():
    """Dataset submission block: CLI path, interactive path, or sample dataset."""
    section(" DATASET SUBMISSION")
    print("Required: Date, Description, Amount")
    print("Optional: Category")
    print("Press Enter to use data/sample_expenses.csv.\n")

    if len(sys.argv) > 1:
        path = Path(sys.argv[1]).expanduser()
    else:
        value = input("Enter CSV path: ").strip().strip('"')
        path = DATA_DIR / "sample_expenses.csv" if not value else Path(value).expanduser()

    if not path.exists():
        print(f" File not found: {path}")
        return None
    if path.suffix.lower() != ".csv":
        print(" Please submit a CSV file.")
        return None

    print(f" Dataset selected: {path}")
    return path

def load_dataset(path):
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))

    before = len(df)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Description"] = df["Description"].astype(str).str.strip()
    df = df.dropna(subset=["Date", "Amount"])
    df = df[df["Amount"] >= 0]
    df = df[df["Description"].str.len() > 0].copy()

    if "Category" not in df.columns:
        df["Category"] = ""

    df = df.sort_values("Date").reset_index(drop=True)
    print(f" Loaded {len(df):,} valid rows ({before - len(df):,} removed).")
    return df

def categorize_expense(description):
    text = re.sub(r"[^a-z0-9\s]", " ", str(description).lower())
    for category, keywords in CATEGORY_RULES.items():
        if any(word in text for word in keywords):
            return category
    return "Other"

def auto_categorize(df):
    result = df.copy()
    existing = result["Category"].fillna("").astype(str).str.strip()
    detected = result["Description"].map(categorize_expense)
    result["Category"] = np.where(
        existing.eq("") | existing.eq("Other"), detected, existing
    )
    return result

def prepare_data(df):
    df = auto_categorize(df)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Day"] = df["Date"].dt.date.astype(str)
    df["Weekday"] = df["Date"].dt.day_name()
    return df

def calculate_summary(df, monthly_income):
    total = float(df["Amount"].sum())
    savings = monthly_income - total
    rate = savings / monthly_income * 100 if monthly_income else 0
    return {
        "income": monthly_income, "expense": total, "savings": savings,
        "savings_rate": rate, "transactions": len(df),
        "average": float(df["Amount"].mean()), "largest": float(df["Amount"].max())
    }

def monthly_summary(df):
    return (df.groupby("Month", as_index=False)["Amount"].sum()
            .rename(columns={"Amount": "Total Expense"}))

def category_summary(df):
    out = (df.groupby("Category", as_index=False)["Amount"].sum()
           .sort_values("Amount", ascending=False))
    total = out["Amount"].sum()
    out["Share %"] = out["Amount"] / total * 100 if total else 0
    return out.reset_index(drop=True)

def daily_summary(df):
    return (df.groupby("Day", as_index=False)["Amount"].sum()
            .rename(columns={"Amount": "Daily Expense"}))

def budget_analysis(df, budgets=DEFAULT_BUDGETS):
    actual = category_summary(df)[["Category","Amount"]].rename(columns={"Amount":"Actual"})
    budget = pd.DataFrame({"Category": list(budgets), "Budget": list(budgets.values())})
    out = budget.merge(actual, on="Category", how="left").fillna({"Actual":0})
    out["Variance"] = out["Budget"] - out["Actual"]
    out["Used %"] = np.where(out["Budget"] > 0, out["Actual"]/out["Budget"]*100, 0)
    out["Status"] = np.where(out["Variance"] >= 0, "Within Budget", "Over Budget")
    return out.sort_values("Used %", ascending=False)

def predict_next_month(df, periods=3):
    monthly = monthly_summary(df)
    if len(monthly) < periods:
        return None
    y = monthly.tail(periods)["Total Expense"].to_numpy(float)
    x = np.arange(periods)
    slope, intercept = np.polyfit(x, y, 1)
    return max(0.0, float(slope * periods + intercept))

def save(fig, filename):
    CHART_DIR.mkdir(exist_ok=True)
    path = CHART_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path

def generate_charts(df, budget_df):
    charts = []

    monthly = monthly_summary(df)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(monthly["Month"], monthly["Total Expense"], marker="o", linewidth=2)
    ax.set(title="Monthly Spending Trend", xlabel="Month", ylabel="Expense (₹)")
    ax.grid(alpha=.25); ax.tick_params(axis="x", rotation=35)
    charts.append(save(fig, "01_monthly_spending_trend.png"))

    cat = category_summary(df).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(cat["Category"][::-1], cat["Amount"][::-1])
    ax.set(title="Top Expense Categories", xlabel="Expense (₹)", ylabel="Category")
    charts.append(save(fig, "02_category_spending.png"))

    cat_all = category_summary(df)
    fig, ax = plt.subplots(figsize=(8,8))
    ax.pie(cat_all["Amount"], labels=cat_all["Category"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending Distribution by Category")
    charts.append(save(fig, "03_category_distribution.png"))

    daily = daily_summary(df)
    fig, ax = plt.subplots(figsize=(11,5))
    ax.plot(daily["Day"], daily["Daily Expense"], marker="o")
    ax.set(title="Daily Spending Analysis", xlabel="Date", ylabel="Daily Expense (₹)")
    ax.grid(alpha=.25); ax.tick_params(axis="x", rotation=45)
    charts.append(save(fig, "04_daily_spending.png"))

    b = budget_df[(budget_df["Budget"] > 0) | (budget_df["Actual"] > 0)]
    fig, ax = plt.subplots(figsize=(11,6))
    x = np.arange(len(b)); w = .38
    ax.bar(x-w/2, b["Budget"], w, label="Budget")
    ax.bar(x+w/2, b["Actual"], w, label="Actual")
    ax.set(title="Budget vs Actual Spending", ylabel="Amount (₹)")
    ax.set_xticks(x); ax.set_xticklabels(b["Category"], rotation=35, ha="right")
    ax.legend(); ax.grid(axis="y", alpha=.2)
    charts.append(save(fig, "05_budget_vs_actual.png"))

    weekday = df.groupby("Weekday")["Amount"].sum().reindex(
        ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    ).fillna(0)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(weekday.index, weekday.values)
    ax.set(title="Spending by Day of Week", xlabel="Day", ylabel="Expense (₹)")
    ax.tick_params(axis="x", rotation=30)
    charts.append(save(fig, "06_weekday_spending.png"))

    return charts

def export_reports(df, budget_df):
    REPORT_DIR.mkdir(exist_ok=True)
    files = {
        "cleaned_expenses.csv": df,
        "monthly_expense_summary.csv": monthly_summary(df),
        "category_expense_summary.csv": category_summary(df),
        "daily_expense_summary.csv": daily_summary(df),
        "budget_analysis.csv": budget_df,
    }
    for name, data in files.items():
        data.to_csv(REPORT_DIR / name, index=False)
    return list(files)

def main():
    header()
    path = get_dataset_path()
    if path is None:
        return

    try:
        df = prepare_data(load_dataset(path))
    except Exception as exc:
        print(f" Dataset error: {exc}")
        return

    section(" INCOME INPUT")
    while True:
        raw = input("Monthly income in ₹ [50000]: ").strip()
        if not raw:
            income = 50000.0
            break
        try:
            income = float(raw.replace(",", ""))
            if income < 0: raise ValueError
            break
        except ValueError:
            print(" Enter a valid non-negative number.")

    summary = calculate_summary(df, income)
    budget_df = budget_analysis(df)
    prediction = predict_next_month(df)

    section(" EXPENSE SUMMARY")
    print(f"Monthly Income  : ₹{summary['income']:,.2f}")
    print(f"Total Expenses  : ₹{summary['expense']:,.2f}")
    print(f"Savings         : ₹{summary['savings']:,.2f}")
    print(f"Savings Rate    : {summary['savings_rate']:.2f}%")
    print(f"Transactions    : {summary['transactions']:,}")
    print(f"Average Expense : ₹{summary['average']:,.2f}")
    print(f"Largest Expense : ₹{summary['largest']:,.2f}")

    section(" TOP CATEGORIES")
    print(category_summary(df).head(5).to_string(index=False))

    section(" BUDGET STATUS")
    over = budget_df[budget_df["Status"] == "Over Budget"]
    print(" Over budget: " + ", ".join(over["Category"]) if len(over) else "✅ All categories within budget.")

    section(" EXPENSE PREDICTION")
    if prediction is None:
        print("Need at least 3 months of data.")
    else:
        print(f"Estimated next-month expense: ₹{prediction:,.2f}")
        print("Method: linear trend over the latest 3 months.")
        print("Educational estimate — not financial advice.")

    section(" GENERATING CHARTS")
    for chart in generate_charts(df, budget_df):
        print(f" {chart.name}")

    section(" EXPORTING REPORTS")
    for name in export_reports(df, budget_df):
        print(f" {REPORT_DIR / name}")

    section("👀 DATASET PREVIEW")
    print(df[["Date","Description","Category","Amount"]].head(10).to_string(index=False))

    print("\n Day 29 analysis completed successfully!")
    print(f"Charts : {CHART_DIR}")
    print(f"Reports: {REPORT_DIR}")

if __name__ == "__main__":
    main()
