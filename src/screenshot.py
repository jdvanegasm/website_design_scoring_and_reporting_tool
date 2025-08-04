from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

from config_loader import cfg
C = cfg().get("screenshot", {})


def capture_homepage(url: str, out_path: Path, viewport: tuple[int, int] | None = None) -> None:
    """
    takes a full-page screenshot of the site and saves it to out_path
    mod: wait for load state and buffer for lazy js after full scroll
    i think that maybe it could need more changes for each sidecase, but for now it works
    """
    viewport = tuple(viewport or C.get("viewport", [1280, 800]))

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})

        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state(
                "networkidle",
                timeout=C.get("networkidle_timeout_ms", 10_000)
            )
        except PWTimeout:
            page.wait_for_timeout(3000)

        page.wait_for_timeout(C.get("buffer_ms", 1500))

        try:
            page.wait_for_selector("footer", timeout=3000)
        except Exception:
            pass

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(C.get("scroll_delay_ms", 500))
        page.evaluate("window.scrollTo(0, 0)")

        page.screenshot(
            path=str(out_path),
            full_page=True,
            type="png",
            omit_background=False
        )
        browser.close()