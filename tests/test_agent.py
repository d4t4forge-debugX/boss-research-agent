import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.server"],
        env=None
    )

    print("🤖 Simulating Agent Session...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Verify tool discovery
            tools_response = await session.list_tools()
            print("\n📋 Discovered Tools:")
            for t in tools_response.tools:
                print(f"  • {t.name}: {t.description.strip()[:60]}...")

            # Test 1: arXiv
            q_arxiv = "graph neural networks drug discovery"
            print(f"\n⚡ Invoking 'search_arxiv' for: '{q_arxiv}'...")
            res_arxiv = await session.call_tool("search_arxiv", arguments={"query": q_arxiv, "max_results": 1})
            for c in res_arxiv.content:
                print(c.text)

            # Test 2: PubMed
            q_pubmed = "crispr gene therapy"
            print(f"\n⚡ Invoking 'search_pubmed' for: '{q_pubmed}'...")
            res_pubmed = await session.call_tool("search_pubmed", arguments={"query": q_pubmed, "max_results": 1})
            for c in res_pubmed.content:
                print(c.text)

if __name__ == "__main__":
    asyncio.run(main())
