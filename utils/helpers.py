def search_gene_function(gene_id):
    # Placeholder logic — we can replace this with real API calls or models later
    dummy_data = {
        "BRCA1": {
            "function": "DNA repair",
            "pathway": "Homologous recombination",
            "disease": "Breast cancer"
        },
        "TP53": {
            "function": "Tumor suppressor",
            "pathway": "Cell cycle regulation",
            "disease": "Various cancers"
        },
        "EGFR": {
            "function": "Growth factor receptor",
            "pathway": "EGFR signaling pathway",
            "disease": "Lung cancer"
        }
    }
    return dummy_data.get(gene_id.upper())
