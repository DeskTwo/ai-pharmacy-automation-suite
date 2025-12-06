# src/gateway/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from src.gateway.scraper import scraper_instance
from src.gateway.config import get_settings
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway.api")

app = FastAPI(
    title=get_settings().APP_NAME,
    description="Interface for Cannaleo Browser Automation",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Start browser on API launch to be ready."""
    logger.info("Gateway starting up...")
    # Optional: Warmup browser
    # await scraper_instance.start_session()

@app.on_event("shutdown")
async def shutdown_event():
    await scraper_instance.close()

@app.get("/health")
async def health_check():
    return {"status": "online", "browser": "ready" if scraper_instance.browser else "standby"}

@app.get("/orders")
async def fetch_orders(status: str = "new"):
    """Trigger scraping of orders."""
    try:
        orders = await scraper_instance.get_orders(status_filter=status)
        return {"count": len(orders), "data": orders}
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders/{order_id}/process")
async def process_order(order_id: str, background_tasks: BackgroundTasks):
    """
    Example of async processing: Triggers detail scraping in background
    and returns immediately to not block the caller.
    """
    # background_tasks.add_task(scraper_instance.scrape_details, order_id)
    return {"message": "Processing started", "order_id": order_id}