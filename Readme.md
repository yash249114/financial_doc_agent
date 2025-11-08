# 🤖 Agenti-AI Financial Insight Analyzer  
> AI-powered Financial Document & Dataset Intelligence System  

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/FastAPI-Backend-green)
![UI](https://img.shields.io/badge/Streamlit-Frontend-orange)
![Model](https://img.shields.io/badge/Gemini-2.5%20Flash-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧠 Overview
**Agent-AI Financial Insight Analyzer** is an intelligent system that processes and analyzes financial documents such as invoices, receipts, statements, and reports using **Google Gemini 2.5 Flash**, **FastAPI**, and **Streamlit**.

It automatically performs:
- 🔍 OCR text extraction from PDFs & images  
- 🧾 Document classification (Invoice, Receipt, Tax Document, etc.)  
- 🤖 AI-based summarization and entity extraction  
- 📊 CSV / Excel data insights with Gemini analytics  
- 💻 Beautiful Material-Dark Streamlit UI  

---

## 🏗️ Tech Stack
| Layer | Technology |
|:------|:------------|
| **Backend API** | FastAPI (Python 3.10+) |
| **Frontend UI** | Streamlit |
| **AI Model** | Gemini 2.5 Flash (via Google Generative AI SDK) |
| **OCR Engine** | PyMuPDF + Tesseract |
| **Data Handling** | Pandas |
| **Environment** | dotenv, psutil |

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/financial_doc_agent.git
cd financial_doc_agent
# for windows
# Clone repo → create virtual environment → install dependencies → run project
git clone https://github.com/yash249114/financial_doc_agent.git && cd financial_doc_agent && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python run_project.py
# for MacOS/linux
git clone https://github.com/yash249114/financial_doc_agent.git && cd financial_doc_agent && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 run_project.py
