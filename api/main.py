# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import document

app = FastAPI(title="AI Financial Document Backend")

# Enable CORS so Streamlit can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router)

@app.get("/")
async def root():
    return {"message": "✅ FastAPI AI Backend is Running!"}
