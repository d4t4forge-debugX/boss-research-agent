import httpx
import xmltodict

async def search_arxiv(query: str, max_results: int = 3) -> str:
    """Search arXiv for research papers by keywords or topic."""
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        return f"Error: Received HTTP {response.status_code} from arXiv API"

    data = xmltodict.parse(response.text)
    entries = data.get("feed", {}).get("entry", [])

    if not entries:
        return f"No arXiv papers found for query: '{query}'"

    if isinstance(entries, dict):
        entries = [entries]

    results = []
    for idx, entry in enumerate(entries, 1):
        title = entry.get("title", "").replace("\n", " ").strip()
        published = entry.get("published", "")[:10]
        paper_id = entry.get("id", "").strip()
        summary = entry.get("summary", "").replace("\n", " ").strip()

        raw_authors = entry.get("author", [])
        if isinstance(raw_authors, list):
            authors = ", ".join([a.get("name", "") for a in raw_authors[:3]])
        else:
            authors = raw_authors.get("name", "")

        results.append(
            f"[{idx}] {title}\n"
            f"    Authors: {authors}\n"
            f"    Date: {published}\n"
            f"    URL: {paper_id}\n"
            f"    Abstract: {summary}\n"
        )

    return "\n".join(results)
