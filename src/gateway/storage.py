# src/gateway/storage.py

class OrderStorage:
    """
    Simuliert eine Datenbank-Verbindung. 
    Aktuell speichert dies nichts dauerhaft (In-Memory),
    aber hier würden wir später Redis oder SQL anbinden.
    """
    def __init__(self):
        self._memory_db = {}

    async def get_order_status(self, order_id: str) -> dict:
        # Platzhalter: Gibt später echte Daten zurück
        return self._memory_db.get(order_id)

    async def save_interaction(self, order_id: str, summary: str):
        # Platzhalter: Speichert, was der Agent getan hat
        print(f"[DB LOG] Saving interaction for Order {order_id}: {summary}")
        self._memory_db[order_id] = summary