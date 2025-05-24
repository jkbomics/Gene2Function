import streamlit as st

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import search_gene_function

st.set_page_config(page_title="Gene2Function", layout="centered")

st.title("🧬 Gene2Function")
st.subheader("Discover gene function, pathway & disease information")

gene_input = st.text_input("🔍 Enter a Gene ID or Gene Symbol", "")

if gene_input:
    with st.spinner("Searching..."):
        result = search_gene_function(gene_input)
        if result:
            st.success("Results found!")
            st.json(result)
        else:
            st.error("No results found.")
