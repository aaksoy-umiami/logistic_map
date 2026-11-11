"""Visit the live app in a headless browser, so that Streamlit does not put it
to sleep.

Streamlit Community Cloud puts an app to sleep after 12 hours without a visit,
and the next visitor has to press a button and wait for it to start.  This
script opens the app as a visitor's browser would.  If it finds the app
asleep, it presses the wake-up button.  It then waits for the app's own header
to be on the page, and fails if the header does not appear, so that a failed
run sends a notification.

It is run every 6 hours by .github/workflows/keep_awake.yml.  To run it by
hand:

    pip install playwright
    python -m playwright install --only-shell chromium
    python .github/scripts/keep_awake.py
"""

import sys
import time

from playwright.sync_api import sync_playwright

APP_URL = "https://logistic-map.streamlit.app"
APP_HEADER = "Logistic Map Simulator"        # the app's header (utils/ui.py)
WAKE_BUTTON = "Yes, get this app back up!"   # on Streamlit's page for a sleeping app
WAIT_SECONDS = 300                           # a sleeping app can take minutes to start
STAY_SECONDS = 10                            # stay a moment once the app is up


def header_is_shown(page) -> bool:
    """Whether the app's header is visible.  The app runs in a frame of the
    page, so every frame is searched."""
    for frame in page.frames:
        try:
            header = frame.get_by_text(APP_HEADER)
            if header.count() > 0 and header.first.is_visible():
                return True
        except Exception:
            pass                             # a frame that went away while loading
    return False


def main(url: str) -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        was_asleep = False
        deadline = time.monotonic() + WAIT_SECONDS
        while time.monotonic() < deadline:
            if header_is_shown(page):
                page.wait_for_timeout(STAY_SECONDS * 1000)
                print(f"{url} " + ("was asleep and is awake now." if was_asleep else "is awake."))
                browser.close()
                return 0
            button = page.get_by_role("button", name=WAKE_BUTTON)
            if not was_asleep and button.count() > 0:
                button.first.click()
                was_asleep = True
                print(f"{url} was asleep; pressed the wake-up button.")
            page.wait_for_timeout(2000)
        print(f"{url}: the app's header did not appear within {WAIT_SECONDS} seconds.")
        browser.close()
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else APP_URL))
