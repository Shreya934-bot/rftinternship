"""
Automated Invoice Processing System

Supports:
- CSV invoice processing
- Text-based PDF extraction
- Invoice and customer detail extraction
- Item and price extraction
- Invoice total calculation
- Overdue invoice detection
- Consolidated CSV reports
- Automated summary report
"""

from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
SAMPLE_CSV = BASE_DIR / "sample_invoices.csv"
SAMPLE_PDF_DIR = BASE_DIR / "invoices"

REQUIRED_COLUMNS = {
    "Invoice Number",
    "Customer Name",
    "Invoice Date",
}

OPTIONAL_COLUMNS = [
    "Customer Email",
    "Due Date",
    "Item",
    "Quantity",
    "Unit Price",
    "Amount",
    "Tax",
]


def parse_amount(value):
    """Convert a currency-formatted value into a float."""
    if pd.isna(value):
        return 0.0

    text = str(value).replace(",", "")
    text = re.sub(r"[^\d.\-]", "", text)

    try:
        return float(text)
    except ValueError:
        return 0.0


def parse_date(value):
    """Convert a date value into pandas datetime."""
    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT

    return pd.to_datetime(
        value,
        errors="coerce",
        dayfirst=True
    )


def extract_field(text, patterns):
    """Return the first matching field from invoice text."""
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)

        if match:
            return match.group(1).strip()

    return ""


def extract_invoice_number(text):
    return extract_field(
        text,
        [
            r"Invoice\s*(?:No|Number|#)\s*[:\-]?\s*([A-Z0-9\-/]+)",
            r"INV(?:OICE)?\s*[:#\-]?\s*([A-Z0-9\-/]+)",
        ],
    )


def extract_customer_name(text):
    return extract_field(
        text,
        [
            r"Customer\s*Name\s*[:\-]\s*(.+)",
            r"Bill\s*To\s*[:\-]\s*(.+)",
            r"Customer\s*[:\-]\s*(.+)",
        ],
    )


def extract_email(text):
    match = re.search(
        r"[\w.+-]+@[\w-]+\.[\w.-]+",
        text,
        flags=re.IGNORECASE,
    )

    return match.group(0) if match else ""


def extract_labelled_date(text, label):
    value = extract_field(
        text,
        [
            rf"{label}\s*[:\-]?\s*"
            r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}"
            r"|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}"
            r"|\d{1,2}\s+[A-Za-z]+\s+\d{4})"
        ],
    )

    return parse_date(value)


def extract_items(text):
    """Extract simple pipe-separated invoice item rows."""
    items = []

    pattern = re.compile(
        r"^(.+?)\s*\|\s*"
        r"(\d+(?:\.\d+)?)\s*\|\s*"
        r"[₹$]?\s*([\d,]+(?:\.\d+)?)\s*\|\s*"
        r"[₹$]?\s*([\d,]+(?:\.\d+)?)$"
    )

    ignored_words = (
        "item",
        "description",
        "subtotal",
        "tax",
        "total",
    )

    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = pattern.match(line)

        if not match:
            continue

        if any(
            word in match.group(1).lower()
            for word in ignored_words
        ):
            continue

        item, quantity, unit_price, line_amount = match.groups()

        items.append(
            {
                "Item": item.strip(),
                "Quantity": float(quantity),
                "Unit Price": parse_amount(unit_price),
                "Line Amount": parse_amount(line_amount),
            }
        )

    return items


def extract_invoice_total(text):
    """Extract an explicitly printed invoice total."""
    matches = re.findall(
        r"(?:Grand\s+)?Total\s*[:\-]?\s*[₹$]?\s*"
        r"([\d,]+(?:\.\d+)?)",
        text,
        flags=re.IGNORECASE,
    )

    if matches:
        return parse_amount(matches[-1])

    return 0.0


