from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from func.serp_linkedin_service import search_linkedin_profiles
from func.ranking_service import rank_candidates_profiles

mcp = FastMCP("Candidate Search MCP")

@mcp.tool()
def search_profiles(skills: List[str], location: str = "", experience: Optional[str] = None, position: Optional[str] = None, page: int = 1, limit: int = 10):
    """Search tool used by JSON workflow steps."""
    # Pass the full parameters to the LinkedIn tool by skills/location/experience/position
    result = search_linkedin_profiles(
        skills=skills,
        location=location,
        experience=experience or "",
        position=position or "",
        limit=limit,
        page=page
    )

    return result


@mcp.tool()
def rank_profiles(
    profiles: List[Dict[str, Any]],
    skills: List[str],
    location: Optional[str] = None,
    experience: Optional[str] = None,
    position: Optional[str] = None
):
    """Ranking tool used by JSON workflow steps with optional context.
    If pre_ranked=True, uses passed profiles as base ranked results."""
    
    ranked = rank_candidates_profiles(
        profiles=profiles,
        required_skills=skills,
        location=location or "",
        experience=experience or "",
        position=position or ""
    )
    return ranked

@mcp.tool()
def find_best_candidates(
    skills: List[str],
    location: str = "",
    experience: Optional[str] = None,
    position: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    """
    High-level tool to search and rank candidates based on job criteria.
    """

    # Step 1: Search candidates
    search_result = search_profiles(
        skills=skills,
        location=location,
        experience=experience,
        position=position,
        page=page,
        limit=limit
    )

    profiles = search_result.get("profiles", [])

    # Step 2: Rank candidates
    ranked_candidates = rank_profiles(
        profiles=profiles,
        skills=skills,
        location=location,
        experience=experience,
        position=position
    )

    return {
        "candidates": ranked_candidates,
        "pagination": search_result.get("pagination", {})
    }

if __name__ == "__main__":
    # Defaults to STDIO transport
    mcp.run()
    # Run server with HTTP transport on port 8000
    # mcp.run(transport="http", host="localhost", port=8000)