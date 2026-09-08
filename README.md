# BOSS Research Agent Harness (MCP)

A modular Model Context Protocol (MCP) server providing scientific literature discovery and retrieval tools for terminal-based autonomous AI agents (Claude Code, Gemini CLI, BossConsole).

## Features
- **arXiv Paper Retrieval (`search_arxiv`)**: Searches papers across Computer Science, Artificial Intelligence, Quantitative Biology, Mathematics, and Physics.
- **NCBI PubMed Search (`search_pubmed`)**: Queries biomedical, pharmaceutical, and life sciences studies via NCBI Entrez e-utilities.
- **FastMCP Architecture**: Standard `stdio` transport compatible with any MCP client without opening network ports.

## Repository Layout
```text
boss-research-agent/
├── src/
│   ├── server.py        # FastMCP entry point
│   ├── arxiv_tool.py    # arXiv search implementation
│   └── pubmed_tool.py   # PubMed search implementation
├── tests/
│   └── test_agent.py    # In-memory agent simulation test
├── requirements.txt     # Python dependencies
└── README.md