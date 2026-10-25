🛒 Retail Product Annotation & Data Quality Analyzer

An end-to-end Python data workflow for retail product categorization, data-quality validation, SQL analysis, and automated Excel reporting.

📌 Project Overview

Retail businesses manage large product catalogues containing thousands of product names, descriptions, and categories. Before these datasets can be used for reporting, search, analytics, or machine-learning workflows, they need to be organized, labeled consistently, and checked for quality issues.

Manual categorization and validation can be repetitive, time-consuming, and prone to mistakes.

The Retail Product Annotation & Data Quality Analyzer addresses this problem through a reproducible Python pipeline that suggests product categories, identifies potentially problematic records, evaluates suggestions against a reference-label dataset, stores structured data in SQLite, and generates Excel reports for further inspection.

The project brings together practical data-processing techniques used in data annotation and data operations workflows.

Project scope: This is a rule-based data-processing prototype, not a trained machine-learning model. The sample catalogue is synthetic, and the supplied reference labels are provisional. Review the reference labels before presenting evaluation results as meaningful accuracy measurements.

🎯 Problem Statement

How can retail product datasets be categorized consistently and validated efficiently before being used for further analysis?

Product catalogues may contain missing names, duplicate records, unfamiliar product descriptions, and categories that require human verification. This project automates the initial categorization process and flags potential data-quality problems so that records needing attention can be reviewed systematically.

💡 Proposed Solution

Build a Python-based tool that:

Suggests retail categories using transparent, keyword-based rules.

Detects missing product names, duplicate records, and uncertain classifications.

Compares suggested categories against a reference set of labels.

Stores product and annotation records in a relational database.

Uses SQL to retrieve, validate, and summarize data.

Generates structured Excel, CSV, and JSON reports.

✨ Key Features

Feature

Description

Retail product annotation

Suggests categories for product names using configurable keyword rules.

Seven-category taxonomy

Supports Dairy, Snacks, Beverages, Personal Care, Household, Staples, and Other.

Data-quality validation

Flags blank product names, duplicate names, invalid categories, and uncertain classifications.

Reference-label evaluation

Compares suggested categories with reference labels associated with matching product IDs.

SQLite database

Stores products, annotations, and reference labels in related tables.

SQL analysis

Retrieves category counts, review queues, reference mismatches, and products without reference labels.

Excel reporting

Generates a multi-sheet workbook containing summaries, quality issues, and comparison results.

CSV and JSON exports

Produces structured outputs for inspection and additional data-processing tasks.

Automated tests

Tests important categorization, validation, evaluation, and database operations.

🏷️ Product Categories

The annotation system uses the following seven categories:

Category

Example product

Dairy

Amul Butter 500g

Snacks

Lays Magic Masala Chips

Beverages

Tata Tea Gold

Personal Care

Dettol Handwash

Household

Surf Excel Detergent Powder

Staples

Tata Salt 1kg

Other

Mystery Product XYZ

The rules are designed to consider the product type rather than simply matching an ingredient.

For example:

Coconut Milk Soap → Personal Care

Coconut Milk Beverage → Beverages

Protein Bar Chocolate → Snacks

Coconut Cooking Oil → Staples

If no rule matches, the system assigns Other as a provisional category and flags the product for review.

The categorization rules are defined in src/annotate.py, and category definitions and edge-case instructions are documented in data/annotation_guidelines.md.

🧭 End-to-End Workflow

flowchart TD
    A["Retail Product Dataset (CSV)"] --> B["Load Data with Pandas"]
    B --> C["Suggest Categories with Python Rules"]
    C --> D["Validate Product Records"]
    C --> E["Compare with Reference Labels"]
    D --> F["Store Data in SQLite"]
    E --> F
    F --> G["Execute SQL Quality Checks"]
    G --> H["Generate Excel, CSV and JSON Reports"]
    H --> I["Review Flagged Records"]

Workflow stages

1. Data ingestion

Read product IDs and product names from data/products.csv using Pandas.

2. Category suggestion

Apply keyword-based rules and explicit edge-case conditions to suggest one of the seven product categories. Record the matched rule or the reason the product needs review.

3. Data-quality validation

Check for blank product names, repeated product names, invalid categories, and unmatched or uncertain products. Flag the affected records rather than assuming every issue is a confirmed error.

4. Reference-label comparison

