# src/agent/schemas.py
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class ActionType(str, Enum):
    REPLY = "reply"           # LLM antwortet selbstständig
    ESCALATE = "escalate"     # Human in the loop benötigt

class EmailAnalysis(BaseModel):
    summary: str = Field(..., description="Zusammenfassung des Patientenanliegens in 1 Satz.")
    order_status_match: bool = Field(..., description="Passt die Mail zum aktuellen Bestellstatus? (z.B. Patient fragt 'Wo Ware?', Status ist 'Versendet')")
    suggested_action: ActionType
    draft_subject: Optional[str] = None
    draft_body: Optional[str] = Field(None, description="Der Antwortvorschlag an den Patienten (höflich, Deutsch).")
    reasoning: str = Field(..., description="Warum wurde diese Aktion gewählt?")
    confidence: float = Field(..., description="Wie sicher ist sich das Modell (0.0 - 1.0)?")