def extract_pdf_invoice(path):
    """Extract invoice data from a text-based PDF."""
    if PdfReader is None:
        raise ImportError(
            "pypdf is required for PDF processing. "
            "Install it with: pip install pypdf"
        )

    reader = PdfReader(str(path))
    text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    items = extract_items(text)

    calculated_total = sum(
        item["Line Amount"]
        for item in items
    )

    printed_total = extract_invoice_total(text)

    total = (
        printed_total
        if printed_total > 0
        else calculated_total
    )

    return {
        "Invoice Number": extract_invoice_number(text),
        "Customer Name": extract_customer_name(text),
        "Customer Email": extract_email(text),
        "Invoice Date": extract_labelled_date(
            text,
            "Invoice Date",
        ),
        "Due Date": extract_labelled_date(
            text,
            "Due Date",
        ),
        "Items": "; ".join(
            item["Item"]
            for item in items
        ),
        "Item Count": len(items),
        "Calculated Total": calculated_total,
        "Invoice Total": total,
        "Source File": path.name,
        "Source Type": "PDF",
    }


def load_csv(path):
    """Load and validate an invoice CSV."""
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    for column in OPTIONAL_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    df["Invoice Date"] = df["Invoice Date"].map(parse_date)
    df["Due Date"] = df["Due Date"].map(parse_date)

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce",
    ).fillna(1)

    for column in [
        "Unit Price",
        "Amount",
        "Tax",
    ]:
        df[column] = df[column].map(parse_amount)

    if df["Amount"].eq(0).all():
        df["Amount"] = (
            df["Quantity"] * df["Unit Price"]
            + df["Tax"]
        )

    return df


def consolidate_csv(df, source_name):
    """Combine multiple item rows into one invoice record."""
    records = []

    for invoice_number, group in df.groupby(
        "Invoice Number",
        sort=False,
    ):
        first = group.iloc[0]

        items = [
            str(item).strip()
            for item in group["Item"]
            if str(item).strip()
        ]

        total = float(group["Amount"].sum())

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
                "Source File": source_name,
                "Source Type": "CSV",
            }
        )

    return pd.DataFrame(records)


def add_payment_status(df, as_of=None):
    """Identify overdue invoices and calculate days overdue."""
    result = df.copy()

    today = (
        pd.Timestamp(as_of).normalize()
        if as_of is not None
        else pd.Timestamp.today().normalize()
    )

    result["Due Date"] = pd.to_datetime(
        result["Due Date"],
        errors="coerce",
    )

    result["Days Overdue"] = (
        today - result["Due Date"]
    ).dt.days.fillna(0).clip(lower=0).astype(int)

    result["Payment Status"] = np.where(
        result["Due Date"].notna()
        & (result["Due Date"] < today),
        "Overdue",
        "Current",
    )

    return result


def create_summary(df):
    """Create high-level invoice statistics."""
    overdue = df[
        df["Payment Status"] == "Overdue"
    ]

    return {
        "Total Invoices": int(len(df)),
        "Total Amount": float(
            df["Invoice Total"].sum()
        ),
        "Average Invoice": float(
            df["Invoice Total"].mean()
        ) if len(df) else 0.0,
        "Overdue Invoices": int(len(overdue)),
        "Overdue Amount": float(
            overdue["Invoice Total"].sum()
        ),
        "Unique Customers": int(
            df["Customer Name"].nunique()
        ),
    }


def export_reports(df, summary):
    """Export consolidated, overdue and summary reports."""
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    consolidated_path = (
        REPORT_DIR / "consolidated_invoice_report.csv"
    )

    overdue_path = (
        REPORT_DIR / "overdue_invoices.csv"
    )

    summary_path = (
        REPORT_DIR / "invoice_summary_report.csv"
    )

    df.to_csv(
        consolidated_path,
        index=False,
    )

    df[
        df["Payment Status"] == "Overdue"
    ].to_csv(
        overdue_path,
        index=False,
    )

    pd.DataFrame([summary]).to_csv(
        summary_path,
        index=False,
    )

    return [
        consolidated_path,
        overdue_path,
        summary_path,
    ]