Compare suggested categories with the labels provided in data/gold_labels.csv. Calculate the match rate for products with matching IDs.

5. Database storage

Store product records, annotation results, and reference labels in a local SQLite database.

6. SQL analysis

Run SQL queries to retrieve category counts, identify review items, and compare suggested labels with reference labels.

7. Report generation

Export a multi-sheet Excel workbook, CSV files, and a JSON summary for inspection and further analysis.

The entire workflow is orchestrated by run_project.py, which calls the pipeline implemented in src/pipeline.py.

🧰 Technology Stack

Technology

Purpose

Python

Implements the processing pipeline, categorization rules, validation, and reporting.

Pandas

Reads CSV files, transforms tabular data, compares labels, and calculates summaries.

Regular Expressions

Matches product-name patterns and category keywords.

SQLite

Stores product records, annotations, and reference labels in a local database.

SQL

Filters, joins, groups, and validates database records.

openpyxl

Enables Excel workbook creation through Pandas.

unittest

Executes automated tests for key project functionality.

Git and GitHub

Support source-code version control and project sharing.

🗂️ Project Structure

Retail-Annotation-Analyzer/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── products.csv
│   ├── gold_labels.csv
│   └── annotation_guidelines.md
├── src/
│   ├── __init__.py
│   ├── annotate.py
│   ├── validate.py
│   ├── database.py
│   ├── pipeline.py
│   └── report.py
├── sql/
│   └── quality_checks.sql
├── tests/
│   └── test_project.py
├── run_project.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md

Main modules

File

Responsibility

run_project.py

Entry point for running the complete project.

src/annotate.py

Implements rule-based category suggestions.

src/validate.py

Performs data-quality checks and reference-label evaluation.

src/database.py

Creates SQLite tables, persists records, and executes SQL queries.

src/pipeline.py

Coordinates the end-to-end workflow.

src/report.py

Generates Excel, CSV, and JSON outputs.

sql/quality_checks.sql

Contains example SQL queries for data validation and analysis.

tests/test_project.py

Tests important annotation, validation, and database functions.

🚀 Installation and Setup

Prerequisites

Python 3.10 or newer

Git, if cloning the repository

VS Code or another code editor

Excel or a compatible spreadsheet application to inspect the generated workbook

Step 1: Clone the repository

git clone https://github.com/saipranav31/Retail-Annotation-Analyzer.git
cd Retail-Annotation-Analyzer

Alternatively, download the repository as a ZIP from GitHub and extract it.

Step 2: Create a virtual environment

Windows PowerShell

py -m venv .venv
.\.venv\Scripts\Activate.ps1

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate

Step 3: Install dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

Step 4: Run the project

python run_project.py

The pipeline processes the input data, saves records to SQLite, executes SQL analysis, and generates the output reports.

Step 5: Run the automated tests

python -m unittest discover -s tests -v

The tests cover product-type edge cases, missing-name detection, duplicate-name detection, reference evaluation, and SQLite persistence.

Windows troubleshooting: Close reports/quality_report.xlsx in Excel before rerunning the pipeline. Excel may lock the workbook and prevent Python from overwriting it.

📥 Input Data

data/products.csv

Contains 200 synthetic sample product records.

Column

Description

item_id

Unique identifier used to link records across files and database tables.

product_name

Product name used by the categorization rules.

The sample dataset deliberately includes a small number of blank, repeated, ambiguous, and unmatched product names so that the validation process can be demonstrated.

This is educational sample data, not a verified commercial retail catalogue.

data/gold_labels.csv

Contains reference categories for selected product IDs.

These reference labels allow the program to compare its category suggestions with expected answers. They must be checked against the written annotation guidelines before using the resulting match rate as a meaningful evaluation metric.

data/annotation_guidelines.md

Defines the categories, their intended meanings, and rules for handling difficult products consistently.

🗄️ Database Design

The project uses SQLite to maintain three related tables.

Table

Purpose

Main columns

items

Stores source product records.

item_id, product_name

annotations

Stores category suggestions and review information.

item_id, suggested_label, needs_review, review_reason

gold

Stores reference labels used for comparison.

item_id, gold_label

The shared item_id allows product details, suggested labels, and reference labels to be connected through SQL queries.

The database is generated locally at:

database/retail_annotation.db

It is reproducible and does not need to be committed to GitHub.

