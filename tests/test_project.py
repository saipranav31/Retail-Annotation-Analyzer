import tempfile
import unittest
from pathlib import Path
import pandas as pd

from src.annotate import suggest_category, annotate_dataframe
from src.validate import validate_products, evaluate_gold
from src.database import build_database, run_sql_query

class AnnotationTests(unittest.TestCase):
    def test_product_type_edge_cases(self):
        self.assertEqual(suggest_category("Coconut Milk Soap")[0], "Personal Care")
        self.assertEqual(suggest_category("Coconut Milk Beverage")[0], "Beverages")
        self.assertEqual(suggest_category("Protein Bar Chocolate")[0], "Snacks")
        self.assertEqual(suggest_category("Coconut Cooking Oil")[0], "Staples")

    def test_blank_name_flagged(self):
        df = pd.DataFrame({"item_id": ["P001"], "product_name": [""]})
        validated = validate_products(annotate_dataframe(df))
        self.assertTrue(bool(validated.iloc[0]["is_missing_name"]))
        self.assertTrue(bool(validated.iloc[0]["needs_review"]))

    def test_duplicate_name_flagged(self):
        df = pd.DataFrame({"item_id": ["P001", "P002"], "product_name": ["Amul Butter 500g", "Amul Butter 500g"]})
        validated = validate_products(annotate_dataframe(df))
        self.assertTrue(validated["is_duplicate_name"].all())

    def test_gold_evaluation(self):
        df = annotate_dataframe(pd.DataFrame({
            "item_id": ["P001", "P002"],
            "product_name": ["Amul Butter 500g", "Lays Magic Masala Chips"]
        }))
        gold = pd.DataFrame({"item_id": ["P001", "P002"], "gold_label": ["Dairy", "Snacks"]})
        _, metrics = evaluate_gold(df, gold)
        self.assertEqual(metrics["reference_items"], 2)
        self.assertEqual(metrics["accuracy_pct"], 100.0)

    def test_sqlite_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            df = pd.DataFrame({"item_id": ["P001"], "product_name": ["Amul Butter 500g"]})
            validated = validate_products(annotate_dataframe(df))
            gold = pd.DataFrame({"item_id": ["P001"], "gold_label": ["Dairy"]})
            db_path = Path(tmp) / "test.db"
            build_database(db_path, validated, gold)
            result = run_sql_query(db_path, "SELECT COUNT(*) AS n FROM items")
            self.assertEqual(int(result.iloc[0]["n"]), 1)

if __name__ == "__main__":
    unittest.main()
