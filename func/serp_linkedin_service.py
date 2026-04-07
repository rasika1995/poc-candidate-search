import serpapi
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_KEY")


def _build_linkedin_query(
    skills: List[str],
    location: str = "",
    experience: str = "",
    position: str = ""
) -> str:
    terms = []

    if position:
        terms.append(f'"{position}"')

    if skills:
        terms.extend([f'"{skill}"' for skill in skills])

    if experience:
        terms.append(f'"{experience}"')

    if location:
        terms.append(f'"{location}"')

    # Force Google to return LinkedIn profiles
    return f'site:linkedin.com/in {" ".join(terms)}'


def search_linkedin_profiles(
    skills: List[str],
    location: str = "",
    experience: str = "",
    position: str = "",
    page: int = 1,
    limit: int = 10
) -> Dict[str, Any]:

    client = serpapi.Client(api_key=SERP_API_KEY)

    query = _build_linkedin_query(skills, location, experience, position)

    start = (page - 1) * limit

    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "api_key": SERP_API_KEY,
        "start": start,
        "output": "json",
    }

    client = serpapi.Client(api_key=os.getenv("API_KEY"))

    search = client.search(params)
    results = search.get_dict()

    profiles = []

    # Extract profiles
    for result in results.get("organic_results", []):
        profiles.append({
            "name": result.get("title"),
            "linkedin_url": result.get("link"),
            "snippet": result.get("snippet")
        })

    # Extract pagination details
    pagination = results.get("pagination", {})

    return {
        "profiles": profiles,
        "pagination": pagination,
    }