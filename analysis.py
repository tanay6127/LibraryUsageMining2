
import pandas as pd
from pathlib import Path

# Locate the dataset relative to this Python file
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "library_borrowing.csv"

# Load the library data
df = pd.read_csv(DATA_PATH)

print("=" * 50)
print("UNIVERSITY LIBRARY USAGE ANALYSIS")
print("=" * 50)

# Basic dataset information
print("\n1. DATASET SUMMARY")
print("-" * 30)
print("Total borrowing records:", len(df))
print("Unique students:", df["Student_ID"].nunique())
print("Unique books:", df["Book_Title"].nunique())

# Count borrowing records for each book
print("\n2. MOST BORROWED BOOKS")
print("-" * 30)

book_counts = df["Book_Title"].value_counts()
print(book_counts.to_string())

# Count borrowing records for each category
print("\n3. POPULAR BOOK CATEGORIES")
print("-" * 30)

category_counts = df["Category"].value_counts()
print(category_counts.to_string())

# Save analysis results
results_dir = PROJECT_DIR / "results"
results_dir.mkdir(exist_ok=True)

book_counts.rename_axis("Book_Title").reset_index(
    name="Borrow_Count"
).to_csv(results_dir / "book_popularity.csv", index=False)

category_counts.rename_axis("Category").reset_index(
    name="Borrow_Count"
).to_csv(results_dir / "category_popularity.csv", index=False)

print("\nAnalysis completed successfully!")
print("Results saved in the results folder.")
