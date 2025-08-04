from pathlib import Path
def generate_reports(url, shot, score, breakdown, metrics, out_dir: Path):
    pdf = out_dir / "report.pdf"
    html = out_dir / "report.html"
    md  = out_dir / "report.md"
    for p in (pdf, html, md):
        p.write_text("TODO")
    return pdf, html, md