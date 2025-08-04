from pathlib import Path
from playwright.sync_api import sync_playwright

# takes a full-page screenshot of the site and saves it to out_path
def capture_homepage(url: str, out_path: Path, viewport=(1280, 800)) -> None:

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=str(out_path), full_page=True, type="png")
        browser.close()