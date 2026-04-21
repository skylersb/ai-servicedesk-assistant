import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").strip().lower()


def _build_context(docs: list[dict[str, Any]]) -> str:
    if not docs:
        return "No relevant internal documents were found."

    sections = []
    for doc in docs:
        sections.append(
            f"Source: {doc.get('source', 'unknown')}\n"
            f"Content:\n{doc.get('content', '')}"
        )
    return "\n\n---\n\n".join(sections)


def _fallback_answer(query: str, docs: list[dict[str, Any]]) -> str:
    if not docs:
        return (
            "Answer:\n"
            "I couldn’t find a matching internal support article for that issue.\n\n"
            "Steps:\n"
            "1. Review the issue details\n"
            "2. Try basic troubleshooting steps\n"
            "3. Contact IT support if the issue continues\n\n"
            "Troubleshooting:\n"
            "- No matching article → escalate to IT\n\n"
            "Escalation:\n"
            "Please escalate this issue to IT support so a team member can review it."
        )

    return docs[0]["content"].strip()


def _fallback_ticket_summary(
    query: str,
    answer: str,
    user_name: str,
    user_email: str,
    blocked: bool = False,
) -> str:
    requested_action = (
        "Route to IT administrator through approved verification process"
        if blocked
        else "Review issue and assist user directly"
    )

    return (
        f"Ticket Summary\n\n"
        f"User: {user_name}\n"
        f"Email: {user_email}\n\n"
        f"Issue:\n"
        f"{query}\n\n"
        f"Steps Attempted:\n"
        f"- User asked the AI ServiceDesk Assistant for help\n"
        f"- Assistant provided initial troubleshooting guidance\n\n"
        f"Requested Action:\n"
        f"{requested_action}"
    )



def generate_answer(query: str, docs: list[dict[str, Any]]) -> str:
    provider = LLM_PROVIDER
    context = _build_context(docs)

    system_prompt = (
        "You are an internal IT service desk assistant. "
        "Use only the provided internal documentation context to answer the user's question. "
        "Do not mention sources, confidence scores, retrieval, or internal documentation. "
        "Do not repeat raw knowledge-base fields like Title, Problem, or Applies To. "
        "Write in a clear, practical Tier 1 IT support style for a non-technical employee. "
        "Prioritize action over explanation. "
        "Start with one short helpful sentence. "
        "Then provide only the steps the user should actually take. "
        "Keep troubleshooting concise and only include it if helpful. "
        "Only include escalation guidance when it is genuinely needed. "
        "Respond using this exact structure:\n\n"
        "Answer:\n"
        "<short explanation>\n\n"
        "Steps:\n"
        "1. <step>\n"
        "2. <step>\n"
        "3. <step>\n\n"
        "Troubleshooting:\n"
        "- <issue> → <fix>\n"
        "- <issue> → <fix>\n\n"
        "Escalation:\n"
        "<when to contact IT>\n\n"
        "Keep the response concise, actionable, and easy for an employee to follow."
    )

    user_prompt = (
        f"User question:\n{query}\n\n"
        f"Internal documentation context:\n{context}\n\n"
        "Generate the support response now."
    )

    try:
        if provider == "anthropic":
            from anthropic import Anthropic

            api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
            if not api_key:
                return _fallback_answer(query, docs)

            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            text_parts = []
            for block in response.content:
                if getattr(block, "type", "") == "text":
                    text_parts.append(block.text)

            answer = "\n".join(text_parts).strip()
            return answer or _fallback_answer(query, docs)

        if provider == "openai":
            from openai import OpenAI

            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            if not api_key:
                return _fallback_answer(query, docs)

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=500,
            )

            answer = response.choices[0].message.content.strip()
            return answer or _fallback_answer(query, docs)

        return _fallback_answer(query, docs)

    except Exception:
        return _fallback_answer(query, docs)



def generate_ticket_summary(
    query: str,
    answer: str,
    user_name: str,
    user_email: str,
    blocked: bool = False,
) -> str:
    provider = LLM_PROVIDER

    system_prompt = (
        "You are generating an internal IT ticket summary. "
        "Return only plain text. "
        "Use this exact structure:\n\n"
        "Ticket Summary\n\n"
        "User: <name>\n"
        "Email: <email>\n\n"
        "Issue:\n"
        "<short issue summary>\n\n"
        "Steps Attempted:\n"
        "- <bullet>\n"
        "- <bullet>\n\n"
        "Requested Action:\n"
        "<short action request>\n\n"
        "Keep it concise, realistic, and helpful for an IT support technician."
    )

    blocked_note = (
        "This request was blocked due to account/security policy."
        if blocked
        else "This request received an initial AI troubleshooting answer."
    )

    user_prompt = (
        f"User name: {user_name}\n"
        f"User email: {user_email}\n"
        f"Original user question: {query}\n"
        f"Assistant answer: {answer}\n"
        f"Context note: {blocked_note}\n\n"
        "Generate the ticket summary now."
    )

    try:
        if provider == "anthropic":
            from anthropic import Anthropic

            api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
            if not api_key:
                return _fallback_ticket_summary(query, answer, user_name, user_email, blocked)

            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
                max_tokens=350,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            text_parts = []
            for block in response.content:
                if getattr(block, "type", "") == "text":
                    text_parts.append(block.text)

            summary = "\n".join(text_parts).strip()
            return summary or _fallback_ticket_summary(query, answer, user_name, user_email, blocked)

        if provider == "openai":
            from openai import OpenAI

            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            if not api_key:
                return _fallback_ticket_summary(query, answer, user_name, user_email, blocked)

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=350,
            )

            summary = response.choices[0].message.content.strip()
            return summary or _fallback_ticket_summary(query, answer, user_name, user_email, blocked)

        return _fallback_ticket_summary(query, answer, user_name, user_email, blocked)

    except Exception:
        return _fallback_ticket_summary(query, answer, user_name, user_email, blocked)