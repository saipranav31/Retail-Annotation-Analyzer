# Retail Product Annotation & Data Quality Analyzer

A small, solo-built project that demonstrates retail product annotation, data validation, SQL querying, and Excel reporting using Python, pandas, SQLite, and openpyxl.

## What it does

1. Loads retail product names from `data/products.csv`.
2. Applies transparent keyword-based rules to suggest one of seven categories.
3. Flags blank names, duplicate product names, and low-confidence/unmatched items for manual review.
4. Compares the manually verified reference labels in `data/gold_labels.csv` with predictions on matching products.
5. Saves products, annotations, reference labels, and review outcomes to SQLite.
6. Executes SQL quality checks and exports a multi-sheet Excel report.

**Important:** This is a rule-based demonstration, not a trained machine-learning model. The generated sample data and labels are synthetic. The reported reference-set accuracy is meaningful only after you review and confirm the gold labels. Do not claim multi-annotator agreement: this is a solo project.

## Requirements

- Python 3.10 or newer
- VS Code (recommended, but not required)
- Internet is not required after Python and dependencies are installed

## Quick start (Windows PowerShell)

Open this project folder in VS Code, then open Terminal > New Terminal.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python run_project.py
```

If PowerShell blocks activation, you can run commands without activating the environment:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_project.py
```

## Quick start (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python run_project.py
```

## Outputs

After running, inspect:
- `database/retail_annotation.db` — SQLite database
- `reports/quality_report.xlsx` — summary, scorecard, disagreements, data quality, confusion matrix, final labels
- `reports/summary.json` — machine-readable metrics
- `reports/final_labels.csv` — final label output
- `reports/validation_issues.csv` — flagged rows

## Project workflow

```text
Product CSV -> Rule-based category suggestions -> Validation/review flags
            -> Reference-label evaluation -> SQLite -> SQL checks -> Excel report
```

## Data files

- `data/products.csv`: 200 synthetic retail product records. It intentionally includes some duplicate names, blank names, and ambiguous products so validation checks can be demonstrated.
- `data/gold_labels.csv`: a reference set for selected product IDs. Treat these labels as provisional until you manually review them against the guidelines.
- `data/annotation_guidelines.md`: category definitions and edge-case rules.

The product list is synthetic and is intended for demonstration. Replace it with an appropriately licensed dataset or your own verified list before presenting it as real-world data.

## How to customize

Edit category rules in `src/annotate.py` and add more product names to `data/products.csv`. If a product is ambiguous or no rule matches, the tool assigns `Other` with a review flag. Rule order matters, so specific rules should appear before broad ones.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Suggested resume bullet (use only after running and verifying)

**Retail Product Annotation & Data Quality Analyzer | Python, Pandas, SQL, SQLite, Excel**
- Built a Python pipeline to suggest retail product categories and flag missing, duplicate, and uncertain records for review.
- Stored product and annotation records in SQLite and wrote SQL checks for data validation.
- Generated an Excel quality report with category summaries, reference-set evaluation, and review queues.

Add only metrics you have personally verified from the generated reports. Explain that category suggestions are keyword-rule-based, not model predictions.
