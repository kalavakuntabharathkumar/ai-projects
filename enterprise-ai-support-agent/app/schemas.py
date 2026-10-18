from typing import Literal
from pydantic import BaseModel, Field

Category = Literal["billing", "technical", "account", "shipping", "other"]
Priority = Literal["low", "normal", "high", "urgent"]

class Ticket(BaseModel):
    id: str = Field(min_length=1, max_length=100)
    subject: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1, max_length=12000)
    customer_email: str = Field(default="customer@example.com", max_length=320)

class TriageResult(BaseModel):
    ticket_id: str
    category: Category
    priority: Priority
    team: str
    summary: str
    suggested_reply: str
    confidence: float = Field(ge=0, le=1)
    prompt_version: str
    needs_human_review: bool = False
