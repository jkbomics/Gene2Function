# 🧬 Gene2Function

**Gene2Function** is a modular, multi-page, Streamlit-based bioinformatics tool that takes gene IDs or symbols as input and provides predicted functional annotations, associated pathways, and potential disease links. Built for speed and usability, this app empowers researchers to quickly extract and explore gene-level biological insights.
---
✅ Now supports scroll navigation, multi-page interface, and interactive plots for GO terms and pathways!
---

## 🚀 Features

- 🔍 Input single gene
- 🧠 Returns predicted:
  - Gene function
  - Pathway associations (KEGG, Reactome, WikiPathways, etc.)
  - GO terms: Biological Process, Molecular Function, Cellular Component
  - Cross-references: Entrez, UniProt, PharmGKB, Taxonomy ID
  - Disease enrichment (coming soon via DisGeNET)
 
---

📊 Visualizations (NEW)
  - Interactive pie charts for GO terms and pathway database distribution.
  - Per-plot customization controls (height, font, colors).
  - View Top 10 GO terms for better interpretability.
📋 Gene Function Table (Enhanced)
  - Dual display:
     - ✅ Clickable HTML table for enriched info.
     -✅ Filterable Streamlit table for clean, interactive exploration.
  - CSV export and preview options included.
  - 🔄 Scroll to Top/Bottom buttons for seamless navigation in long tables.
🗂️ UI & Navigation (NEW)
  - Multi-page app with:
    - main.py: Gene search + plots
    - pages/1_Gene_Table.py: Full annotation table
  - Streamlit sidebar collapsed by default for a cleaner view.
  - "View Gene Table" navigation button.
🔗 Modular & Expandable Codebase
  - Built for flexibility: Easily integrate APIs, visualization libraries, or ML models.

---

## 🛠️ Tech Stack

- Python 3.10
- [Streamlit](https://streamlit.io/)
- Biothings API
- Pandas, Requests
- DisGeNET (⚙️ integration coming soon)

---

## 📈 Future Scope

- 🧬 Organism-agnostic annotation via UniProt cross-references  
- 📊 Add heatmaps, network plots, and advanced charts 
- 🤖 AI integration with GPT/BioBERT for intelligent annotation  
- 🔍 Use external enrichment tools (e.g., Enrichr, Harmonizome)

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
