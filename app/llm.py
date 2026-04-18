import os
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI

load_dotenv()


def fallback_answer(query, docs):
    if not docs:
        return (
            "I couldn’t find a matching help article for this issue. "
            "Please escalate this to IT support so someone can help directly."
        )

    top_doc = docs[0]["content"].strip()

    return (
        f"{top_doc}\n\n"
        "If these steps don’t fix the problem, please escalate it to IT support."
    )


def generate_answer(query, docs):
    if not docs:
        return (
            "I couldn’t find a matching help article for this issue. "
            "Please escalate it to IT support."
        )

    context = "\n\n".join([f"Content: {d['content']}" for d in docs])

    # Default active provider for v1
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()

    try:
        # =========================
        # ACTIVE: Anthropic / Claude
        # =========================
        if provider == "anthropic":
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            response = client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=500,
                system=(
                    "You are a friendly internal IT help desk assistant.\n\n"
                    "Your job:\n"
                    "- answer in a calm, clear, human way\n"
                    "- give straightforward step-by-step guidance\n"
                    "- keep it simple for non-technical employees\n"
                    "- do not mention confidence scores\n"
                    "- do not mention source files or internal documentation names\n"
                    "- do not sound robotic\n"
                    "- if the issue seems unresolved or too complex, recommend escalation"
                ),
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"User question:\n{query}\n\n"
                            f"Knowledge base context:\n{context}"
                        ),
                    }
                ],
            )

            text_parts = []
            for block in response.content:
                if getattr(block, "type", None) == "text":
                    text_parts.append(block.text)

            final_text = "\n".join(text_parts).strip()
            if final_text:
                return final_text

            return fallback_answer(query, docs)

        # =========================
        # ALTERNATE: OpenAI / ChatGPT
        # To switch providers:
        # 1. Set LLM_PROVIDER=openai in .env
        # 2. Add OPENAI_API_KEY to .env
        # =========================
        elif provider == "openai":
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=(
                    "You are a friendly internal IT help desk assistant.\n\n"
                    "Your job:\n"
                    "- answer in a calm, clear, human way\n"
                    "- give straightforward step-by-step guidance\n"
                    "- keep it simple for non-technical employees\n"
                    "- do not mention confidence scores\n"
                    "- do not mention source files or internal documentation names\n"
                    "- do not sound robotic\n"
                    "- if the issue seems unresolved or too complex, recommend escalation\n\n"
                    f"User question:\n{query}\n\n"
                    f"Knowledge base context:\n{context}"
                ),
            )

            return response.output_text.strip()

        else:
            return fallback_answer(query, docs)

    except Exception:
        return fallback_answer(query, docs)