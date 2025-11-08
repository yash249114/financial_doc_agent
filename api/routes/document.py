import time
import psutil
import pandas as pd
import io
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from api.services.ocr_service import extract_text_from_pdf
from api.services.gemini_service import summarize_with_gemini, analyze_tabular_data_with_gemini
from api.services.classification_service import classify_text, KEYWORDS
from api.services.reasoning_service import explain_reasoning

router = APIRouter()


# ---------------------------------------------------------
# 🔹 Utility: measure latency and CPU usage
# ---------------------------------------------------------
def get_metrics(start_time):
    latency = round(time.time() - start_time, 3)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    return {"latency_s": latency, "cpu_percent": cpu_percent}


# ---------------------------------------------------------
# 🔹 Main route: document analysis (PDF, Image, CSV, Excel)
# ---------------------------------------------------------
@router.post("/analyze/")
async def analyze_document(file: UploadFile = File(...)):
    """
    Main route for AI document processing — supports:
    - PDFs / Images via OCR
    - CSV / Excel via Gemini Tabular Analyzer
    """
    start_time = time.time()
    file_name = file.filename.lower()
    print(f"🧾 Processing: {file_name}")

    try:
        # -------------------------------
        # 1️⃣ TABULAR FILES (CSV/Excel)
        # -------------------------------
        if file_name.endswith((".csv", ".xlsx", ".xls")):
            file_bytes = await file.read()

            if file_name.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(file_bytes))
            else:
                df = pd.read_excel(io.BytesIO(file_bytes))

            gemini_data = analyze_tabular_data_with_gemini(df)

            result = {
                "Filename": file.filename,
                "Predicted Label": "Tabular Data",
                "Confidence": "N/A",
                "Reasoning": "Detected tabular structure, processed with Gemini analytics model.",
                **get_metrics(start_time),
                **gemini_data
            }

            return JSONResponse(content=result)

        # -------------------------------
        # 2️⃣ DOCUMENTS (PDF/Image)
        # -------------------------------
        else:
            # ✅ Await the async OCR extraction
            text = await extract_text_from_pdf(file)

            # Safety: Ensure we always have a string
            if not isinstance(text, str):
                text = str(text)

            # Step 2: Classification
            label, confidence = classify_text(text)

            # Step 3: Reasoning
            reasoning = explain_reasoning(text, label, KEYWORDS)

            # Step 4: Gemini Summarization
            gemini_data = summarize_with_gemini(text, label)

            # Step 5: Combine results
            metrics = get_metrics(start_time)
            result = {
                "Filename": file.filename,
                "Predicted Label": label,
                "Confidence": confidence,
                "Reasoning": reasoning,
                **metrics
            }

            # Merge Gemini data (structured)
            if isinstance(gemini_data, dict):
                result.update(gemini_data)
            else:
                result["Summary"] = str(gemini_data)

            return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            content={"error": f"⚠️ Internal error: {str(e)}"},
            status_code=500
        )
