# utils/helpers.py

from biothings_client import get_client

def search_gene_function(gene_id):
    """
    Queries MyGene.info to fetch gene function, pathway, and disease-related information.
    """
    mg = get_client('gene')

    try:
        # Search the gene symbol
        res = mg.query(gene_id, species='human', fields='symbol,name,summary,pathway')

        if res and res['hits']:
            hit = res['hits'][0]
            gene_symbol = hit.get('symbol', '')
            gene_name = hit.get('name', '')
            summary = hit.get('summary', '')
            pathway = hit.get('pathway', {})

            return {
                "symbol": gene_symbol,
                "name": gene_name,
                "function": summary,
                "pathway": pathway if pathway else "Not available",
                "disease": "To be integrated"  # Placeholder for next step
            }
        else:
            return None

    except Exception as e:
        return {"error": str(e)}
