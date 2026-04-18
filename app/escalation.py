def should_escalate(query, docs):
    risky_keywords = [
        "compromised",
        "breach",
        "security",
        "admin",
        "urgent",
        "phishing",
        "malware",
        "ransomware",
        "privileged",
        "locked out",
        "can't sign in",
        "cannot sign in"
    ]

    query_lower = query.lower()

    if any(word in query_lower for word in risky_keywords):
        return True

    if not docs:
        return True

    if docs[0]["score"] < 0.18:
        return True

    return False