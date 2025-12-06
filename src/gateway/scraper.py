# src/gateway/scraper.py
import logging
import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext
from src.gateway.config import get_settings

settings = get_settings()
logger = logging.getLogger("gateway.scraper")

class CannaleoScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    async def start_session(self):
        """Initializes the browser session and performs login."""
        logger.info("Starting Browser Session...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=settings.HEADLESS)
        
        self.context = await self.browser.new_context(
            user_agent=settings.USER_AGENT,
            accept_downloads=True
        )
        self.page = await self.context.new_page()
        
        try:
            await self._login()
        except Exception as e:
            logger.error(f"Login failed: {e}")
            await self.close()
            raise

    async def _login(self):
        """Internal login logic handling specific Cannaleo selectors."""
        logger.info(f"Navigating to login for user: {settings.CANNALEO_USER}")
        await self.page.goto("https://apo-cannaleo.de/login") # URL anpassen falls nötig
        
        # Check if already logged in (Cookie persistence could be added here)
        if await self.page.is_visible("text=Logout"):
            logger.info("Session already active.")
            return

        # Fill credentials
        await self.page.fill('input[name="email"]', settings.CANNALEO_USER)
        await self.page.fill('input[name="password"]', settings.CANNALEO_PASS)
        await self.page.click('button[type="submit"]')
        
        # Wait for dashboard (Proof of Login)
        await self.page.wait_for_selector(".dashboard-container", timeout=15000)
        logger.info("Login successful.")

    async def get_orders(self, status_filter: str = "new"):
        """Scrapes the order grid based on status."""
        if not self.page:
            await self.start_session()
            
        logger.info(f"Scraping orders with status: {status_filter}")
        await self.page.goto(f"https://apo-cannaleo.de/orders?status={status_filter}")
        
        # Wait for Grid
        await self.page.wait_for_selector("table.order-list")
        
        # Extract Data (Simplified for Demo)
        orders = await self.page.evaluate("""() => {
            const rows = Array.from(document.querySelectorAll('table.order-list tr.order-row'));
            return rows.map(row => ({
                id: row.dataset.id,
                patient: row.querySelector('.patient-name').innerText,
                status: row.querySelector('.status-badge').innerText
            }));
        }""")
        
        logger.info(f"Found {len(orders)} orders.")
        return orders

    async def close(self):
        """Clean shutdown."""
        if self.context: await self.context.close()
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()
        logger.info("Browser session closed.")

# Singleton Instance to be used in API
scraper_instance = CannaleoScraper()