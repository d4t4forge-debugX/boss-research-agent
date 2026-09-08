from mcp.server.fastmcp import FastMCP
from src.arxiv_tool import search_arxiv as arxiv_fn
from src.pubmed_tool import search_pubmed as pubmed_fn

mcp = FastMCP("BossResearchAgent")

@mcp.tool()
async def search_arxiv(query: str, max_results: int = 3) -> str:
    """Search arXiv for papers (AI, CS, Math, Physics) by topic or keywords."""
    return await arxiv_fn(query, max_results)

@mcp.tool()
async def search_pubmed(query: str, max_results: int = 3) -> str:
    """Search PubMed for biomedical, pharmaceutical, and health literature."""
    return await pubmed_fn(query, max_results)

if __name__ == "__main__":
    mcp.run(transport="stdio")
