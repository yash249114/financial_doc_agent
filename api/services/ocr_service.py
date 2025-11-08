# api/services/ocr_service.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import tempfile
import asyncio


async def extract_text_from_pdf(file):
    """
    Extracts text from PDF or image using PyMuPDF / Tesseract.
    Supports FastAPI UploadFile (async) input.
    Returns extracted text or a clear error message if OCR fails.
    """

    try:
        # ✅ Read bytes properly (await if async)
        if hasattr(file, "read"):
            if asyncio.iscoroutinefunction(file.read):
                file_bytes = await file.read()
            else:
                file_bytes = file.read()
        else:
            return "⚠️ Invalid file input."

        # ✅ Save temporarily for PyMuPDF or PIL
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        text_content = ""

        # ✅ Handle PDFs
        if file.filename.lower().endswith(".pdf"):
            with fitz.open(tmp_path) as pdf:
                for page in pdf:
                    text_content += page.get_text("text")

        # ✅ Handle Images
        elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image = Image.open(io.BytesIO(file_bytes))
            text_content = pytesseract.image_to_string(image)

        else:
            return "⚠️ Unsupported file type."

        # ✅ Clean up extracted text
        text_content = text_content.strip()

        # ✅ If OCR fails or is empty
        if not text_content or len(text_content) < 30:
            return "⚠️ OCR extraction failed — no readable text found."

        return text_content

    except Exception as e:
        return f"⚠️ OCR extraction error: {e}"
