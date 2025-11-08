# api/services/classification_service.py
import re

# ======================================================
# 🔹 Keyword Library for Financial Document Classification
# ======================================================
KEYWORDS = {
    "Invoice": [
        "invoice", "bill to", "total", "due date", "balance due", "invoice number", "amount due"
    ],
    "Receipt": [
        "receipt", "thank you for your purchase", "payment received", "transaction id", "paid by"
    ],
    "Purchase Order": [
        "purchase order", "vendor", "order number", "buyer", "supplier", "ordered by"
    ],
    "Bank Statement": [
        "account number", "transaction", "debit", "credit", "balance", "statement period", "ifsc"
    ],
    "Tax Document": [
        "tax", "gst", "vat", "income", "pan", "filing", "assessment year", "financial year"
    ],
    "Salary Slip": [
        "employee id", "salary", "earnings", "deductions", "net pay", "basic pay", "hra"
    ],
    "Financial Report": [
        "assets", "liabilities", "equity", "profit", "loss", "cash flow", "balance sheet"
    ],
    "Unknown": []
}

# ======================================================
# 🔹 Classification Function
# ======================================================
def classify_text(text: str):
    """
    Classifies financial document text into categories
    such as Invoice, Receipt, Bank Statement, etc.
    Returns:
        (label, confidence_score)
    """
    if not text or len(text.strip()) == 0:
        return "Unknown", 0.0

    text_lower = text.lower()
    best_match = "Unknown"
    max_score = 0

    # Check all keyword patterns
    for label, patterns in KEYWORDS.items():
        score = sum(1 for keyword in patterns if re.search(rf"\b{keyword}\b", text_lower))
        if score > max_score:
            best_match, max_score = label, score

    # Convert score to 0–1 confidence range
    confidence = round(min(max_score / 5, 1.0), 2)

    return best_match, confidence
