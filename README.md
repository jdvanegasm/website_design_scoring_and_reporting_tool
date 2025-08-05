# Website Design Scoring & Reporting Tool

Automatically capture a homepage, analyse its visual design, and publish share-ready reports.  
Runs end-to-end on Python 3 (Linux-friendly, cross-platform) and—optionally—pushes artefacts to **Google Drive** while logging scores to **Google Sheets**.

> **Why?** Get an at-a-glance health check of typography, colour usage, layout balance, and overall polish—handy for designers, QA teams, and CRO audits.

---

## Features

| Category | Details |
|----------|---------|
| **Capture** | Headless Chromium via Playwright; full-page PNG at 1280 × 800. |
| **Analysis** | OpenCV + NumPy heuristics:<br>• Whitespace ratio<br>• Global contrast<br>• Palette harmony (k-means)<br>• Text density (edge map) |
| **Scoring** | Weighted 0-100 (+ breakdown table). Weights editable in **`config.yaml`**. |
| **Reporting** | • HTML (styled)<br>• PDF (WeasyPrint)<br>• Markdown (Git-friendly)<br>Each embeds the screenshot + tips. |
| **Cloud** | *(opt-in)* Upload screenshot & reports to Drive 📂, append row to Sheets 📋. |
| **CLI** | `python -m src.main <url> -o <output_dir>` |

---

## 🗂 Project Layout

```

website_design_scoring_and_reporting_tool/  
├── src/  
│ ├── analyzer.py # metrics  
│ ├── screenshot.py # Playwright capture  
│ ├── scorer.py # weighted total  
│ ├── report.py # HTML → PDF / MD  
│ └── integrations.py # Drive + Sheets  
├── secrets/ # ← OAuth / SA credentials (git-ignored)  
├── config.yaml  
├── requirements.txt  
└── README.md

````

---

## Installation

```bash
git clone https://github.com/jdvanegasm/website_design_scoring_and_reporting_tool.git
cd website_design_scoring_and_reporting_tool

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
````

---

## Quick Start

```bash
# from repo root
python -m src.main https://example.com -o output/
# → output/report.{pdf,html,md}, screenshot_*.png
```

---

## Google Drive / Sheets Integration (optional)

|Step|What to do|
|---|---|
|**1. Enable APIs**|In Google Cloud Console enable **Drive API** and **Sheets API** for your project.|
|**2. Credentials**|- **Option A**: Service-account JSON (requires Workspace + shared drive).- **Option B**: OAuth “Desktop” client (`client_secret.json`). First run opens a browser to grant access and stores `token.json` automatically.|
|**3. IDs**|Copy the **folder ID** (`https://drive.google.com/drive/folders/<ID>`) and **sheet ID** (`https://docs.google.com/spreadsheets/d/<ID>/…`).|
|**4. Edit `config.yaml`**|`yaml<br>google:<br> service_account_json: "secrets/client_secret.json"<br> drive_folder_id: "1AbC...DriveID"<br> sheet_id: "1XyZ...SheetID"<br>`|
|**5. Run again**|The tool uploads files to the folder and appends a new row (`timestamp|

All credential files live in **`secrets/`** and are ignored by Git (`.gitignore`).

---

## Configuration Highlights

```yaml
weights:
  whitespace: 0.20
  contrast:   0.30
  color_harmony: 0.30
  text_density: 0.20   # tweak to reflect your priorities

analyzer:
  whitespace_tol: 245          # RGB > tol counts as “white”
  contrast_percentiles: [5,95] # change for dark sites
```

---

## Metric Cheat-Sheet

|Metric|Good ≈|Why it matters|
|---|---|---|
|Whitespace|≥ 60 %|Gives breathing room & focus|
|Contrast|≥ 70 %|Aids legibility / accessibility|
|Color harmony|≥ 80 %|Cohesive, professional feel|
|Text density|10–20 %|Balanced information vs. clutter|

---

## Contributing

PRs are welcome—open an issue for large proposals first.  
Please run `black` and `pytest` before pushing.

---

## License

GPL-3.0 – see `LICENSE`.

---

> _Made with 🐍  by [@jdvanegasm](https://github.com/jdvanegasm)._ Enjoy scoring!