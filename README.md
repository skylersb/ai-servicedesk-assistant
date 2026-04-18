# AI ServiceDesk Assistant

> AI-powered internal IT support system with RAG, guided
> troubleshooting, and escalation workflows.

------------------------------------------------------------------------

## 🚀 What It Does (End-to-End Flow)

### 🖥️ Clean UI Experience

Modern chat-style interface for internal IT support.

### 💬 Ask Questions → Get Real Answers

Users can ask real IT issues and receive structured, step-by-step
guidance.

### 🎥 Helpful Training Videos

Relevant YouTube walkthroughs are embedded directly into responses when
helpful.

### 🚨 Escalation Flow

If an issue isn't resolved: - Ticket is created - Context is preserved -
Ready for Tier 2 support

------------------------------------------------------------------------

## 🧠 What This Demonstrates

**This project focuses on practical, real-world AI application --- not
just model usage, but workflow design.**

-   Retrieval-Augmented Generation (RAG)
-   Knowledge base design (real IT scenarios)
-   AI + UX integration
-   Escalation logic / support workflows
-   Safety + grounded responses
-   API integration (YouTube + LLM)

------------------------------------------------------------------------

## 🧠 System Architecture

-   User query → FastAPI backend
-   Retrieval from internal knowledge base (RAG)
-   LLM generates grounded response
-   Optional YouTube video enrichment
-   Escalation creates structured support ticket

Designed to simulate a real Tier 1 → Tier 2 IT support pipeline.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   Python (FastAPI)
-   HTML / CSS (custom UI)
-   OpenAI API
-   YouTube API
-   Local knowledge base (TXT docs)

------------------------------------------------------------------------

## ⚙️ Run Locally

``` bash
git clone https://github.com/skylersb/ai-servicedesk-assistant
cd ai-servicedesk-assistant
pip install -r requirements.txt
```

Create a `.env` file:

    OPENAI_API_KEY=your_key_here
    YOUTUBE_API_KEY=your_key_here

Run the app:

``` bash
uvicorn app.main:app --reload
```

Open:

    http://127.0.0.1:8000

------------------------------------------------------------------------

## 🎯 Why This Project Matters

This project simulates what a real internal IT support tool could look
like:

-   Reduces ticket volume
-   Improves employee self-service
-   Provides consistent, accurate guidance
-   Bridges Tier 1 → Tier 2 support

------------------------------------------------------------------------

## 👤 Author

Skyler Blood\
Building systems at the intersection of AI, automation, and
human-centered design.
