
from pathlib import Path

import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"


def load_csv(path):
    """Load a CSV file if it exists."""
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


@app.route("/")
def home():
    # Load borrowing data
    df = load_csv(DATA_DIR / "library_borrowing.csv")

    if df.empty:
        return "Dataset not found. Run data/create_dataset.py first."

    # Calculate dashboard metrics
    total_records = len(df)
    total_students = df["Student_ID"].nunique()
    total_books = df["Book_Title"].nunique()

    # Book popularity
    book_counts = (
        df["Book_Title"]
        .value_counts()
        .rename_axis("book")
        .reset_index(name="count")
    )

    # Category popularity
    category_counts = (
        df["Category"]
        .value_counts()
        .rename_axis("category")
        .reset_index(name="count")
    )

    # Clustering results
    clusters = load_csv(
        RESULTS_DIR / "student_clusters.csv"
    )

    # Association rules
    rules = load_csv(
        RESULTS_DIR / "association_rules.csv"
    )

    return render_template(
        "index.html",
        total_records=total_records,
        total_students=total_students,
        total_books=total_books,
        book_counts=book_counts.to_dict("records"),
        category_counts=category_counts.to_dict("records"),
        clusters=clusters.to_dict("records"),
        rules=rules.to_dict("records"),
    )


if __name__ == "__main__":
    app.run(debug=True)
