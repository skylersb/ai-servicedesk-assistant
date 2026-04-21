def check_risky_request(query: str) -> dict:
    q = query.lower().strip()

    risky_patterns = [
        "coworker password",
        "co-worker password",
        "someone else's password",
        "someone elses password",
        "another person's password",
        "another persons password",
        "change my coworker",
        "reset my coworker",
        "reset someone else's",
        "reset someone elses",
        "access someone else's",
        "access someone elses",
        "bypass mfa",
        "disable mfa",
        "turn off mfa for",
        "login as another user",
        "log in as another user",
        "impersonate",
        "hack",
        "phish",
        "steal credentials",
    ]

    blocked = any(pattern in q for pattern in risky_patterns)

    if blocked:
        return {
            "blocked": True,
            "message": (
                "I can’t help with accessing, changing, or bypassing another person’s "
                "account, credentials, or security settings. If this is a legitimate "
                "business need, please contact your IT administrator and follow your "
                "company’s approved process."
            ),
        }

    return {
        "blocked": False,
        "message": "",
    }