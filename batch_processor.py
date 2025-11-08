import csv
import time
import psutil
from ocr_agent import extract_text_from_pdf
from classify_agent import classify_text, KEYWORDS
from reasoning_agent import explain_reasoning, get_metrics
from gemini_agent import summarize_with_gemini
import os

# Folder containing test documents
folder_path = "sample_docs"

# ✅ Output file
output_csv = "financial_doc_results.csv"

# ✅ CSV headers (flattened)
headers = [
    "Filename", "Predicted Label", "Confidence", "Reasoning",
    "Latency (s)", "CPU Usage (%)",
    "Summary", "Confirmed Label", "Invoice Number", "Total Amount",
    "Invoice Date", "Due Date", "Vendor Name", "Tax Rate", "Tax Amount", "Subtotal"
]

# Write header
with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    # Loop through all files
    for filename in os.listdir(folder_path):
        if not (filename.endswith(".pdf") or filename.endswith(".jpg") or filename.endswith(".png")):
            continue

        print(f"\n🧾 Processing: {filename}")
        start_time = time.time()
        filepath = os.path.join(folder_path, filename)

        # Step 1: Extract text
        text = extract_text_from_pdf(filepath)

        # Step 2: Classify document
        label, confidence = classify_text(text)

        # Step 3: Reasoning
        reasoning = explain_reasoning(text, label, KEYWORDS)

        # Step 4: Metrics
        metrics = get_metrics(start_time)

        # Step 5: Gemini AI summary (JSON)
        gemini_data = summarize_with_gemini(text, label)

        # ✅ Extract safely even if some keys are missing
        writer.writerow([
            filename,
            label,
            confidence,
            reasoning,
            metrics["latency_s"],
            metrics["cpu_percent"],
            gemini_data.get("summary", ""),
            gemini_data.get("confirmed_label", ""),
            gemini_data.get("invoice_number", ""),
            gemini_data.get("total_amount", ""),
            gemini_data.get("invoice_date", ""),
            gemini_data.get("due_date", ""),
            gemini_data.get("vendor_name", ""),
            gemini_data.get("tax_rate", ""),
            gemini_data.get("tax_amount", ""),
            gemini_data.get("subtotal", "")
        ])

        print(f"✅ Done: {filename}")

print("\n📊 Batch processing complete! Results saved to financial_doc_results.csv")