def process_csv_file(path):
    raw = load_csv(path)
    return consolidate_csv(
        raw,
        path.name,
    )


def process_pdf_files(paths):
    records = []

    for path in paths:
        records.append(
            extract_pdf_invoice(path)
        )

    return pd.DataFrame(records)


def process(source, as_of=None):
    """
    Process a CSV file, one PDF file, or multiple PDF files.

    Returns:
        data: Processed invoice DataFrame
        summary_data: Invoice summary dictionary
    """

    # Handle multiple PDF files first
    if isinstance(source, (list, tuple)):
        if not source:
            raise ValueError("No PDF files were provided.")

        data = process_pdf_files(source)

    else:
        source_path = Path(source)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source file not found: {source_path}"
            )

        if source_path.is_file():
            extension = source_path.suffix.lower()

            if extension == ".csv":
                data = process_csv_file(source_path)

            elif extension == ".pdf":
                data = pd.DataFrame(
                    [extract_pdf_invoice(source_path)]
                )

            else:
                raise ValueError(
                    "Unsupported file type. "
                    "Use CSV or PDF."
                )

        else:
            raise ValueError(
                f"The provided path is not a file: {source_path}"
            )

    # Add payment status and overdue information
    data = add_payment_status(
        data,
        as_of=as_of
    )

    # Generate summary
    summary_data = create_summary(data)

    # Export reports
    export_reports(
        data,
        summary_data
    )

    return data, summary_data


def print_summary(summary_data):
    """Print a clean terminal summary."""
    print("\n" + "=" * 64)
    print("AUTOMATED INVOICE PROCESSING SYSTEM")
    print("=" * 64)

    print(
        f"Total invoices   : "
        f"{summary_data['Total Invoices']:,}"
    )

    print(
        f"Total amount     : "
        f"Rs. {summary_data['Total Amount']:,.2f}"
    )

    print(
        f"Average invoice  : "
        f"Rs. {summary_data['Average Invoice']:,.2f}"
    )

    print(
        f"Overdue invoices : "
        f"{summary_data['Overdue Invoices']:,}"
    )

    print(
        f"Overdue amount   : "
        f"Rs. {summary_data['Overdue Amount']:,.2f}"
    )

    print(
        f"Unique customers : "
        f"{summary_data['Unique Customers']:,}"
    )

    print("=" * 64)
    print(
        f"Reports saved to: {REPORT_DIR}"
    )


def interactive_run():
    """Run the processor from the terminal."""
    print("\nAutomated Invoice Processing System")
    print("1. Process a CSV file")
    print("2. Process a PDF file")
    print("3. Process the sample CSV")
    print("4. Process all sample PDFs")

    choice = input("\nChoose an option [3]: ").strip() or "3"

    if choice == "1":
        path = Path(
            input("Enter CSV path: ")
            .strip()
            .strip('"')
        )

        data, summary_data = process(path)

    elif choice == "2":
        path = Path(
            input("Enter PDF path: ")
            .strip()
            .strip('"')
        )

        data, summary_data = process(path)

    elif choice == "4":
        pdf_files = sorted(
            SAMPLE_PDF_DIR.glob("*.pdf")
        )

        if not pdf_files:
            raise FileNotFoundError(
                "No PDF files found in the invoices folder."
            )

        data, summary_data = process(pdf_files)

    else:
        if not SAMPLE_CSV.exists():
            raise FileNotFoundError(
                f"Sample CSV not found: {SAMPLE_CSV}"
            )

        data, summary_data = process(
            SAMPLE_CSV
        )

    print_summary(summary_data)

    return data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        processed_data, processed_summary = process(
            Path(sys.argv[1])
        )
        print_summary(processed_summary)
    else:
        interactive_run()
