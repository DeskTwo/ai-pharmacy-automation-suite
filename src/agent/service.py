# src/agent/service.py
from openai import AsyncOpenAI
from src.agent.schemas import EmailAnalysis, ActionType
from src.gateway.config import get_settings

settings = get_settings()

class SupportAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def process_inquiry(self, email_text: str, order_context: dict) -> EmailAnalysis:
        """
        Kombiniert eingehende Mail mit Scraper-Daten (order_context),
        um eine Antwort zu generieren.
        """
        
        # Wir füttern das LLM mit dem aktuellen Wissen aus dem Scraper
        system_prompt = (
            "Du bist ein intelligenter Support-Bot für eine Cannabis-Apotheke. "
            "Deine Aufgabe: Analysiere die E-Mail des Patienten basierend auf dem beigefügten Bestellstatus (JSON). "
            "\n\nRegeln:"
            "\n1. Wenn der Status die Frage klärt (z.B. Frage: 'Wann Versand?', Status: 'Versendet inkl. Tracking'), generiere eine freundliche Antwort."
            "\n2. Wenn Daten fehlen, Widersprüche auftreten oder der Patient wütend ist -> ESCALATE."
            "\n3. Sei präzise, empathisch und professionell."
            "\n4. Antworte immer auf Deutsch."
        )

        user_content = f"""
        --- AKTUELLER BESTELLSTATUS (vom Scraper) ---
        {order_context}
        
        --- EINGEHENDE E-MAIL ---
        {email_text}
        """

        try:
            response = await self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                response_format=EmailAnalysis,
                temperature=0.1, # Geringe Kreativität für Konsistenz
            )
            return response.choices[0].message.parsed

        except Exception as e:
            # Fallback bei API Fehler -> Immer eskalieren
            return EmailAnalysis(
                summary="Systemfehler bei Analyse",
                order_status_match=False,
                suggested_action=ActionType.ESCALATE,
                reasoning=f"API Error: {str(e)}",
                confidence=0.0
            )

agent_instance = SupportAgent()