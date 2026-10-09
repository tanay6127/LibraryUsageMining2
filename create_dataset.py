
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"

st.set_page_config(
    page_title="University Library Analytics",
    page_icon="📚",
    layout="wide"
)

st.title("📚 University Library Collection Planning")
st.caption(
    "Analyze borrowing patterns to support "
    "data-driven library decisions."
)

# Load data
df = pd.read_csv(DATA_DIR / "library_borrowing.csv")
clusters_path = RESULTS_DIR / "student_clusters.csv"
rules_path = RESULTS_DIR / "association_rules.csv"

# Sidebar filters
st.sidebar.header("Filters")
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Book category", categories
)

filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Borrowing Records", len(filtered_df))
col2.metric("Unique Students", filtered_df["Student_ID"].nunique())
col3.metric("Unique Books", filtered_df["Book_Title"].nunique())

st.divider()

# Book popularity chart
st.subheader("📊 Book Popularity")

book_counts = (
    filtered_df["Book_Title"]
    .value_counts()
    .rename_axis("Book")
    .reset_index(name="Borrow Count")
)

fig_books = px.bar(
    book_counts,
    x="Book",
    y="Borrow Count",
    color="Borrow Count",
    title="Borrowing Frequency by Book"
)

st.plotly_chart(fig_books, use_container_width=True)

# Category popularity
st.subheader("📚 Category Popularity")

category_counts = (
    filtered_df["Category"]
    .value_counts()
    .rename_axis("Category")
    .reset_index(name="Borrow Count")
)

fig_categories = px.pie(
    category_counts,
    names="Category",
    values="Borrow Count",
    title="Borrowing Records by Category"
)

st.plotly_chart(fig_categories, use_container_width=True)

# Clustering results
st.subheader("🧩 Student Borrowing Clusters")

if clusters_path.exists():
    clusters = pd.read_csv(clusters_path)
    st.dataframe(
        clusters.sort_values(["Cluster", "Student_ID"]),
        use_container_width=True
    )
else:
    st.info("Run src/clustering.py to generate cluster results.")

# Association rules
st.subheader("🔗 Books Borrowed Together")

if rules_path.exists():
    rules = pd.read_csv(rules_path)
    st.dataframe(rules, use_container_width=True)
else:
    st.info("Run src/association.py to generate association rules.")

# Acquisition planning insights
st.subheader("💡 Collection Planning Insights")

if not book_counts.empty:
    top_book = book_counts.iloc[0]
    st.write(
        f"**Most borrowed book in this selection:** "
        f"{top_book['Book']} "
        f"({top_book['Borrow Count']} records)."
    )

st.caption(
    "These results use sample data. Acquisition decisions "
    "should also consider available copies, costs, and librarian review."
)
