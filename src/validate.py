"""Dataset validation and reference-label evaluation."""
from __future__ import annotations
import pandas as pd
from .annotate import CATEGORIES

def validate_products(annotated: pd.DataFrame) -> pd.DataFrame:
    out = annotated.copy()
    out["product_name_clean"] = out["product_name"].fillna("").astype(str).str.strip()
    out["is_missing_name"] = out["product_name_clean"].eq("")
    normalized = out["product_name_clean"].str.casefold()
    out["is_duplicate_name"] = normalized.ne("") & normalized.duplicated(keep=False)
    out["is_valid_label"] = out["suggested_label"].isin(CATEGORIES)
    out["needs_review"] = (
        out["is_missing_name"] |
        out["is_duplicate_name"] |
        ~out["is_valid_label"] |
        out["confidence_status"].eq("Review")
    )
    reasons = []
    for _, row in out.iterrows():
        row_reasons = []
        if row["is_missing_name"]:
            row_reasons.append("Missing product name")
        if row["is_duplicate_name"]:
            row_reasons.append("Duplicate product name")
        if not row["is_valid_label"]:
            row_reasons.append("Invalid category")
        if row["confidence_status"] == "Review":
            row_reasons.append("Manual category review")
        reasons.append("; ".join(row_reasons))
    out["review_reason"] = reasons
    return out

def evaluate_gold(annotated: pd.DataFrame, gold: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    required = {"item_id", "gold_label"}
    missing = required - set(gold.columns)
    if missing:
        raise ValueError(f"Gold file is missing required columns: {sorted(missing)}")
    joined = annotated.merge(gold[["item_id", "gold_label"]], on="item_id", how="inner")
    if joined.empty:
        joined["matches_gold"] = pd.Series(dtype=bool)
        return joined, {"reference_items": 0, "matches": 0, "accuracy_pct": None}
    joined["matches_gold"] = joined["suggested_label"] == joined["gold_label"]
    matches = int(joined["matches_gold"].sum())
    total = int(len(joined))
    return joined, {
        "reference_items": total,
        "matches": matches,
        "accuracy_pct": round(matches / total * 100, 2)
    }
