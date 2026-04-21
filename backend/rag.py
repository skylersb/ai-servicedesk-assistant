import os
import re
from pathlib import Path
from typing import Any


KB_DIR = Path("backend/knowledge_base")


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _load_docs() -> list[dict[str, Any]]:
    docs = []

    if not KB_DIR.exists():
        return docs

    for file_path in KB_DIR.glob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8").strip()
        except Exception:
            continue

        title = ""
        for line in content.splitlines():
            if line.strip().lower() == "title:":
                continue
            if title == "" and line.strip() and not line.strip().lower().endswith(":"):
                title = line.strip()
                break

        docs.append(
            {
                "source": file_path.name,
                "title": title,
                "content": content,
            }
        )

    return docs


def _intent_keywords(query: str) -> set[str]:
    q = query.lower()
    keywords: set[str] = set()

    if any(term in q for term in ["iphone", "ios", "mail app", "apple mail"]):
        keywords.update(["iphone", "ios", "mail", "exchange", "email"])

    if any(term in q for term in ["password", "reset password", "forgot password"]):
        keywords.update(["password", "reset", "signin"])

    if any(term in q for term in ["authenticator", "mfa", "2fa", "two-factor", "verification"]):
        keywords.update(["authenticator", "mfa", "verification", "security", "phone"])

    if any(term in q for term in ["outlook", "outlook sign-in", "outlook login"]):
        keywords.update(["outlook", "signin", "credentials", "office"])

    if any(term in q for term in ["teams", "compliance", "company portal", "intune"]):
        keywords.update(["teams", "compliance", "portal", "intune", "device"])

    return keywords


def _score_doc(query: str, doc: dict[str, Any]) -> float:
    query_lower = query.lower()
    query_tokens = set(_tokenize(query))
    boosted_tokens = query_tokens | _intent_keywords(query)

    source = doc.get("source", "").lower()
    title = doc.get("title", "").lower()
    content = doc.get("content", "").lower()

    score = 0.0

    # 1) Filename boost
    for token in boosted_tokens:
        if token and token in source:
            score += 8.0

    # 2) Title boost
    for token in boosted_tokens:
        if token and token in title:
            score += 6.0

    # 3) Content token overlap
    for token in boosted_tokens:
        if token and token in content:
            score += 2.0

    # 4) Strong phrase matches
    strong_phrases = [
        "set up email on iphone",
        "work email on iphone",
        "mail app on iphone",
        "microsoft authenticator",
        "reset password",
        "outlook sign-in",
        "teams mobile compliance",
    ]

    for phrase in strong_phrases:
        if phrase in query_lower and phrase in content:
            score += 12.0
        elif phrase in query_lower and phrase in title:
            score += 14.0
        elif phrase in query_lower and phrase in source:
            score += 16.0

    # 5) Special intent routing
    if any(term in query_lower for term in ["iphone", "ios", "mail app"]):
        if any(term in source for term in ["iphone", "ios", "mail", "email"]):
            score += 18.0
        if any(term in title for term in ["iphone", "ios", "mail", "email"]):
            score += 14.0

    if "authenticator" in query_lower or "mfa" in query_lower:
        if "authenticator" in source or "authenticator" in title:
            score += 18.0

    if "password" in query_lower:
        if "password" in source or "password" in title:
            score += 18.0

    if "outlook" in query_lower:
        if "outlook" in source or "outlook" in title:
            score += 18.0

    if "teams" in query_lower or "compliance" in query_lower:
        if any(term in source for term in ["teams", "compliance", "portal", "intune"]):
            score += 18.0

    # 6) Penalize bad-fit collisions
    if any(term in query_lower for term in ["iphone", "mail", "email"]) and "password_reset" in source:
        score -= 8.0

    if "password" in query_lower and "iphone_work_email_setup" in source:
        score -= 6.0

    return score


def query_kb(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    docs = _load_docs()
    if not docs:
        return []

    ranked = sorted(
        docs,
        key=lambda doc: _score_doc(query, doc),
        reverse=True,
    )

    # Keep only docs with some meaningful relevance
    filtered = [doc for doc in ranked if _score_doc(query, doc) > 0]

    return filtered[:top_k]