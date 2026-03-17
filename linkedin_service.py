from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_KEY")


def search_linkedin_profiles(skill: str, location: str = "", offset: int = 0):
    """
    Fetch LinkedIn profiles dynamically using SerpAPI.
    Only offset is provided to determine the starting point of results.
    """
    query = f'site:linkedin.com/in "{skill}" {location}'
    profiles = []
    pagination = {}

    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "api_key": SERP_API_KEY,
        "start": offset  # Pagination offset
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract profiles
    for result in results.get("organic_results", []):
        profiles.append({
            "name": result.get("title"),
            "linkedin_url": result.get("link"),
            "snippet": result.get("snippet")
        })

    # Extract pagination details
    pagination = results.get("pagination", {})

    return {"profiles": profiles, "pagination": pagination}