import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px # Import plotly for plotting
from collections import defaultdict # To easily count terms

# Import actual gene search function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.helpers import search_gene_function

# Configure page settings for wide layout and collapsed sidebar
st.set_page_config(page_title="Gene2Function", layout="wide", initial_sidebar_state="collapsed")
st.title("🧬 Gene2Function")
st.subheader("🔍 Enter a Gene or Upload a File")

# Initialize session state for storing results (only needed for passing to another page)
if 'gene_search_results' not in st.session_state:
    st.session_state['gene_search_results'] = []
if 'original_pathways' not in st.session_state:
    st.session_state['original_pathways'] = None
if 'original_go_terms' not in st.session_state:
    st.session_state['original_go_terms'] = None

gene_input = st.text_input("🔡 Enter Gene Symbol/ID:")
uploaded_file = st.file_uploader("📁 Or Upload a CSV/TSV/Excel File", type=["csv", "tsv", "xlsx"])

# -----------------------
# File or manual input
# -----------------------
search_performed = False
current_results = [] # Temporary list for current search

if gene_input:
    with st.spinner("🔎 Searching..."):
        result = search_gene_function(gene_input.strip())
        if result:
            result["input_gene"] = gene_input.strip()
            current_results.append(result)
    search_performed = True

elif uploaded_file:
    ext = uploaded_file.name.split('.')[-1]
    if ext == "csv":
        df = pd.read_csv(uploaded_file)
    elif ext == "tsv":
        df = pd.read_csv(uploaded_file, sep="\t")
    elif ext == "xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error("❌ Unsupported file format.")
        st.stop()

    gene_column = df.columns[0]
    genes = df[gene_column].dropna().astype(str).unique()

    st.write("📋 Preview of uploaded gene list:")
    st.dataframe(df[[gene_column]].head(10))

    with st.spinner(f"🔍 Searching {len(genes)} gene(s)..."):
        for gene in genes:
            res = search_gene_function(gene.strip())
            if res:
                res["input_gene"] = gene.strip()
                current_results.append(res)
    search_performed = True

# Store results in session state ONLY after a search is performed
# These will be used by the '1_Gene_Table.py' page
if search_performed:
    st.session_state['gene_search_results'] = current_results
    if current_results:
        temp_df = pd.DataFrame(current_results)
        if "pathway" in temp_df.columns:
            st.session_state['original_pathways'] = temp_df["pathway"].copy()
        if "go_terms" in temp_df.columns:
            st.session_state['original_go_terms'] = temp_df["go_terms"].copy()
    else:
        st.session_state['original_pathways'] = None
        st.session_state['original_go_terms'] = None

