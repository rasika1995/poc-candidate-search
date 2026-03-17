def rank_candidates(profiles, required_skills):
    """
    Simple scoring: add 10 points for each skill match in snippet.
    """
    ranked = []
    for profile in profiles:
        score = 0
        text = (profile.get("snippet") or "").lower()
        for skill in required_skills:
            if skill.lower() in text:
                score += 10
        profile["score"] = score
        ranked.append(profile)

    # Sort profiles by score in descending order
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked