import asyncio
from playwright.async_api import async_playwright
import http.server
import threading
import os

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server():
    os.chdir('/home/jules')
    with http.server.HTTPServer(("", 8001), Handler) as httpd:
        httpd.serve_forever()

async def verify():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    await asyncio.sleep(2) # Wait for server to start

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Test Home Page
        await page.goto("http://localhost:8001/index.html")
        await page.wait_for_selector(".resource-card")

        # Check if Website button exists
        website_btn = page.locator(".btn-primary:has-text('Website')")
        count = await website_btn.count()
        print(f"Found {count} website buttons on index page.")

        await page.screenshot(path="verification/index_updated.png")

        # Test Map Page
        await page.goto("http://localhost:8001/map.html")
        await page.wait_for_selector(".leaflet-marker-icon")

        # Click markers until we find a website link
        markers = page.locator(".leaflet-marker-icon")
        marker_count = await markers.count()
        print(f"Found {marker_count} markers on map.")

        found_popup_website = False
        for i in range(min(15, marker_count)):
            await markers.nth(i).click(force=True)
            await page.wait_for_selector(".leaflet-popup-content", timeout=2000)
            popup_website_link = page.locator(".leaflet-popup-content a:has-text('Website')")
            if await popup_website_link.count() > 0:
                print(f"Found website link in map popup for marker {i}.")
                found_popup_website = True
                await page.screenshot(path="verification/map_popup_updated.png")
                break
            # Click elsewhere to close popup
            await page.mouse.click(0, 0)

        if not found_popup_website:
            print("ERROR: No website link found in any of the first 15 map popups!")
            await page.screenshot(path="verification/map_popup_failed.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
