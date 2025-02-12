#!/bin/bash

# Define subdirectories to be created inside the existing neurafind folder
SUBDIRS=(
    "phases/phase_1_data"
    "phases/phase_2_models"
    "phases/phase_3_optimization"
    "phases/phase_4_mlop"
    "data/raw"
    "data/processed"
    "models"
    "notebooks"
    "scripts"
)

# Navigate to neurafind directory
cd neurafind || { echo "neurafind directory not found!"; exit 1; }

# Create subdirectories
for dir in "${SUBDIRS[@]}"; do
    mkdir -p "$dir"
    echo "Created: $dir"
done

# Create essential files
touch "requirements.txt"
touch ".gitignore"
touch "README.md"
echo "Created essential files."

echo "✅ neurafind project structure is set up inside the existing repository!"

