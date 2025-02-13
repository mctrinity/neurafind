import os
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
import faiss
import numpy as np

# Define paths
base_dir = os.path.abspath(os.path.dirname(__file__))
faiss_index_path = os.path.join(base_dir, "../../models/item_faiss_index.bin")
embeddings_path = os.path.join(base_dir, "../../models/item_embeddings.csv")
models_dir = os.path.dirname(faiss_index_path)

# Ensure models directory exists
os.makedirs(models_dir, exist_ok=True)

# Load dataset
file_path = os.path.join(base_dir, "../../data/processed/user_interactions_cleaned.csv")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Data file not found: {file_path}")
df = pd.read_csv(file_path)

# Ensure unique item list for indexing
unique_items = df["item_id"].unique()

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()


# Function to generate embeddings
def generate_embedding(text):
    inputs = tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()


# Create FAISS index
d = 768  # BERT embedding size
index = faiss.IndexFlatL2(d)

# Dictionary to map item IDs to embeddings
item_embeddings = {}

# Process each item and store embeddings
print("Generating embeddings and building FAISS index...")
for item in unique_items:
    embedding = generate_embedding(str(item))
    item_embeddings[item] = embedding
    index.add(np.array([embedding], dtype=np.float32))

# Ensure index is not empty before saving
if index.ntotal == 0:
    raise RuntimeError("FAISS index is empty. No embeddings were added.")

# Save the FAISS index
faiss.write_index(index, faiss_index_path)
print(f"✅ FAISS index saved at: {faiss_index_path}")

# Save item ID mapping
embedding_df = pd.DataFrame.from_dict(item_embeddings, orient="index")
embedding_df.to_csv(embeddings_path)
print(f"✅ Item embeddings saved at: {embeddings_path}")
