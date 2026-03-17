from fastmcp import FastMCP
from linkedin_service import search_linkedin_profiles
from ranking_service import rank_candidates
import json

# Create MCP server
mcp = FastMCP("Candidate Search MCP")


@mcp.tool()
def search_best_linkedin_profiles(skills: list[str], location: str = "", offset: int = 10):
    """
    MCP tool to fetch top LinkedIn profiles based on skills & location.
    Does not store data.
    """
    # Fetch LinkedIn profiles dynamically
    result = search_linkedin_profiles(skill=" ".join(skills), location=location, offset=offset)
    profiles = result["profiles"]
    pagination = result["pagination"]

    # Rank candidates in memory
    ranked = rank_candidates(profiles, skills)

    # Return both ranked profiles and pagination details
    return json.dumps({"profiles": ranked, "pagination": pagination})


if __name__ == "__main__":
     # Run server with HTTP transport on port 8000
    mcp.run(transport="http", host="localhost", port=8000)