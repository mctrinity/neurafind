import pandas as pd
import os

# Define the data directory
data_dir = "data/raw"
os.makedirs(data_dir, exist_ok=True)

# Create sample user interaction data
data = {
    "user_id": [101, 102, 103, 101, 104, 105, 103, 102, 106, 107],
    "item_id": [
        "A001",
        "A002",
        "A003",
        "A002",
        "A004",
        "A005",
        "A001",
        "A003",
        "A006",
        "A007",
    ],
    "rating": [4.5, 3.0, 5.0, 2.5, 4.0, 3.5, 5.0, 4.0, 2.0, 4.8],
    "timestamp": [
        1700000000,
        1700000100,
        1700000200,
        1700000300,
        1700000400,
        1700000500,
        1700000600,
        1700000700,
        1700000800,
        1700000900,
    ],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
csv_path = os.path.join(data_dir, "user_interactions.csv")
df.to_csv(csv_path, index=False)

print(f"✅ Sample data saved at: {csv_path}")
