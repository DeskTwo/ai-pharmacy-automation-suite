# In src/gateway/main.py hinzufügen

from pydantic import BaseModel
from src.agent.service import agent_instance

# Request Model für den Webhook
class InboundEmail(BaseModel):
    sender: str
    body: str
    related_order_id: str # Der Mail-Agent hat idealerweise schon eine ID extrahiert oder wir suchen sie

@app.post("/webhook/email-inbound")
async def handle_incoming_email(payload: InboundEmail):
    """
    1. Holt aktuellen Status vom Scraper (oder Cache/DB).
    2. Fragt LLM um Rat.
    3. Gibt Handlungsempfehlung zurück.
    """
    
    # 1. Daten holen (Hier simulieren wir den Scraper-Lookup)
    # In Realität: order = await db.get_order(payload.related_order_id)
    # Oder live scrapen, wenn nicht im Cache:
    current_order_data = {
        "id": payload.related_order_id,
        "status": "In Bearbeitung",
        "payment": "Bezahlt",
        "last_update": "Heute, 10:00 Uhr"
    }
    
    # 2. Agent fragen
    analysis = await agent_instance.process_inquiry(
        email_text=payload.body, 
        order_context=current_order_data
    )
    
    # 3. Ergebnis zurückgeben (Der Mail-Agent führt dann Senden oder Flaggen aus)
    return {
        "action": analysis.suggested_action,
        "draft": analysis.draft_body,
        "confidence": analysis.confidence,
        "reason": analysis.reasoning
    }