from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.rag import query_kb
from app.llm import generate_answer
from app.escalation import should_escalate
from app.safety import check_risky_request

app = FastAPI()


class Question(BaseModel):
    query: str


@app.get("/")
def home():
    return FileResponse("static/index.html", media_type="text/html")


@app.post("/ask")
def ask(question: Question):
    query = question.query.strip()

    safety = check_risky_request(query)
    if safety["blocked"]:
        ticket_summary = (
            f"Issue summary:\n"
            f"- User question: {query}\n"
            f"- Response: Request blocked due to account/security policy\n"
            f"- Recommended next step: Route to IT administrator through approved verification process"
        )

        return {
            "answer": safety["message"],
            "escalate": True,
            "blocked": True,
            "videos": [],
            "ticket_summary": ticket_summary,
        }

    docs = query_kb(query)
    answer = generate_answer(query, docs)
    escalate = should_escalate(query, docs)

    query_lower = query.lower()
    videos = []

    # YouTube video suggestions
    if (
        ("iphone" in query_lower or "ios" in query_lower or "mail app" in query_lower)
        and ("email" in query_lower or "account" in query_lower or "mail" in query_lower)
    ):
        videos.append({
            "title": "How to add your work email on iPhone",
            "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1",
            "thumbnail": "https://img.youtube.com/vi/YOUR_VIDEO_ID_1/hqdefault.jpg"
        })

    if (
        "company portal" in query_lower
        or "intune" in query_lower
        or "compliant" in query_lower
        or "security requirements" in query_lower
        or "device not compliant" in query_lower
    ):
        videos.append({
            "title": "How to install Company Portal",
            "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_2",
            "thumbnail": "https://img.youtube.com/vi/YOUR_VIDEO_ID_2/hqdefault.jpg"
        })

    if (
        "authenticator" in query_lower
        or "mfa" in query_lower
        or "verification" in query_lower
        or "two-factor" in query_lower
        or "2fa" in query_lower
    ):
        videos.append({
            "title": "How to install Microsoft Authenticator",
            "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_3",
            "thumbnail": "https://img.youtube.com/vi/YOUR_VIDEO_ID_3/hqdefault.jpg"
        })

    if escalate:
        ticket_summary = (
            f"Issue summary:\n"
            f"- User question: {query}\n"
            f"- Guidance already provided: {answer}\n"
            f"- Suggested next step: IT support should review and assist directly"
        )
    else:
        ticket_summary = (
            f"Issue summary:\n"
            f"- User question: {query}\n"
            f"- Guidance already provided: {answer}"
        )

    return {
        "answer": answer,
        "escalate": escalate,
        "blocked": False,
        "videos": videos,
        "ticket_summary": ticket_summary,
    }
