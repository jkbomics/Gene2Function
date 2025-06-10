import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gene Function Table", layout="wide", initial_sidebar_state="collapsed")

# -----------------------
# Helper: pathway links
# -----------------------
def make_pathway_links(pathways, for_display_html=True):
    links = []
    if pd.isna(pathways) or pathways == "":
        return ""

    for entry in str(pathways).split(';'):
        entry = entry.strip()
        if not entry:
            continue

        if ':' in entry:
            source, pid = entry.split(':', 1)
            source = source.strip().lower()
            pid = pid.strip()

            if for_display_html:
                if source == "kegg":
                    links.append(f'<a href="https://www.kegg.jp/dbget-bin/www_bget?{pid}" target="_blank">{pid}</a>')
                elif source == "reactome":
                    links.append(f'<a href="https://reactome.org/PathwayBrowser/#/{pid}" target="_blank">{pid}</a>')
                elif source == "wikipathways":
                    links.append(f'<a href="https://www.wikipathways.org/instance/{pid}" target="_blank">{pid}</a>')
                elif source == "netpath":
                    links.append(f'<a href="https://www.netpath.org/pathways?path_id={pid}" target="_blank">{pid}</a>')
                elif source == "biocarta":
                    links.append(f'<a href="https://cgap.nci.nih.gov/Pathways/BioCarta_Pathways?ID={pid}" target="_blank">{pid}</a>')
                elif source == "pid":
                    links.append(f'<a href="https://www.ndexbio.org/viewer/networks/{pid}" target="_blank">{pid}</a>')
                elif source == "smpdb":
                    links.append(f'<a href="https://smpdb.ca/pathways/{pid}" target="_blank">{pid}</a>')
                else:
                    links.append(pid)
            else:
                links.append(pid)
        else:
            links.append(entry)

    return ", ".join(links)

# -----------------------
# Get session state results
# -----------------------
results = st.session_state.get('gene_search_results', [])

# -----------------------
# Display Results
# -----------------------
if results:
    result_df = pd.DataFrame(results)

    # Add anchor at the top
    st.markdown('<a name="top"></a>', unsafe_allow_html=True)

    # Button to scroll to bottom
    st.markdown('<p style="text-align:right"><a href="#bottom"><button style="padding:10px 20px; font-size:16px;">⬇️ Scroll to Bottom</button></a></p>', unsafe_allow_html=True)

    st.header("Gene Function Table")

    # DataFrame for HTML clickable view
    html_df = result_df.copy()
    if "pathway" in html_df.columns:
        html_df["pathway"] = html_df["pathway"].apply(lambda x: make_pathway_links(x, for_display_html=True))

    # DataFrame for interactive Streamlit table (no HTML)
    clean_df = result_df.copy()
    if "pathway" in clean_df.columns:
        clean_df["pathway"] = clean_df["pathway"].apply(lambda x: make_pathway_links(x, for_display_html=False))

    columns_order = [
        "input_gene", "gene_symbol", "name", "function",
        "pathway", "go_terms", "pharmgkb", "entrez_id", "uniprot", "taxid"
    ]
    html_df = html_df[[col for col in columns_order if col in html_df.columns]]
    clean_df = clean_df[[col for col in columns_order if col in clean_df.columns]]

    # Display HTML table with links
    st.markdown("### 📊 Gene Function Table (with Clickable Pathways)")
    st.markdown(html_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Display Streamlit interactive table
    st.markdown("### 🔍 Interactive Table (Filterable, Non-clickable)")
    def highlight_missing(s):
        return ['background-color: #ffdddd' if pd.isna(v) or v == "" else '' for v in s]

    st.dataframe(clean_df.style.apply(highlight_missing, axis=0), use_container_width=True)

    # CSV Preview
    st.markdown("📝 **Preview CSV Content (copyable)**")
    st.code(clean_df.drop(columns=["pathway"]).to_csv(index=False), language='csv')

    # Download CSV
    csv = clean_df.drop(columns=["pathway"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name="gene2function_results.csv",
        mime="text/csv"
    )

    # Anchor at bottom
    st.markdown('<a name="bottom"></a>', unsafe_allow_html=True)

    # Button to scroll back to top
    st.markdown('<p style="text-align:right"><a href="#top"><button style="padding:10px 20px; font-size:16px;">⬆️ Scroll to Top</button></a></p>', unsafe_allow_html=True)

else:
    st.info("No gene search results available. Please go back to the home page and search for genes.")
