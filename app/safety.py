def check_risky_request(query: str):
    q = query.lower()

    risky_patterns = [
        "coworker password",
        "co worker password",
        "someone else's password",
        "someone else password",
        "another person's password",
        "another employee password",
        "change my coworker",
        "change my coworkers",
        "reset my coworker",
        "reset my coworkers",
        "access someone else's",
        "access someone else",
        "get into someone else's account",
        "get into another person's account",
        "log into someone else's email",
        "log into my coworker's email",
        "disable mfa for someone else",
        "bypass mfa",
        "bypass company portal",
        "remove security requirements",
        "impersonate",
        "without their permission"
    ]

    matched = any(pattern in q for pattern in risky_patterns)

    if matched:
        return {
            "blocked": True,
            "message": (
                "I can’t help with accessing, changing, or bypassing another person’s "
                "account, credentials, or security settings. If this is a legitimate business need, "
                "please contact your IT administrator and follow your company’s approved process."
            )
        }

    return {
        "blocked": False,
        "message": ""
    }