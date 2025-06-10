# 🧬 Gene2Function

**Gene2Function** is a modular Streamlit-based bioinformatics tool that takes gene IDs or symbols as input and provides predicted functional annotations, associated pathways, and potential disease links. The tool is under active development and aims to help researchers quickly gather functional insights.

---

## 🚀 Features

- 🔍 Input single gene
- 🧠 Returns predicted:
  - Gene function
  - Pathway associations
  - Disease enrichment (coming soon via DisGeNET)
- ✅ Simple web UI built with Streamlit
- 🔗 Modular and expandable codebase

---

## 🛠️ Tech Stack

- Python 3.10
- [Streamlit](https://streamlit.io/)
- Biothings API
- DisGeNET (planned)
- Pandas, Requests

---

## 📈 Future Scope

- 🔍 Integration with Enrichr and Harmonizome APIs  
- 📊 Add heatmaps, network plots, and charts  
- 🤖 Optional GPT/BioBERT integration for intelligent annotation  
- 🧬 Organism-agnostic annotation using UniProt cross-references

---

## 📦 Installation

```bash
git clone https://github.com/jkbomics/Gene2Function.git
cd Gene2Function
conda create -n gene2func python=3.10 -y
conda activate gene2func
pip install -r requirements.txt
streamlit run app/main.py
```
---

## 👩‍💻 Author

**Helga Jenifer M**  
[LinkedIn](https://www.linkedin.com/in/helga-jenifer-m-208977147)  
Freelance Bioinformatician | AI in Bioinformatics Enthusiast 
