# Smart Order Support Agent (POC)

Ein Proof-of-Concept für die Automatisierung von Kundenanfragen im Apotheken-Umfeld mittels LLMs und Live-Daten-Kontext.

## 🎯 Problemstellung
Support-Mitarbeiter verbringen signifikante Zeit mit repetitiven Anfragen zum Bestellstatus ("Wann wird versendet?", "Ist mein Rezept eingegangen?"). Statische Auto-Responder sind oft ungenau, da sie den aktuellen Status im Warenwirtschaftssystem/Webshop nicht kennen.

## 💡 Lösung
Dieser Service fungiert als intelligente Middleware (RAG-Ansatz):
1.  **Ingest:** Empfängt E-Mails via Webhook.
2.  **Context Retrieval:** Zieht den Echtzeit-Status der Bestellung aus dem Shopsystem (simulierter Gateway-Zugriff).
3.  **Analysis:** Ein LLM (OpenAI GPT-4o-mini) analysiert die E-Mail im Kontext des Bestellstatus.
4.  **Decision Engine:**
    *   *Match:* Generiert einen präzisen Antwortentwurf (z.B. "Ihr Paket ging heute um 10:00 Uhr raus").
    *   *Mismatch/Risk:* Flaggt die Mail zur manuellen Eskalation (Human-in-the-Loop), wenn Daten fehlen oder der Kunde unzufrieden wirkt.

## 🛠 Tech Stack
*   **Core:** Python 3.11
*   **API Framework:** FastAPI (Async)
*   **AI/LLM:** OpenAI API (Structured Outputs via Pydantic)
*   **Validation:** Pydantic (Strikte Typisierung für Input/Output)
*   **Config:** Pydantic-Settings (12-Factor App Prinzipien)

## 📂 Architektur

Das Projekt folgt einer strikten Trennung der Verantwortlichkeiten:

*   `src/agent`: Beinhaltet die LLM-Logik und Prompt-Templates. Nutzt `Structured Outputs`, um Halluzinationen zu minimieren und valides JSON für das Frontend zu garantieren.
*   `src/gateway`: Schnittstelle zu externen Datenquellen (Mockup für Webshop/ERP Scraper).
*   `src/main.py`: Orchestrierung der Services via FastAPI Webhooks.

## 🚀 Setup & Development

1.  **Environment:**
    ```bash
    cp .env.example .env
    # API Keys eintragen
    ```

2.  **Install:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run:**
    ```bash
    uvicorn src.main:app --reload
    ```

## ⚠️ Security Note
In diesem POC werden keine echten Patientendaten verarbeitet. Sensible Credentials (API Keys, Logins) werden ausschließlich über Environment Variables (`.env`) geladen und sind nicht im Code hardcodiert.