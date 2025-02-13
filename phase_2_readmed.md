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
```bash
conda install -c conda-forge faiss
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

## **🚨 Critical Issue: Segmentation Fault in FAISS**
### **Issue Description**
While running `search_engine.py`, we encountered a **segmentation fault**, causing the script to crash unexpectedly. This issue is likely due to:
1. **FAISS index handling errors** – Potential corruption or improper loading.
2. **Torch tensor memory issues** – Clearing unnecessary GPU cache (`torch.cuda.empty_cache()`).
3. **Compatibility issues with FAISS on macOS ARM (M1/M2/M3 chips)**.

### **✅ Fixes Applied**
- **Switched to Conda** for better macOS ARM support.
- **Regenerated FAISS index and embeddings** to ensure no corruption.
- **Removed unnecessary GPU cache clearing** since we run on CPU (`torch.cuda.empty_cache()`).
- **Forced garbage collection (`gc.collect()`)** to prevent memory leaks.
- **Tested FAISS search functionality separately** to validate correct behavior.
- **Modified `search_engine.py` to prevent memory corruption**.

### **🛠 If Segmentation Fault Persists**
1️⃣ **Test FAISS separately**:
```bash
python -c "import faiss; d = 768; index = faiss.IndexFlatL2(d); print('FAISS Test Passed')"
```
- If **this crashes**, FAISS might be broken on your system.
- If **it works**, then `search_engine.py` may need further debugging.

2️⃣ **Run `search_engine.py` in Debug Mode**:
```bash
python -m pdb phases/phase_2_models/search_engine.py
```
- Enter **a query**, and when the segmentation fault happens, type:
  ```
  where
  ```
  - This will **pinpoint the exact failure location**.

3️⃣ **Check FAISS Installation**
```bash
pip list | grep faiss
```
- Ensure that `faiss-cpu` is installed (`faiss-gpu` is not compatible with macOS ARM).
- If FAISS seems broken, try reinstalling:
  ```bash
  conda install -c conda-forge faiss
  ```

---

## **🔥 Final Deliverables**
✔ **FAISS Index:** `models/item_faiss_index.bin`  
✔ **Item Embeddings:** `models/item_embeddings.csv`  
✔ **Search Engine:** `phases/phase_2_models/search_engine.py`  
✔ **Fully Documented Debugging Process** 🚀
