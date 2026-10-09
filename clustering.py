
import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "library_borrowing.csv"
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Load borrowing records
df = pd.read_csv(DATA_PATH)

# Create a student-book borrowing matrix
# Rows = students, columns = books
student_book_matrix = pd.crosstab(
    df["Student_ID"],
    df["Book_Title"]
)

# Scale the features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(student_book_matrix)

# Create and train the K-Means model
model = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

cluster_labels = model.fit_predict(scaled_data)

# Attach cluster labels to students
cluster_results = pd.DataFrame({
    "Student_ID": student_book_matrix.index,
    "Cluster": cluster_labels
})

# Save student clusters
cluster_results.to_csv(
    RESULTS_DIR / "student_clusters.csv",
    index=False
)

# Print results
print("=" * 50)
print("UNIVERSITY LIBRARY - CLUSTERING RESULTS")
print("=" * 50)

print("\nStudents grouped by borrowing patterns:")
print(cluster_results.sort_values("Cluster").to_string(index=False))

print("\nNumber of students in each cluster:")
print(cluster_results["Cluster"].value_counts().sort_index().to_string())

print("\nClustering completed successfully!")
print("Results saved to results/student_clusters.csv")
