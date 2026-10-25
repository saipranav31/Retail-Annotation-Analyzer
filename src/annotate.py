"""Rule-based retail product category suggestions."""
from __future__ import annotations
import re
import pandas as pd

CATEGORIES = [
    "Dairy", "Snacks", "Beverages", "Personal Care",
    "Household", "Staples", "Other"
]

# Specific rules should appear before broad rules.
RULES = [
    ("Personal Care", [r"\bsoap\b", r"\bshampoo\b", r"\btoothpaste\b", r"\btoothbrush\b",
                       r"\bhandwash\b", r"\bhand sanitizer\b", r"\bface wash\b", r"\bface moisturizer\b",
                       r"\bbody lotion\b", r"\bdeodorant\b", r"\bsanitary pads?\b", r"\bbaby diapers?\b",
                       r"\bbaby wipes\b", r"\bshaving cream\b", r"\blip balm\b", r"\bsunscreen\b",
                       r"\bhair conditioner\b", r"\bhair oil\b", r"\bpet shampoo\b", r"\btoner\b"]),
    ("Dairy", [r"\bmilk\b", r"\bbutter\b", r"\bcheese\b", r"\bcurd\b", r"\byogurt\b",
               r"\bpaneer\b", r"\bghee\b", r"\bcream\b", r"\bbuttermilk\b", r"\blassi\b"]),
    ("Snacks", [r"\bchips\b", r"\bbiscuits?\b", r"\bcookies?\b", r"\bchocolate\b", r"\bcandy\b",
                r"\bnamkeen\b", r"\bpopcorn\b", r"\bprotein bar\b", r"\bcrackers?\b", r"\bchikki\b",
                r"\bmakhana\b", r"\bwafer\b", r"\bgummies\b", r"\bchana\b"]),
    ("Beverages", [r"\btea\b", r"\bcoffee\b", r"\bjuice\b", r"\bsoft drink\b", r"\bsoda\b",
                   r"\bwater\b", r"\benergy drink\b", r"\bdrink powder\b", r"\bnectar\b",
                   r"\byogurt drink\b", r"\bmilk drink\b", r"\bmalt drink\b", r"\baam panna\b"]),
    ("Household", [r"\bdetergent\b", r"\bdishwash\b", r"\btoilet cleaner\b", r"\bfloor cleaner\b",
                   r"\bcleaner\b", r"\bfabric conditioner\b", r"\bscrub\b", r"\btissue\b",
                   r"\bgarbage bags?\b", r"\blaundry\b", r"\bfoil\b", r"\broom freshener\b",
                   r"\bmosquito repellent\b", r"\broom freshener\b", r"\bcat litter\b",
                   r"\bair freshener\b", r"\bbrush\b", r"\bnapkins\b", r"\bdishwasher tablets\b"]),
    ("Staples", [r"\brice\b", r"\batta\b", r"\bflour\b", r"\bsalt\b", r"\bsugar\b",
                 r"\bcooking oil\b", r"\bsunflower oil\b", r"\bgroundnut oil\b", r"\bmustard oil\b",
                 r"\brice bran oil\b", r"\bpulses?\b", r"\bdal\b", r"\blentils?\b", r"\bspices?\b",
                 r"\bmasala\b", r"\bpepper powder\b", r"\bturmeric\b", r"\bcumin\b", r"\bpoha\b",
                 r"\brava\b", r"\bbesan\b", r"\bpasta\b", r"\bmacaroni\b", r"\bcorn flour\b",
                 r"\boats\b", r"\bdalia\b", r"\bporridge mix\b", r"\bsoy sauce\b", r"\bbaking soda\b",
                 r"\binstant noodles\b", r"\bwheat\b", r"\bchickpeas\b"]),
]

def suggest_category(product_name: object) -> tuple[str, str, str]:
    """Return (suggested_category, confidence, reason). Confidence is rule-match status, not probability."""
    if pd.isna(product_name) or not str(product_name).strip():
        return "Other", "Review", "Blank product name"
    name = re.sub(r"\s+", " ", str(product_name).strip().lower())

    # Product-type-first edge cases
    if "coconut milk soap" in name:
        return "Personal Care", "Rule match", "Classified by product type: soap"
    if "coconut milk beverage" in name:
        return "Beverages", "Rule match", "Classified by product type: beverage"
    if "hair oil" in name:
        return "Personal Care", "Rule match", "Hair oil is personal care"
    if "cooking oil" in name or re.search(r"\b(sunflower|groundnut|mustard|olive|rice bran|coconut) oil\b", name):
        return "Staples", "Rule match", "Cooking oil is a staple"
    if "protein bar" in name:
        return "Snacks", "Rule match", "Protein bars are snacks"

    for category, patterns in RULES:
        for pattern in patterns:
            if re.search(pattern, name):
                return category, "Rule match", f"Matched rule: {pattern}"
    return "Other", "Review", "No category rule matched; manual review recommended"

def annotate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    required = {"item_id", "product_name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")
    out = df.copy()
    results = out["product_name"].apply(suggest_category)
    out[["suggested_label", "confidence_status", "rule_reason"]] = pd.DataFrame(results.tolist(), index=out.index)
    return out
