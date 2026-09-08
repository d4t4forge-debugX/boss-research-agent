import httpx

async def search_pubmed(query: str, max_results: int = 3) -> str:
    """Search NCBI PubMed for biomedical and life sciences literature."""
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
        search_res = await client.get(search_url, params=search_params)
        if search_res.status_code != 200:
            return f"Error: Received HTTP {search_res.status_code} from PubMed search API"

        id_list = search_res.json().get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return f"No PubMed studies found for query: '{query}'"

        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json",
        }
        summary_res = await client.get(summary_url, params=summary_params)
        if summary_res.status_code != 200:
            return f"Error: Received HTTP {summary_res.status_code} from PubMed summary API"

        result_dict = summary_res.json().get("result", {})

    output = []
    for idx, pmid in enumerate(id_list, 1):
        doc = result_dict.get(pmid, {})
        title = doc.get("title", "No title").strip()
        source = doc.get("source", "Unknown journal").strip()
        pubdate = doc.get("pubdate", "Unknown date").strip()
        authors_raw = doc.get("authors", [])
        authors = ", ".join([a.get("name", "") for a in authors_raw[:3]]) if authors_raw else "Not listed"

        output.append(
            f"[{idx}] {title}\n"
            f"    Authors: {authors}\n"
            f"    Journal: {source}\n"
            f"    Date: {pubdate}\n"
            f"    PMID: {pmid}\n"
            f"    Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}/\n"
        )

    return "\n".join(output)
