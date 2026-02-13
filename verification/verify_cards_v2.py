import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def main():
    server = subprocess.Popen(["python3", "-m", "http.server", "8000"])
    time.sleep(2)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1280, 'height': 2000})
            await page.goto("http://localhost:8000")
            await page.wait_for_selector(".resource-card")

            # Scroll to make sure cards are rendered and visible
            await page.evaluate("window.scrollTo(0, 1000)")
            await page.wait_for_timeout(1000)

            await page.screenshot(path="verification/resource_cards_v2.png")
            await browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    asyncio.run(main())
