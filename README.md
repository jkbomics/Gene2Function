# 🧬 Gene2Function

Gene2Function is a lightweight, modular bioinformatics tool built with Streamlit. It accepts gene symbols/IDs as input and returns functional annotation, pathway involvement, and disease enrichment (DisGeNET API support coming soon).

## 🚀 Features
- Input gene symbol or upload list
- Returns:
  - Gene function summary
  - Pathways (via BioThings)
  - Disease associations (upcoming)

## 📦 Tech Stack
- Python
- Streamlit
- Biothings API
- DisGeNET API (in progress)

## 🔧 Setup
```bash
conda create -n gene2func python=3.10 -y
conda activate gene2func
pip install -r requirements.txt
streamlit run app/main.py
