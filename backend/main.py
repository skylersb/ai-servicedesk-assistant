from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.rag import query_kb
from backend.llm import generate_answer, generate_ticket_summary
from backend.escalation import should_escalate
from backend.safety import check_risky_request

app = FastAPI(title="AI ServiceDesk Assistant")

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")


class UserContext(BaseModel):
    name: str
    email: str


class Question(BaseModel):
    query: str
    user: UserContext


@app.get("/")
def home() -> FileResponse:
    return FileResponse("frontend/index.html", media_type="text/html")


@app.post("/ask")
def ask(question: Question) -> dict:
    query = question.query.strip()
    user_name = question.user.name.strip()
    user_email = question.user.email.strip()

    safety = check_risky_request(query)
    if safety["blocked"]:
        ticket_summary = generate_ticket_summary(
            query=query,
            answer=safety["message"],
            user_name=user_name,
            user_email=user_email,
            blocked=True,
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
    escalate = should_escalate(query, docs, answer)

    query_lower = query.lower()
    videos: list[dict[str, str]] = []

    if (
        ("iphone" in query_lower or "ios" in query_lower or "mail app" in query_lower)
        and ("email" in query_lower or "account" in query_lower or "mail" in query_lower)
    ):
        videos.append(
            {
                "title": "How to add your work email on iPhone",
                "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1",
                "thumbnail": "https://img.youtube.com/vi/YOUR_VIDEO_ID_1/hqdefault.jpg",
            }
        )

    if (
        "company portal" in query_lower
        or "intune" in query_lower
        or "compliant" in query_lower
        or "security requirements" in query_lower
        or "device not compliant" in query_lower
    ):
        videos.append(
            {
                "title": "How to install Company Portal",
                "url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_2",
                "thumbnail": "https://img.youtube.com/vi/YOUR_VIDEO_ID_2/hqdefault.jpg",
            }
        )

    if (
        "authenticator" in query_lower
        or "mfa" in query_lower
        or "verification" in query_lower
        or "two-factor" in query_lower
        or "2fa" in query_lower
    ):
        videos.append(
            {
                "title": "How to install Microsoft Authenticator",
                "url": "https://www.youtube.com/watch?v=Ze5OptuFeXo",
                "thumbnail": "https://img.youtube.com/vi/Ze5OptuFeXo/hqdefault.jpg",
            }
        )

    ticket_summary = generate_ticket_summary(
        query=query,
        answer=answer,
        user_name=user_name,
        user_email=user_email,
        blocked=False,
    )

    return {
        "answer": answer,
        "escalate": escalate,
        "blocked": False,
        "videos": videos,
        "ticket_summary": ticket_summary,
    }