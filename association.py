
import pandas as pd
from pathlib import Path
from mlxtend.frequent_patterns import apriori, association_rules

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "library_borrowing.csv"
RESULTS_DIR = PROJECT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Load borrowing data
df = pd.read_csv(DATA_PATH)

# Convert records into a student-book transaction matrix
basket = pd.crosstab(
    df["Student_ID"],
    df["Book_Title"]
).gt(0)

print("=" * 55)
print("UNIVERSITY LIBRARY - ASSOCIATION RULE MINING")
print("=" * 55)

# Find frequently borrowed book combinations
frequent_itemsets = apriori(
    basket,
    min_support=0.2,
    use_colnames=True
)

if frequent_itemsets.empty:
    print("\nNo frequent book combinations found.")
else:
    print("\nFREQUENT BOOK COMBINATIONS")
    print("-" * 35)

    frequent_itemsets["Books"] = frequent_itemsets[
        "itemsets"
    ].apply(lambda books: ", ".join(sorted(books)))

    print(
        frequent_itemsets[
            ["Books", "support"]
        ].to_string(index=False)
    )

    # Generate association rules
    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=0.5
    )

    if rules.empty:
        print("\nNo association rules met the threshold.")
    else:
        rules["If_Borrowed"] = rules["antecedents"].apply(
            lambda books: ", ".join(sorted(books))
        )
        rules["Also_Borrowed"] = rules["consequents"].apply(
            lambda books: ", ".join(sorted(books))
        )

        output = rules[
            [
                "If_Borrowed",
                "Also_Borrowed",
                "support",
                "confidence",
                "lift"
            ]
        ].sort_values("lift", ascending=False)

        output.to_csv(
            RESULTS_DIR / "association_rules.csv",
            index=False
        )

        print("\nASSOCIATION RULES")
        print("-" * 35)
        print(output.round(3).to_string(index=False))

        print("\nRules saved to results/association_rules.csv")

print("\nAssociation analysis completed!")