# -----------------------
# Display Plots on the same page
# -----------------------
if st.session_state['gene_search_results']: # Check if there are results to display plots
    st.success(f"✅ Search complete! Found {len(st.session_state['gene_search_results'])} gene(s).")
    st.markdown("---")

    # Display button to navigate to the Gene Table page
    st.info("Click the button below to view the full Gene Function Table on a separate page.")
    
    # Give the function to the View Gene Table button to switch page
    if st.button("➡️ View Gene Table"):
        st.switch_page("pages/1_Gene_Table.py") # Explicitly switch to the Gene Table page


    st.markdown("### 📈 Data Visualizations")

    # Use the results directly from session_state for plotting
    current_results_df = pd.DataFrame(st.session_state['gene_search_results'])
    original_pathways_for_plot = st.session_state['original_pathways']
    original_go_terms_for_plot = st.session_state['original_go_terms']

    # --- Plot 1: Detailed Gene Ontology (GO) Term Analysis (Three Pie Charts) ---
    if original_go_terms_for_plot is not None and not original_go_terms_for_plot.isnull().all().all():
        st.markdown("#### Gene Ontology (GO) Term Analysis")

        go_terms_by_category = defaultdict(list)
        for entry in original_go_terms_for_plot.dropna():
            for term_entry in entry.split(';'):
                term_entry = term_entry.strip()
                if ':' in term_entry:
                    category, term_name = term_entry.split(':', 1)
                    go_terms_by_category[category.strip()].append(term_name.strip())
        
        go_categories_order = ["Biological Process", "Cellular Component", "Molecular Function"]

        for category in go_categories_order: # Iterate through categories for vertical display
            st.subheader(f" {category}")

            # --- Per-Plot Customization Options for GO Terms ---
            st.markdown("##### Plot Settings")
            # Using columns for horizontal alignment of settings within each vertical plot section
            col_go_h, col_go_f, col_go_c, col_go_legend = st.columns(4) # Added a column for legend toggle
            with col_go_h:
                go_plot_height = st.slider(f"Height ({category})", min_value=300, max_value=800, value=400, step=50, key=f"go_plot_height_{category}")
            with col_go_f:
                go_font_family = st.selectbox(f"Font ({category})", ["Arial", "Courier New", "Open Sans", "Roboto", "Times New Roman", "Verdana"], index=0, key=f"go_font_family_{category}")
            with col_go_c:
                go_colorscale_choice = st.selectbox(f"Color ({category})",
                                                    ['PlotlyDefault', 'Plasma', 'Viridis', 'Cividis', 'Magma',
                                                    'Inferno', 'Turbo', 'RdBu', 'Portland', 'Jet'],
                                                    index=0, key=f"go_colorscale_choice_{category}")
            with col_go_legend: # New legend toggle
                go_show_legend = st.checkbox(f"Show Legend ({category})", value=True, key=f"go_show_legend_{category}")
            st.markdown("---") # Separator


            if category in go_terms_by_category and go_terms_by_category[category]:
                term_counts = pd.Series(go_terms_by_category[category]).value_counts().reset_index()
                term_counts.columns = ['Term', 'Count']
                max_terms_to_show = 10
                plot_df = term_counts.head(max_terms_to_show)

                fig_go_pie = px.pie(plot_df, values='Count', names='Term',
                                    title=f'Distribution of {category} Terms',
                                    hole=0.4,
                                    template="plotly_white",
                                    height=go_plot_height, # Use local height
                                    color_discrete_sequence=px.colors.sequential.__dict__.get(go_colorscale_choice, px.colors.sequential.Plotly3) if go_colorscale_choice != 'PlotlyDefault' else None
                                    )

                fig_go_pie.update_traces(textposition='outside', textinfo='percent+label',
                                         insidetextfont_color='black')
                fig_go_pie.update_layout(showlegend=go_show_legend, # Use local legend toggle
                                        margin=dict(l=20, r=20, t=50, b=20),
                                        font=dict(family=go_font_family) # Use local font family
                                        )
                st.plotly_chart(fig_go_pie, use_container_width=True) # Ensure it takes available width
            else:
                st.info(f"No detailed terms found for {category}.")
    else:
        st.info("No detailed GO term information found for plotting.")


    # --- Plot 2: Pathway Database Distribution ---
    if original_pathways_for_plot is not None and not original_pathways_for_plot.isnull().all().all():
        st.subheader("Distribution of Genes Across Pathway Databases")

        # --- Per-Plot Customization Options for Pathway Distribution ---
        st.markdown("##### Plot Settings (Pathway Distribution)")
        # Using columns for horizontal alignment of settings within this vertical plot section
        col_path_h, col_path_f, col_path_c, col_path_legend = st.columns(4) # Added a column for legend toggle
        with col_path_h:
            path_plot_height = st.slider("Height (Pathways)", min_value=300, max_value=800, value=400, step=50, key="path_plot_height")
        with col_path_f:
            path_font_family = st.selectbox("Font (Pathways)", ["Arial", "Courier New", "Open Sans", "Roboto", "Times New Roman", "Verdana"], index=0, key="path_font_family")
        with col_path_c:
            path_colorscale_choice = st.selectbox("Color (Pathways)",
                                                ['PlotlyDefault', 'Plasma', 'Viridis', 'Cividis', 'Magma',
                                                'Inferno', 'Turbo', 'RdBu', 'Portland', 'Jet'],
                                                index=0, key="path_colorscale_choice")
        with col_path_legend: # New legend toggle
            path_show_legend = st.checkbox("Show Legend (Pathways)", value=True, key="path_show_legend")
        st.markdown("---") # Separator


        pathway_db_counts = {}
        for entry in original_pathways_for_plot.dropna():
            for pathway_id_name in entry.split(';'):
                if ':' in pathway_id_name:
                    db_name = pathway_id_name.split(':')[0].strip()
                    pathway_db_counts[db_name] = pathway_db_counts.get(db_name, 0) + 1

        if pathway_db_counts:
            pathway_plot_df = pd.DataFrame(pathway_db_counts.items(), columns=["Pathway Database", "Number of Genes"])
            max_pathways_to_show = 10
            plot_df_pathways = pathway_plot_df.sort_values(by='Number of Genes', ascending=False).head(max_pathways_to_show)

            fig_pathway = px.pie(plot_df_pathways, values="Number of Genes", names="Pathway Database",
                                 title="Proportion of Genes per Pathway Database",
                                 template="plotly_white",
                                 hole=0.3,
                                 height=path_plot_height, # Use local height
                                 color_discrete_sequence=px.colors.sequential.__dict__.get(path_colorscale_choice, px.colors.sequential.Plotly3) if path_colorscale_choice != 'PlotlyDefault' else None
                                 )
            fig_pathway.update_traces(textposition='outside', textinfo='percent+label',
                                      insidetextfont_color='black')
            fig_pathway.update_layout(showlegend=path_show_legend, # Use local legend toggle
                                     margin=dict(l=20, r=20, t=50, b=20),
                                     font=dict(family=path_font_family) # Use local font family
                                     )
            st.plotly_chart(fig_pathway, use_container_width=True) # Ensure it takes available width
        else:
            st.info("No detailed pathway database information found for plotting.")
elif search_performed and not st.session_state['gene_search_results']:
    st.warning("No results found for the provided gene(s). Please try a different input.")

