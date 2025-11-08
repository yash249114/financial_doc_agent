# api/models/schemas.py
from pydantic import BaseModel
from typing import Optional, List

class DocumentRequest(BaseModel):
    file_name: str
    file_type: str
    content: Optional[str] = None

class DocumentResponse(BaseModel):
    summary: str
    confirmed_label: str
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    invoice_number: Optional[str] = None
    total_amount: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    vendor_name: Optional[str] = None
    tax_rate: Optional[str] = None
    tax_amount: Optional[str] = None
    subtotal: Optional[str] = None
