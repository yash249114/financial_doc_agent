# api/services/gemini_service.py
import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv

# ==========================================================
# 🔹 Load environment variables from .env
# ==========================================================
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please check your .env file.")

# ==========================================================
# 🔹 Initialize Gemini Client (for google-genai==1.49.0)
# ==========================================================
client = genai.Client(api_key=api_key)


# ----------------------------------------------------------
# 1️⃣ For PDFs / Images / OCR-based Documents
# ----------------------------------------------------------
def summarize_with_gemini(document_text: str, label: str):
    """
    Summarizes unstructured OCR text (PDF/Image) using Gemini Flash.
    Compatible with google-genai==1.49.0 syntax.
    """

    if (
        not document_text
        or "⚠️ OCR" in document_text
        or "Unsupported file" in document_text
        or len(document_text.strip()) < 30
    ):
        return {
            "summary": "Due to an OCR extraction error, the content of the document is unavailable. Therefore, no summary can be provided.",
            "confirmed_label": "N/A",
            "invoice_number": None,
            "total_amount": None,
            "invoice_date": None,
            "due_date": None,
            "vendor_name": None,
            "tax_rate": None,
            "tax_amount": None,
            "subtotal": None,
        }

    truncated_text = document_text[:6000]

    prompt = f"""
    You are a professional financial document analysis AI.

    The following text was extracted from a document:
    {truncated_text}

    The system classified this as: {label}.

    Tasks:
    1️⃣ Summarize the document contents in 3–4 lines.
    2️⃣ Confirm if the classification '{label}' is correct. If not, suggest a better type.
    3️⃣ Extract key entities such as invoice number, total amount, date, vendor, and taxes.
    4️⃣ Respond ONLY in strict JSON format like this:
    {{
        "summary": "...",
        "confirmed_label": "...",
        "invoice_number": "...",
        "total_amount": "...",
        "invoice_date": "...",
        "due_date": "...",
        "vendor_name": "...",
        "tax_rate": "...",
        "tax_amount": "...",
        "subtotal": "..."
    }}
    """

    try:
        # ✅ Use correct syntax for google-genai==1.49.0
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )

        # ✅ Extract model text output properly
        text_output = getattr(response, "text", None) or str(response)

        # ✅ Try to parse JSON-like structured output
        if "{" in text_output and "}" in text_output:
            try:
                json_str = text_output[text_output.index("{"): text_output.rindex("}") + 1]
                return json.loads(json_str)
            except Exception:
                pass  # fallback

        return {"summary": text_output.strip()}

    except Exception as e:
        return {
            "summary": f"⚠️ Gemini API Error: {e}",
            "confirmed_label": "N/A",
            "invoice_number": None,
            "total_amount": None,
            "invoice_date": None,
            "due_date": None,
            "vendor_name": None,
            "tax_rate": None,
            "tax_amount": None,
            "subtotal": None,
        }


# ----------------------------------------------------------
# 2️⃣ For CSV / Excel / Structured Tabular Data
# ----------------------------------------------------------
def analyze_tabular_data_with_gemini(df: pd.DataFrame):
    """
    Uses Gemini Flash to analyze financial datasets (CSV/Excel).
    Works with google-genai==1.49.0 syntax.
    """

    table_preview = df.head(20).to_csv(index=False)

    prompt = f"""
    You are a financial analytics AI assistant.

    The user uploaded this dataset:
    {table_preview}

    Tasks:
    1️⃣ Identify what kind of dataset this is (e.g., invoices, transactions, sales, etc.).
    2️⃣ Compute insights such as:
        - Total revenue (sum of numeric columns)
        - Top vendors/customers by frequency
        - Average transaction
        - Detect anomalies or outliers
    3️⃣ Provide a business-level summary.
    4️⃣ Respond ONLY in strict JSON format:
    {{
        "dataset_type": "...",
        "summary": "...",
        "total_amount": "...",
        "top_vendors": ["..."],
        "average_transaction": "...",
        "insights": "..."
    }}
    """

    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )

        text_output = getattr(response, "text", None) or str(response)

        if "{" in text_output and "}" in text_output:
            try:
                json_str = text_output[text_output.index("{"): text_output.rindex("}") + 1]
                return json.loads(json_str)
            except Exception:
                pass

        return {"summary": text_output.strip()}

    except Exception as e:
        return {"summary": f"⚠️ Gemini API Error: {e}"}
