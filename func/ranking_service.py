from typing import List, Dict, Any


def rank_candidates_profiles(profiles: List[Dict[str, Any]], required_skills: List[str], location: str = "", experience: str = "", position: str = "") -> List[Dict[str, Any]]:
    """Rank profiles by skills plus context hints (location/experience/position)."""
    ranked = []
    skill_tokens = [s.lower() for s in required_skills]
    location_lower = location.lower() if location else ""
    experience_lower = experience.lower() if experience else ""
    position_lower = position.lower() if position else ""

    for profile in profiles:
        score = 0
        text = (profile.get("snippet", "") + " " + profile.get("headline", "") + " " + profile.get("summary", "") + " " + profile.get("position", "")).lower()

        for skill in skill_tokens:
            if skill and skill in text:
                score += 10

        if location_lower and location_lower in (profile.get("location", "") or "").lower():
            score += 20

        if position_lower and position_lower in (profile.get("position", "") or "").lower():
            score += 15

        if experience_lower and experience_lower in (profile.get("experience", "") or "").lower():
            score += 10

        profile_copy = dict(profile)
        profile_copy["score"] = score
        ranked.append(profile_copy)

    ranked.sort(key=lambda p: p.get("score", 0), reverse=True)
    return ranked
