from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # We need to serve the files. Since we can't easily start a server in background in this turn
    # and expect it to persist (or it's complex), we will try to use file:// protocol.
    # However, Service Workers usually don't work on file://.
    # But we can verify the pages load and console has no errors.

    cwd = os.getcwd()

    files = ['index.html', 'about.html', 'submit-resource.html']

    for filename in files:
        url = f'file://{cwd}/{filename}'
        print(f"Checking {url}...")

        # Listen for console errors
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}") if msg.type == "error" else None)

        try:
            page.goto(url)
            page.wait_for_load_state('networkidle')
            print(f"Loaded {filename} successfully.")

            # Take screenshot
            page.screenshot(path=f'verification/{filename.replace(".html", "")}.png')

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
