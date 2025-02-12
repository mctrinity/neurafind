import pandas as pd
import os

# Define paths
raw_data_path = "data/raw/user_interactions.csv"
processed_data_path = "data/processed/user_interactions_cleaned.csv"
os.makedirs("data/processed", exist_ok=True)

# Load dataset
df = pd.read_csv(raw_data_path)

# Convert timestamp to readable datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# Check for missing values and fill or drop if necessary
if df.isnull().sum().sum() > 0:
    df.fillna(0, inplace=True)  # Replace missing values with 0 (modify as needed)

# Normalize ratings to a scale of 1-5 (if needed)
df["rating"] = df["rating"].clip(1, 5)

# Save cleaned dataset
df.to_csv(processed_data_path, index=False)

print(f"✅ Cleaned data saved at: {processed_data_path}")
