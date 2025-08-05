# Website Design Scoring and Reporting Tool

An automated Python solution to assess the visual design of websites using screenshots. The tool analyzes key design principles such as whitespace usage, contrast, color harmony, and text density, and returns a normalized score per metric. Outputs include PDF, HTML, and Markdown reports with screenshots, ready to be shared or logged.

>  **Designed for Linux systems but compatible with other OS**. Integrates with Google Drive and Google Sheets for cloud-based reporting and logging.

---

## Features

- Automated screenshot capture of website homepages
- Visual design evaluation using OpenCV and image analysis
- Metrics:
  - **Whitespace ratio**
  - **Contrast**
  - **Color harmony**
  - **Text density**
- Exports results to:
  - Markdown (`.md`)
  - HTML (`.html`)
  - PDF (`.pdf`)
- Optional: Uploads results to Google Drive and logs metrics to Google Sheets

---

## Project Structure

```

.  
├── src/  
│ ├── analyzer/ # Core image analysis functions  
│ ├── output/ # Generated reports and screenshots  
│ └── utils/ # Helper functions (color analysis, scoring, etc.)  
├── config.yaml # Configuration for API keys and runtime behavior  
├── requirements.txt # Python dependencies  
├── README.md # This file

```

---

## Installation

1. Clone the repository:
```bash
git clone
git@github.com:jdvanegasm/website_design_scoring_and_reporting_tool.git
cd website_design_scoring_and_reporting_tool
```

2. Create and activate a virtual environment:
    
    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    ```
    
3. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    

---

## Usage

1. Run in your terminal (inside src/):
``` bash
python main.py https://your_website -o output
```

---

## Metric Overview

|Metric|Description|Ideal Range|
|---|---|---|
|Whitespace|Proportion of blank space; improves readability and clarity|~60–70%|
|Contrast|Intensity difference between elements|High|
|Color Harmony|Aesthetic coherence between dominant colors|High|
|Text Density|Balance between content and clarity (via edge detection)|Moderate|

---

## Configuration

You can modify `config.yaml` to adjust behavior, enable Drive/Sheets logging, set scoring weights, etc.

---

## License

This project is licensed under the **GPL-3.0 License**. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for more details.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or extend.

---

## Contact

Developed by [@jdvanegasm](https://github.com/jdvanegasm) as part of a test for automation and visual analysis tooling.
