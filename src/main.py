from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent.service import agent_instance

app = FastAPI(title="Cannaleo Support Agent", version="0.1.0")

# Input Model für die API (Was wir vom Frontend/Mail-System erwarten)
class InquiryRequest(BaseModel):
    email_text: str
    order_id: str  # Wir brauchen die ID, um den Status zu "fetchen"

@app.get("/")
def health_check():
    """Einfacher Check, ob der Container läuft."""
    return {"status": "online", "service": "support-agent"}

@app.post("/analyze")
async def analyze_inquiry(request: InquiryRequest):
    """
    Haupt-Endpunkt: Nimmt E-Mail entgegen, holt (simulierten) Status 
    und lässt den LLM-Agenten entscheiden.
    """
    
    # 1. MOCK SCRAPER: Hier würden wir normalerweise den Scraper aufrufen.
    # Für den POC simulieren wir eine Antwort basierend auf der Order-ID.
    order_context = mock_scraper_lookup(request.order_id)
    
    if not order_context:
        # Fallback, falls ID nicht gefunden (sollte real nicht passieren)
        order_context = {"status": "Unknown", "details": "Bestellung nicht gefunden"}

    # 2. AGENT AUFRUF: Das Herzstück
    analysis_result = await agent_instance.process_inquiry(
        email_text=request.email_text,
        order_context=order_context
    )

    # 3. Antwort zurückgeben
    return {
        "order_context_used": order_context,
        "analysis": analysis_result
    }

# --- HILFSFUNKTION (Nur für Demo/POC) ---
def mock_scraper_lookup(order_id: str) -> dict:
    """
    Simuliert die Datenbank/Scraper-Abfrage.
    Je nach ID geben wir einen anderen Status zurück, um den Agenten zu testen.
    """
    mock_db = {
        "12345": {
            "status": "Versendet", 
            "tracking_url": "https://dhl.de/123", 
            "shipped_date": "2023-10-27"
        },
        "67890": {
            "status": "In Bearbeitung", 
            "notes": "Warten auf Rezept-Original vom Arzt"
        },
        "ERROR": {
            "status": "Storniert",
            "reason": "Zahlung abgelehnt"
        }
    }
    return mock_db.get(order_id, {"status": "Nicht gefunden"})