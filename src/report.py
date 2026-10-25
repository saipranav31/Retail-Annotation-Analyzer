"""Excel and CSV report generation."""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd

def build_reports(output_dir: str | Path, validated: pd.DataFrame, gold_eval: pd.DataFrame,
                  metrics: dict, sql_results: dict) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    category_summary = (
        validated["suggested_label"].value_counts(dropna=False)
        .rename_axis("category").reset_index(name="product_count")
    )
    review_rows = validated[validated["needs_review"]].copy()
    disagreements = gold_eval[~gold_eval["matches_gold"]].copy() if not gold_eval.empty else gold_eval.copy()
    confusion = pd.crosstab(
        gold_eval["gold_label"], gold_eval["suggested_label"],
        rownames=["reference_label"], colnames=["suggested_label"]
    ) if not gold_eval.empty else pd.DataFrame()

    final = validated[["item_id", "product_name", "suggested_label", "confidence_status",
                       "needs_review", "review_reason"]].copy()
    final = final.rename(columns={"suggested_label": "provisional_final_label"})
    final["manual_reviewed_label"] = ""
    final["review_status"] = final["needs_review"].map({True: "Needs review", False: "Rule checks passed"})
    final.to_csv(output_dir / "final_labels.csv", index=False)
    review_rows.to_csv(output_dir / "validation_issues.csv", index=False)

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    summary_df = pd.DataFrame([
        ("Total product records", metrics["total_records"]),
        ("Unique nonblank product names", metrics["unique_nonblank_names"]),
        ("Blank product names", metrics["blank_names"]),
        ("Records with duplicate product names", metrics["duplicate_name_records"]),
        ("Records flagged for review", metrics["records_needing_review"]),
        ("Reference-set items", metrics["reference_items"]),
        ("Rule suggestions matching reference labels", metrics["reference_matches"]),
        ("Reference-set match rate (%)", metrics["reference_accuracy_pct"]),
    ], columns=["metric", "value"])

    with pd.ExcelWriter(output_dir / "quality_report.xlsx", engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        category_summary.to_excel(writer, sheet_name="Category Summary", index=False)
        review_rows.to_excel(writer, sheet_name="Data Quality", index=False)
        disagreements.to_excel(writer, sheet_name="Reference Mismatches", index=False)
        confusion.to_excel(writer, sheet_name="Reference Confusion")
        final.to_excel(writer, sheet_name="Final Labels", index=False)
        for name, df in sql_results.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)

        # Basic usability formatting
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for column_cells in ws.columns:
                max_len = max((len(str(c.value)) if c.value is not None else 0) for c in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = min(max(max_len + 2, 12), 48)
