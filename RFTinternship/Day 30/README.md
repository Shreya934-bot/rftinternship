# 🧾 Automated Invoice Processing System

## 📌 Day 30 – RFT Python Internship | Final Day

### 🎯 Task Overview

Built an **Automated Invoice Processing System** that reads invoice data from CSV and text-based PDF files, extracts important invoice fields, calculates totals, identifies overdue invoices, generates consolidated reports, and provides a branded Streamlit interface.

---

## 💡 Tasks Completed

### 📂 Invoice Data Processing
- Read invoice data from CSV files
- Read text-based invoice data from PDF files
- Validate required invoice fields
- Clean invoice dates and monetary values
- Consolidate multiple item rows into invoice-level records

### 🧾 Invoice Information Extraction
- Invoice Number
- Customer Name
- Customer Email
- Invoice Date
- Due Date
- Item Details
- Quantity
- Unit Price
- Line Amount
- Invoice Total

### 🚨 Overdue Invoice Detection
- Current vs overdue classification
- Days overdue calculation
- Total overdue amount
- Selected as-of date for monitoring

### 📊 Consolidated Reporting
- Consolidated invoice report
- Overdue invoice report
- Automated summary report
- CSV export

## ⭐ Bonus Challenge

### 📄 Automated PDF Invoice Extraction
Text-based PDF invoices are processed automatically using `pypdf`.

> Scanned/image-only PDFs require OCR and are outside this lightweight text-PDF implementation.

### 🖥️ Streamlit Interface
The branded **SV / Shreya Verma** dashboard includes:
- CSV upload
- Multiple PDF upload
- KPI cards
- Monthly invoice value chart
- Top customer chart
- Payment status distribution
- Invoice value trend
- Overdue monitor
- Invoice search
- CSV report downloads

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- pypdf
- ReportLab
- Jupyter Notebook

## 📂 Project Structure

```text
Day30/
├── invoice_processor.py
├── app.py
├── Invoice_Processor.ipynb
├── requirements.txt
├── README.md
├── sample_invoices.csv
├── invoices/
│   ├── sample_invoice_001.pdf
│   ├── sample_invoice_002.pdf
│   └── sample_invoice_003.pdf
└── reports/
    ├── consolidated_invoice_report.csv
    ├── overdue_invoices.csv
    └── invoice_summary_report.csv
```

## 📚 Concepts Practiced

* CSV Processing
* PDF Text Extraction
* Data Validation
* Data Cleaning
* Date Parsing
* Monetary Data Processing
* GroupBy and Aggregation
* Invoice Consolidation
* Customer Detail Extraction
* Item-Level Extraction
* Total Calculation
* Overdue Detection
* Days Overdue Calculation
* Financial Reporting
* CSV Export
* Data Visualization
* Streamlit
* Plotly
* Jupyter Notebook
* File Upload Handling
* Search and Filtering

## 🎯 Key Learning Outcomes

Through this project, I practiced how to:

* Process structured invoice datasets
* Extract information from text-based PDF documents
* Validate and clean financial records
* Calculate invoice totals
* Consolidate invoice line items
* Identify overdue invoices
* Generate automated financial reports
* Build interactive financial visualizations
* Create searchable invoice dashboards
* Export processed data as CSV
* Build an end-to-end document-processing workflow

## ✅ Task Completion Status

* [x] Read invoice data from CSV
* [x] Read invoice data from PDF
* [x] Extract Invoice Number
* [x] Extract Customer Details
* [x] Extract Invoice Date
* [x] Extract Due Date
* [x] Extract Item & Price Details
* [x] Calculate Total Amount
* [x] Identify Overdue Invoices
* [x] Generate Consolidated Invoice Report
* [x] Export Final Report as CSV
* [x] Automate PDF Invoice Extraction
* [x] Generate Automated Summary Report
* [x] Create Streamlit Interface
* [x] Add Search and Filtering
* [x] Create Jupyter Notebook Implementation

## 🎉 Day 30 Completed

This project completes the **final Day of the RFT Python Internship**, combining document extraction, financial calculations, overdue detection, reporting, visualization, and dashboard development into one practical workflow.

**Final Day. Final Project. 🚀🧾**