💻 Example SQL Queries

1. Count products in each suggested category

SELECT
    suggested_label,
    COUNT(*) AS product_count
FROM annotations
GROUP BY suggested_label
ORDER BY product_count DESC;

2. Retrieve records requiring manual review

SELECT
    i.item_id,
    i.product_name,
    a.suggested_label,
    a.review_reason
FROM items AS i
JOIN annotations AS a
    ON a.item_id = i.item_id
WHERE a.needs_review = 1
ORDER BY i.item_id;

3. Compare suggested categories with reference labels

SELECT
    i.item_id,
    i.product_name,
    a.suggested_label,
    g.gold_label,
    CASE
        WHEN a.suggested_label = g.gold_label
            THEN 'MATCH'
        ELSE 'MISMATCH'
    END AS comparison_result
FROM items AS i
JOIN annotations AS a
    ON a.item_id = i.item_id
JOIN gold AS g
    ON g.item_id = i.item_id;

Additional SQL quality checks are available in sql/quality_checks.sql.

📊 Generated Reports

After running the pipeline, the following files are produced.

Output

Description

database/retail_annotation.db

SQLite database containing product, annotation, and reference-label records.

reports/quality_report.xlsx

Multi-sheet workbook containing summaries, category distributions, validation issues, and reference comparisons.

reports/final_labels.csv

Provisional labels, review status, and a field intended for human-approved labels.

reports/validation_issues.csv

Records flagged by the validation checks.

reports/summary.json

Machine-readable summary metrics.

Excel workbook contents

The workbook includes:

Summary: Overall dataset and reference-comparison metrics.

Category Summary: Product counts by suggested category.

Data Quality: Rows flagged for review and the associated reasons.

Reference Mismatches: Reference items where suggestions differ from the supplied labels.

Reference Confusion: A cross-tabulation of reference and suggested categories.

Final Labels: Provisional labels and fields intended for manual review.

SQL result sheets: Results from selected SQL queries.

The manual_reviewed_label field is intentionally left blank until a human reviews and approves a label. The program does not claim those records have already been manually verified.

📏 Evaluation and Quality Considerations

The pipeline calculates a reference-set match rate by comparing suggested categories with the labels in the supplied reference file.

For example, if 37 out of 40 reference labels match the program's suggestions:

[
\text{Match Rate} = \frac{37}{40} \times 100 = 92.5%
]

This percentage only describes agreement with the supplied reference file. It is not proof of real-world accuracy, particularly while the reference labels remain unverified.

Before presenting an evaluation result:

Review and verify the reference labels against the annotation guidelines.

Examine the mismatches and document their causes.

Keep reference labels independent from the rules being evaluated wherever possible.

Report the reference-set size alongside the match rate.

A record flagged for review is a potential issue, not necessarily a confirmed annotation error. Likewise, duplicate product names may represent repeated records or legitimate product variants.

⚠️ Limitations

The categorization system uses predefined keyword rules rather than a trained machine-learning model.

Keyword matching may miss synonyms, spelling variations, context, or unfamiliar product descriptions.

A rule match is not a calibrated confidence probability.

Other is a provisional fallback, not a guarantee that the category is correct.

Duplicate names are flagged for review rather than automatically removed.

Reference labels require human verification.

The current workflow does not include a web interface or multi-annotator management.

It does not calculate Cohen's kappa, inter-annotator agreement, or annotator speed.

🔭 Future Improvements

Possible extensions include:

Expanding and configuring category rules using reviewed examples.

Adding a human-review workflow that saves approved labels and reviewer comments.

Evaluating on a larger, appropriately licensed dataset with independently verified labels.

Reporting category-specific precision and recall after verifying the reference labels.

Adding a lightweight interface for reviewing and correcting product categories.

Supporting larger datasets and additional retail taxonomies.



🗣️ Project Explanation

I developed a Retail Product Annotation and Data Quality Analyzer using Python, Pandas, SQL, SQLite, and Excel. The system reads retail product names, suggests one of seven categories using keyword-based rules, flags missing and duplicate records, and compares suggestions against a reference-label file. I use SQLite to store structured records, SQL queries to analyze the data, and Python libraries to generate an Excel quality report. This project helped me practice data annotation, validation, Python automation, database operations, and reporting.


Built as a practical learning project focused on retail data operations, annotation workflows, and data quality.
