import os
import faiss
import numpy as np
import pandas as pd
import torch
import gc
from transformers import BertTokenizer, BertModel

# Define paths
base_dir = os.path.abspath(os.path.dirname(__file__))
faiss_index_path = os.path.join(base_dir, "../../models/item_faiss_index.bin")
embeddings_path = os.path.join(base_dir, "../../models/item_embeddings.csv")
models_dir = os.path.dirname(faiss_index_path)

# Ensure models directory exists
os.makedirs(models_dir, exist_ok=True)

# Load FAISS index
if not os.path.exists(faiss_index_path):
    raise FileNotFoundError(f"FAISS index file not found: {faiss_index_path}")

print("Loading FAISS index...")
index = faiss.read_index(faiss_index_path)
print(
    f"FAISS index loaded successfully. Index dimension: {index.d}, Total entries: {index.ntotal}"
)

if index.ntotal == 0:
    raise RuntimeError("FAISS index is empty. No embeddings were added.")

# Load item embeddings mapping
if not os.path.exists(embeddings_path):
    raise FileNotFoundError(f"Embeddings CSV file not found: {embeddings_path}")

print("Loading item embeddings...")
item_embeddings_df = pd.read_csv(embeddings_path, index_col=0)
item_ids = item_embeddings_df.index.tolist()
print(f"Item embeddings loaded successfully. Number of items: {len(item_ids)}")

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model.eval()


# Function to generate embedding for a search query
def generate_query_embedding(query):
    inputs = tokenizer(
        query, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
    embedding = embedding.astype(np.float32).reshape(
        1, -1
    )  # Ensure correct shape for FAISS
    torch.cuda.empty_cache()  # Clear GPU cache
    gc.collect()  # Force garbage collection to free memory
    print(f"Generated query embedding with shape: {embedding.shape}")
    return embedding


# Function to search for similar items
def search_items(query, top_k=5):
    query_embedding = generate_query_embedding(query)

    # Debugging FAISS index dimension
    print(
        f"Query embedding shape: {query_embedding.shape}, FAISS index dimension: {index.d}"
    )
    if query_embedding.shape[1] != index.d:
        raise ValueError(
            f"Embedding size mismatch: expected {index.d}, got {query_embedding.shape[1]}"
        )

    # Ensure FAISS index has entries before searching
    if index.ntotal == 0:
        raise RuntimeError("FAISS index is empty. Cannot perform search.")

    distances, indices = index.search(query_embedding, top_k)
    results = [
        item_ids[idx] for idx in indices[0] if 0 <= idx < len(item_ids)
    ]  # Prevent negative indexing

    # Clear caches again after search
    torch.cuda.empty_cache()
    gc.collect()

    return results


# Example search query
if __name__ == "__main__":
    query = input("Enter search query: ")
    results = search_items(query)
    print("🔍 Top search results:", results)
