import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_KEY")


def search_linkedin_profiles(skill: str, location: str = "", limit: int = 10):
    """
    Fetch LinkedIn profiles dynamically using SerpAPI.
    """
    query = f'site:linkedin.com/in "{skill}" {location}'
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": limit
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    data = response.json()

    profiles = []
    for result in data.get("organic_results", [])[:limit]:
        profiles.append({
            "name": result.get("title"),
            "linkedin_url": result.get("link"),
            "snippet": result.get("snippet")
        })

    return profiles