from src.pipeline import run_pipeline

if __name__ == "__main__":
    metrics = run_pipeline()
    print("\nProject run completed.")
    print("-" * 48)
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print("\nGenerated:")
    print("  database/retail_annotation.db")
    print("  reports/quality_report.xlsx")
    print("  reports/final_labels.csv")
    print("  reports/validation_issues.csv")
    print("  reports/summary.json")
