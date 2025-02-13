# 🚀 Phase 2: Implementing the Search Engine

## 📌 Overview
Phase 2 focuses on implementing a **FAISS-based search engine** that retrieves relevant items based on **BERT-generated embeddings**. The search engine is designed to provide efficient **similarity-based search** for user queries.

---

## **✅ Step 1: Setting Up Conda Environment (Recommended for macOS M3/M2/M1)**
### **Why Use Conda?**
- Better **dependency management** on macOS ARM-based chips.
- FAISS **runs more reliably** in Conda compared to `pip`.
- Conda provides **isolated environments**, preventing system conflicts.

### **Install Miniforge (Conda for macOS ARM)**
```bash
brew install miniforge
```
Restart your terminal after installation.

### **Create a Conda Environment**
```bash
conda create --name neurafind python=3.9
conda activate neurafind
```

### **Install FAISS Using Conda**
Since FAISS 1.10.0 is not available on Conda-forge for macOS ARM, install via `pip`:
```bash
pip install --no-cache-dir --upgrade faiss-cpu
```
Verify installation:
```bash
python -c "import faiss; print(faiss.__version__)"
```

### **Install Other Dependencies**
```bash
pip install torch transformers pandas numpy
```

---

## **✅ Step 2: Generating Item Embeddings**
### **Script: `embedding_generator.py`**
- Converts item IDs into **BERT embeddings**.
- Stores embeddings in a **FAISS index** for fast retrieval.
- Saves **FAISS index** and **item mappings** for later use.

**Command to Run:**
```bash
python phases/phase_2_models/embedding_generator.py
```

**Expected Output:**
- ✅ `models/item_faiss_index.bin`  (FAISS index file)
- ✅ `models/item_embeddings.csv`  (Embeddings mapping file)

---

## **✅ Step 3: Implementing the Search Engine**
### **Script: `search_engine.py`**
- Loads the **FAISS index** and **BERT model**.
- Converts user **search queries into embeddings**.
- Retrieves **most similar items** based on FAISS similarity search.

**Command to Run:**
```bash
python phases/phase_2_models/search_engine.py
```

**Expected Output:**
```
Loading FAISS index...
FAISS index loaded successfully. Index dimension: 768, Total entries: X
Loading item embeddings...
Item embeddings loaded successfully. Number of items: X
Enter search query: A001
🔍 Top search results: [A003, A007, ...]
```

---

## **🔍 Understanding Embeddings and FAISS**
### **✅ Why Do We Use Embeddings?**
- Embeddings **convert categorical data (item IDs) into numerical vectors**.
- Similar items have **closer vector representations** in high-dimensional space.
- This allows FAISS to **efficiently find nearest neighbors** based on similarity.

### **✅ Why Did We Create a FAISS Index?**
- Without FAISS, we'd have to **compare each query against all stored embeddings manually**, which is computationally expensive.
- FAISS organizes embeddings into a **searchable index**, allowing **fast retrieval**.
- **Querying FAISS returns the closest items in milliseconds**, making the search engine highly efficient.

---

## **🔍 Comparing FAISS with Elasticsearch**
### **✅ Similarities Between FAISS and Elasticsearch**
| **Feature**            | **FAISS (Embeddings-based Search)**           | **Elasticsearch (Text-based Search)**  |
|------------------------|--------------------------------|--------------------------------|
| **Purpose**           | Finds similar items via **vector embeddings** | Retrieves documents via **keyword matching** |
| **Storage Format**    | **High-dimensional vector index** | **Inverted index for fast text search** |
| **Similarity Search** | Uses **nearest neighbor search in vector space** | Uses **BM25, term frequency, fuzzy matching** |
| **Use Cases**         | **Recommendations, NLP-based search** | **Structured queries, full-text search** |

### **✅ Key Difference: FAISS vs. Elasticsearch**
- **FAISS** is optimized for **semantic similarity search** (finding related items based on embeddings).
- **Elasticsearch** is optimized for **text-based search** (matching documents using keywords and structured queries).
- A **hybrid approach** combines both—where **Elasticsearch retrieves documents**, and **FAISS ranks them using embeddings**.

---

## **🔍 Interpretation of Search Engine Results**
### **✅ FAISS is Working Correctly**
- **FAISS index loads successfully**, confirming that embeddings were indexed properly.
- **Query embedding shape matches FAISS index dimension (`768`)**, ensuring that embeddings are consistent.
- The search engine is **returning results without crashing**.

### **✅ Understanding the Search Results**
- **The query item (`A001`) appears in the top results**, confirming that FAISS recognizes it as most similar to itself (expected behavior).
- The next closest results are **`A002, A003, A007, A004`**, meaning these items have similar embeddings to `A001`.

### **🔎 Why are `A002, A003, A007, A004` Similar to `A001`?**
- FAISS ranks results based on **cosine similarity or L2 distance**.
- These items are **close in embedding space** to `A001`, meaning they share similar features.
- Possible reasons for similarity:
  - **Users who interacted with `A001` also interacted with these items**.
  - The **embeddings capture content similarities** (e.g., same category, similar descriptions).

### **🚀 Next Steps: Evaluating & Tuning the Search Engine**
#### **1️⃣ Evaluate Search Relevance**
- Are the **recommended results expected**?
- If the ranking **feels off**, we might need to **fine-tune the embeddings**.

#### **2️⃣ Test More Queries**
```bash
Enter search query: A003
Enter search query: A007
```
- Do the results **make sense**?
- Are the **top-ranked items logically similar** to the query?

#### **3️⃣ Tune FAISS Search Parameters (Optional)**
- FAISS parameters like **number of neighbors (`k`)** and **distance metric** can be adjusted.
- If results seem **too broad** or **too narrow**, we can tweak FAISS settings.

---

## **🚨 Critical Issue: OpenMP Conflict (`libomp.dylib`)**
### **Issue Description**
While running `search_engine.py`, we encountered an OpenMP (`libomp.dylib`) conflict, causing the script to crash with:
```
OMP: Error #15: Initializing libomp.dylib, but found libomp.dylib already initialized.
```
### **✅ Fix: Set Environment Variable to Prevent Crash**
To bypass this error, set:
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```
To make this permanent, add it to your `~/.zshrc`:
```bash
echo 'export KMP_DUPLICATE_LIB_OK=TRUE' >> ~/.zshrc
source ~/.zshrc
```

### **Alternative Fix: Reinstall OpenMP (`libomp`)**
```bash
brew install libomp
```
Then restart your terminal and rerun `search_engine.py`.

---

## **🔥 Final Deliverables**
✔ **FAISS Index:** `models/item_faiss_index.bin`  
✔ **Item Embeddings:** `models/item_embeddings.csv`  
✔ **Search Engine:** `phases/phase_2_models/search_engine.py`  
✔ **Fully Documented Debugging Process & Interpretation of Results** 🚀
