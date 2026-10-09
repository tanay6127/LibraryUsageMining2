
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Project configuration
st.set_page_config(
    page_title="LibraryIQ | Library Analytics",
    page_icon="📚",
    layout="wide"
)

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "library_borrowing.csv"
RESULTS_DIR = BASE_DIR / "results"

# Custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b1020;
        color: #e8ecf7;
    }
    [data-testid="stMetric"] {
        background-color: #141d32;
        border: 1px solid #26314a;
        padding: 20px;
        border-radius: 14px;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📚 LibraryIQ")
st.subheader("University Library Analytics Dashboard")
st.caption(
    "Understand borrowing patterns and make "
    "data-driven library collection decisions."
)

st.divider()

# Load dataset
if not DATA_PATH.exists():
    st.error(
        "Dataset not found. Please upload "
        "data/library_borrowing.csv to GitHub."
    )
    st.stop()

try:
    df = pd.read_csv(DATA_PATH)
except Exception as exc:
    st.error(f"Could not read the dataset: {exc}")
    st.stop()

required_columns = {"Student_ID", "Book_Title", "Category"}

if not required_columns.issubset(df.columns):
    st.error(
        "The dataset must contain these columns: "
        "Student_ID, Book_Title, Category."
    )
    st.stop()

if df.empty:
    st.warning("The borrowing dataset is empty.")
    st.stop()

# Sidebar filters
st.sidebar.title("⚙️ Dashboard Filters")

categories = sorted(
    df["Category"].dropna().astype(str).unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select book category",
    ["All Categories"] + categories
)

filtered_df = df.copy()

if selected_category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["Category"].astype(str) == selected_category
    ]

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("📖 Borrowing Records", len(filtered_df))
col2.metric(
    "👨‍🎓 Unique Students",
    filtered_df["Student_ID"].nunique()
)
col3.metric(
    "📚 Unique Books",
    filtered_df["Book_Title"].nunique()
)

st.divider()

# Book popularity
st.subheader("📊 Book Popularity")

book_counts = (
    filtered_df["Book_Title"]
    .value_counts()
    .rename_axis("Book")
    .reset_index(name="Borrow Count")
)

if not book_counts.empty:
    fig_books = px.bar(
        book_counts.head(15),
        x="Book",
        y="Borrow Count",
        color="Borrow Count",
        title="Top 15 Most Borrowed Books",
        template="plotly_dark"
    )
    fig_books.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig_books, use_container_width=True)
else:
    st.info("No book borrowing data available.")

# Category popularity
st.subheader("📚 Category Popularity")

category_counts = (
    filtered_df["Category"]
    .value_counts()
    .rename_axis("Category")
    .reset_index(name="Borrow Count")
)

if not category_counts.empty:
    fig_categories = px.pie(
        category_counts,
        names="Category",
        values="Borrow Count",
        title="Borrowing Records by Category",
        hole=0.45,
        template="plotly_dark"
    )
    fig_categories.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_categories, use_container_width=True)

st.divider()

# Student clustering results
st.subheader("🧩 Student Borrowing Clusters")

clusters_path = RESULTS_DIR / "student_clusters.csv"

if clusters_path.exists():
    try:
        clusters = pd.read_csv(clusters_path)

        if {"Student_ID", "Cluster"}.issubset(clusters.columns):
            st.dataframe(
                clusters.sort_values(["Cluster", "Student_ID"]),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("The clustering CSV has unexpected columns.")
    except Exception as exc:
        st.error(f"Could not load clustering results: {exc}")
else:
    st.info(
        "Clustering results are not available yet. "
        "Upload results/student_clusters.csv."
    )

st.divider()

# Association rules
st.subheader("🔗 Books Borrowed Together")

rules_path = RESULTS_DIR / "association_rules.csv"

if rules_path.exists():
    try:
        rules = pd.read_csv(rules_path)

        if not rules.empty:
            st.dataframe(
                rules,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No association rules were generated.")
    except Exception as exc:
        st.error(f"Could not load association rules: {exc}")
else:
    st.info(
        "Association rules are not available yet. "
        "Upload results/association_rules.csv."
    )

st.divider()

# Collection planning insight
st.subheader("💡 Collection Planning Insights")

if not book_counts.empty:
    top_book = book_counts.iloc[0]

    st.success(
        f"Most borrowed book in this selection: "
        f"{top_book['Book']} "
        f"({top_book['Borrow Count']} borrowing records)."
    )

st.caption(
    "LibraryIQ | Data-driven collection planning | "
    "Results depend on the supplied dataset."
)
