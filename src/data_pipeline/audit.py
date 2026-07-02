import pandas as pd
from pathlib import Path

def generate_audit_report(csv_path: str = "data/raw/netflix_titles.csv", output_path: str = "docs/data_audit_report.md"):
    \"\"\"Generates a markdown audit report for the raw dataset.\"\"\"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return
        
    report = [
        "# Raw Data Audit Report",
        f"**Records:** {len(df):,}",
        f"**Columns:** {len(df.columns)}",
        "",
        "## Missing Values",
        "| Column | Null Count | Null % |",
        "|---|---|---|"
    ]
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        if null_count > 0:
            report.append(f"| `{col}` | {null_count:,} | {null_pct:.2f}% |")
            
    report.extend([
        "",
        "## Duplicates",
        f"- Exact Duplicate Rows: {df.duplicated().sum()}",
        f"- Duplicate `show_id`s: {df.duplicated(subset=['show_id']).sum()}"
    ])
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
if __name__ == "__main__":
    generate_audit_report()
