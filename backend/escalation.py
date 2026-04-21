from typing import Any


def should_escalate(query: str, docs: list[dict[str, Any]], answer: str) -> bool:
    query_lower = query.lower()

    escalation_keywords = [
        "locked out",
        "still not working",
        "didn't work",
        "doesn't work",
        "not working",
        "can't sign in",
        "cannot sign in",
        "account locked",
        "administrator",
        "admin",
        "urgent",
        "escalate",
        "manager",
        "security issue",
        "breach",
        "phishing",
    ]

    if any(keyword in query_lower for keyword in escalation_keywords):
        return True

    if not docs:
        return True

    top_score = float(docs[0].get("score", 0.0))
    if top_score < 0.10:
        return True

    answer_lower = answer.lower()
    weak_answer_signals = [
        "couldn’t find",
        "could not find",
        "please escalate",
        "insufficient",
        "team member can review it",
    ]

    if any(signal in answer_lower for signal in weak_answer_signals):
        return True

    return False