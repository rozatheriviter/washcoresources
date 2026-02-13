import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        # Test Home Page
        print("Navigating to index.html...")
        await page.goto("http://localhost:8001/index.html")
        try:
            await page.wait_for_selector(".resource-card", timeout=10000)
            print("Successfully loaded resources.")

            # Check if Website button exists
            website_btn = page.locator(".btn-primary:has-text('Website')")
            count = await website_btn.count()
            print(f"Found {count} website buttons on index page.")

            await page.screenshot(path="verification/index_updated_v2.png")
        except Exception as e:
            print(f"Failed to load resources: {e}")
            await page.screenshot(path="verification/index_failed_v2.png")

        # Test Map Page
        print("Navigating to map.html...")
        await page.goto("http://localhost:8001/map.html")
        try:
            await page.wait_for_selector(".leaflet-marker-icon", timeout=10000)
            markers = page.locator(".leaflet-marker-icon")
            marker_count = await markers.count()
            print(f"Found {marker_count} markers on map.")

            found_popup_website = False
            for i in range(min(15, marker_count)):
                await markers.nth(i).click(force=True)
                await asyncio.sleep(0.5)
                popup_website_link = page.locator(".leaflet-popup-content a:has-text('Website')")
                if await popup_website_link.count() > 0:
                    print(f"Found website link in map popup for marker {i}.")
                    found_popup_website = True
                    await page.screenshot(path="verification/map_popup_updated_v2.png")
                    break
                await page.mouse.click(0, 0)

            if not found_popup_website:
                print("No website link found in sample.")
        except Exception as e:
            print(f"Failed to load map: {e}")
            await page.screenshot(path="verification/map_failed_v2.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
