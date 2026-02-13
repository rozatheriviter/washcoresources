import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def main():
    # Start a local server
    server = subprocess.Popen(["python3", "-m", "http.server", "8000"])
    time.sleep(2)  # Give the server time to start

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("http://localhost:8000")

            # Wait for resources to render
            await page.wait_for_selector(".resource-card")

            # Scroll to see some cards
            await page.evaluate("window.scrollTo(0, 800)")
            await page.wait_for_timeout(1000)

            await page.screenshot(path="verification/resource_cards.png")

            # Count cards with website buttons
            website_buttons = await page.query_selector_all("a.btn-primary:has-text('Website')")
            print(f"Found {len(website_buttons)} cards with website buttons on screen/loaded.")

            await browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    asyncio.run(main())
