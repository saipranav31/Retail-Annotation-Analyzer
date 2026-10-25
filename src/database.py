
"""SQLite persistence and query helpers."""

import sqlite3
from pathlib import Path

import pandas as pd


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS items (
    item_id TEXT PRIMARY KEY,
    product_name TEXT
);

CREATE TABLE IF NOT EXISTS annotations (
    item_id TEXT PRIMARY KEY,
    suggested_label TEXT NOT NULL,
    confidence_status TEXT NOT NULL,
    rule_reason TEXT,
    needs_review INTEGER NOT NULL,
    review_reason TEXT,
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);

CREATE TABLE IF NOT EXISTS gold (
    item_id TEXT PRIMARY KEY,
    gold_label TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES items(item_id)
);
"""


def build_database(db_path, validated, gold):
    """Save products, annotations, and reference labels to SQLite."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)

    try:
        conn.executescript(SCHEMA)

        # Clear old data in foreign-key-safe order.
        conn.execute("DELETE FROM annotations")
        conn.execute("DELETE FROM gold")
        conn.execute("DELETE FROM items")

        items = validated[["item_id", "product_name"]].copy()
        items["product_name"] = items["product_name"].where(
            items["product_name"].notna(), None
        )

        items.to_sql("items", conn, if_exists="append", index=False)

        annotations = validated[
            [
                "item_id",
                "suggested_label",
                "confidence_status",
                "rule_reason",
                "needs_review",
                "review_reason",
            ]
        ].copy()

        annotations["needs_review"] = (
            annotations["needs_review"].astype(int)
        )

        annotations.to_sql(
            "annotations", conn, if_exists="append", index=False
        )

        gold[["item_id", "gold_label"]].to_sql(
            "gold", conn, if_exists="append", index=False
        )

        conn.commit()

    finally:
        # Always release the database file, including on errors.
        conn.close()


def run_sql_query(db_path, query):
    """Execute a SQL query and return its results as a DataFrame."""
    conn = sqlite3.connect(db_path)

    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
