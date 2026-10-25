"""Orchestrates annotation, validation, SQLite storage, and reporting."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from .annotate import annotate_dataframe
from .validate import validate_products, evaluate_gold
from .database import build_database, run_sql_query
from .report import build_reports

ROOT = Path(__file__).resolve().parents[1]

def run_pipeline(root: str | Path = ROOT) -> dict:
    root = Path(root)
    products_path = root / "data" / "products.csv"
    gold_path = root / "data" / "gold_labels.csv"
    db_path = root / "database" / "retail_annotation.db"
    reports_path = root / "reports"

    products = pd.read_csv(products_path, keep_default_na=False)
    # Keep blank strings as blanks, so they can be flagged by validation.
    annotated = annotate_dataframe(products)
    validated = validate_products(annotated)
    gold = pd.read_csv(gold_path, keep_default_na=False)
    gold_eval, gold_metrics = evaluate_gold(annotated, gold)

    total = int(len(validated))
    nonblank = validated.loc[~validated["is_missing_name"], "product_name_clean"]
    metrics = {
        "total_records": total,
        "unique_nonblank_names": int(nonblank.nunique()),
        "blank_names": int(validated["is_missing_name"].sum()),
        "duplicate_name_records": int(validated["is_duplicate_name"].sum()),
        "records_needing_review": int(validated["needs_review"].sum()),
        "reference_items": gold_metrics["reference_items"],
        "reference_matches": gold_metrics["matches"],
        "reference_accuracy_pct": gold_metrics["accuracy_pct"],
        "note": "Rule-based suggestion match rate against a provisional reference set; manually verify gold labels before presenting as an accuracy claim."
    }

    build_database(db_path, validated, gold)

    queries = {
        "SQL Category Counts": """
            SELECT suggested_label AS category, COUNT(*) AS product_count
            FROM annotations GROUP BY suggested_label ORDER BY product_count DESC
        """,
        "SQL Review Queue": """
            SELECT i.item_id, i.product_name, a.suggested_label, a.review_reason
            FROM items i JOIN annotations a ON i.item_id = a.item_id
            WHERE a.needs_review = 1 ORDER BY i.item_id
        """,
        "SQL Reference Check": """
            SELECT i.item_id, i.product_name, a.suggested_label, g.gold_label,
                   CASE WHEN a.suggested_label = g.gold_label THEN 'MATCH' ELSE 'MISMATCH' END AS result
            FROM items i JOIN annotations a ON i.item_id = a.item_id
            JOIN gold g ON i.item_id = g.item_id ORDER BY i.item_id
        """,
        "SQL Missing Gold": """
            SELECT i.item_id, i.product_name FROM items i
            LEFT JOIN gold g ON i.item_id = g.item_id WHERE g.item_id IS NULL
        """
    }
    sql_results = {name: run_sql_query(db_path, query) for name, query in queries.items()}
    build_reports(reports_path, validated, gold_eval, metrics, sql_results)
    return metrics
