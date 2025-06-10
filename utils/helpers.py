import requests

def search_gene_function(gene_symbol):
    url = "https://mygene.info/v3/query"
    params = {
        "q": gene_symbol,
        "species": "human",
        "fields": "symbol,name,summary,entrezgene,uniprot,pathway,go,pharmgkb,taxid"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("hits"):
            return None

        hit = data["hits"][0]

        # Parse UniProt Swiss-Prot entry properly
        swiss_prot = hit.get("uniprot", {}).get("Swiss-Prot") if isinstance(hit.get("uniprot"), dict) else None
        if isinstance(swiss_prot, list):
            swiss_prot = ', '.join(swiss_prot)

        # Flatten pathway database names and IDs
        pathway_data = hit.get("pathway")
        pathway_info_list = []
        if isinstance(pathway_data, dict):
            for db, pathways in pathway_data.items():
                if isinstance(pathways, list):
                    for p in pathways:
                        if isinstance(p, dict) and "id" in p:
                            pathway_info_list.append(f"{db}:{p['id']}")
                elif isinstance(pathways, dict) and "id" in pathways:
                    pathway_info_list.append(f"{db}:{pathways['id']}")
        
        pathway_info = "; ".join(pathway_info_list) if pathway_info_list else "Not available"


        # --- MODIFICATION START: Flatten GO terms to include category and term name ---
        go_data = hit.get("go", {})
        flattened_go_terms = []
        # Mapping from MyGene.info API keys to display names
        go_category_mapping = {
            "BP": "Biological Process",
            "CC": "Cellular Component",
            "MF": "Molecular Function"
        }

        for category_key, category_display_name in go_category_mapping.items():
            if category_key in go_data:
                terms_list_or_dict = go_data[category_key]
                if isinstance(terms_list_or_dict, list):
                    for term_obj in terms_list_or_dict:
                        if isinstance(term_obj, dict) and "term" in term_obj:
                            # Store as "CategoryDisplayName:Term Name" for easier parsing in main.py
                            flattened_go_terms.append(f"{category_display_name}:{term_obj['term']}")
                elif isinstance(terms_list_or_dict, dict) and "term" in terms_list_or_dict:
                    # Handle cases where a category might have a single term returned as a dict
                    flattened_go_terms.append(f"{category_display_name}:{terms_list_or_dict['term']}")

        go_terms_string = "; ".join(flattened_go_terms) if flattened_go_terms else "Not available"
        # --- MODIFICATION END ---

        result = {
            "gene_symbol": hit.get("symbol"),
            "name": hit.get("name"),
            "function": hit.get("summary", "Function info not available."),
            "pathway": pathway_info,
            "go_terms": go_terms_string, # Now it's a string like "Biological Process:term1; Cellular Component:termA"
            "pharmgkb": hit.get("pharmgkb", "Not available"),
            "entrez_id": hit.get("entrezgene"),
            "uniprot": swiss_prot,
            "taxid": hit.get("taxid")
        }

        return result

    except Exception as e:
        print(f"Error fetching gene info: {e}")
        return None
