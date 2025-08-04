"""
gh: jdvanegasm

website Design Scoring Tool.

how to:
    python -m src.main https://example.com -o output
"""

from pathlib import Path
import argparse
import datetime as dt

# stubs
from screenshot import capture_homepage
from analyzer import analyze_design
from scorer import score_design
from report import generate_reports
from integrations import push_to_drive_and_sheet


def run(url: str, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    # screenshot
    shot_path = out_dir / f"screenshot_{timestamp}.png"
    capture_homepage(url, shot_path)

    # analysis (stub returns dummy data for now)
    metrics = analyze_design(shot_path)

    # score
    score, breakdown = score_design(metrics)

    # reports in html, md, pdf
    pdf_path, html_path, md_path = generate_reports(
        url, shot_path, score, breakdown, metrics, out_dir
    )

    # cloud push (screenshot + reports)
    push_to_drive_and_sheet(
        url=url,
        score=score,
        breakdown=breakdown,
        screenshot_path=shot_path,
        report_paths=[pdf_path, md_path, html_path],
    )

    print(f"finished, doc saved to {pdf_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="design scoring tool")
    parser.add_argument("url", help="target website url")
    parser.add_argument(
        "-o", "--output", default="output", type=Path,
        help="directory where information will be stored"
    )
    args = parser.parse_args()
    run(args.url, args.output)