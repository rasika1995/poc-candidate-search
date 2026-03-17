from fastmcp import FastMCP
from linkedin_service import search_linkedin_profiles
from ranking_service import rank_candidates

# Create MCP server
mcp = FastMCP("Candidate Search MCP")


@mcp.tool()
def search_best_linkedin_profiles(skills: list[str], location: str = "", limit: int = 10):
    """
    MCP tool to fetch top LinkedIn profiles based on skills & location.
    Does not store data.
    """
    # Fetch LinkedIn profiles dynamically
    profiles = search_linkedin_profiles(skill=" ".join(skills), location=location, limit=limit)

    # Rank candidates in memory
    ranked = rank_candidates(profiles, skills)

    # Return top 'limit' profiles
    return ranked[:limit]


if __name__ == "__main__":
     # Run server with HTTP transport on port 8000
    mcp.run(transport="http", host="localhost", port=8000)