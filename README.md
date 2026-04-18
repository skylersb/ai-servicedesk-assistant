# AI ServiceDesk Assistant

AI ServiceDesk Assistant is a portfolio project demonstrating an employee-facing IT support assistant built using a Retrieval-Augmented Generation (RAG) architecture.

It helps employees quickly resolve common IT issues through guided self-service support, while safely escalating more complex problems with structured, ticket-ready summaries.

---

## 🚀 Overview

This project simulates an internal AI-powered service desk assistant that:

- Retrieves relevant knowledge base content
- Provides clear, step-by-step IT support guidance
- Blocks unsafe or unauthorized requests
- Suggests helpful training videos
- Generates escalation-ready ticket summaries
- Delivers a clean, chat-style support experience
- Supports multiple LLM providers with Claude enabled by default

The goal is to reduce repetitive IT tickets while improving the employee support experience.

---

## 🔑 Key Features

- 💬 Chat-based support interface
- 🧠 RAG-style knowledge retrieval (TF-IDF + cosine similarity)
- 🤖 Dual-LLM support (Anthropic Claude + OpenAI ChatGPT)
- 🛑 Security-aware refusal handling for risky requests
- 📄 Automatic ticket summary generation
- 📋 Copyable escalation summaries
- 🎥 Contextual training video recommendations
- ⚡ Quick prompt buttons for common issues
- 🎯 Simple, user-friendly support experience

---

## 🧠 Example Use Cases

- Fix Outlook sign-in issues
- Reset password or login access
- Add work email to iPhone
- Install Microsoft Authenticator
- Resolve device compliance issues

---

## 🏗 Architecture

```text
Frontend (HTML / CSS / JavaScript)
        ↓
FastAPI Backend (main.py)
        ↓
RAG Engine (rag.py)
        ↓
LLM Response Generation (llm.py)
        ↓
Safety Filtering (safety.py)
        ↓
Escalation Logic (escalation.py)
```

---

## 🧰 Tech Stack

- Python 3.10
- FastAPI
- Uvicorn
- scikit-learn (TF-IDF + cosine similarity)
- python-dotenv
- Anthropic API
- OpenAI API
- HTML / CSS / JavaScript

---

## 📦 Project Structure

```text
ai_servicedesk_assistant/
│
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── llm.py
│   ├── escalation.py
│   └── safety.py
│
├── static/
│   └── index.html
│
├── knowledge_base/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-servicedesk-assistant.git
cd ai-servicedesk-assistant
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the root directory with:

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

## 🔄 Switching LLM Providers

This project supports both Anthropic and OpenAI.

### Default provider

Claude is the default active provider in v1:

```env
LLM_PROVIDER=anthropic
```

### Switch to OpenAI

Update your `.env` file to:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

---

## ⚠️ Current Status (v1)

This repository represents a **v1 MVP** focused on demonstrating core functionality and product thinking.

### Included in v1

- Employee-facing AI service desk assistant
- Knowledge base retrieval system
- Human-friendly response generation
- Anthropic Claude as the default active LLM
- OpenAI ChatGPT as an alternate LLM option
- Escalation workflow with structured summaries
- Safety handling for sensitive requests
- Training video support
- Chat-style UI

### Planned for Future Versions

- Live ticketing platform integration (Zendesk / Jira / ServiceNow)
- User identity capture (name + work email)
- Microsoft 365 / Entra authentication
- Role-based and context-aware responses
- Expanded knowledge ingestion
- Admin-facing companion system: **IT Ops Copilot (RAG)**

---

## 🎯 Design Philosophy

This project was built with a focus on:

- **Reducing repetitive IT tickets**
- **Improving employee self-service support**
- **Maintaining security boundaries in AI responses**
- **Providing clear escalation pathways when needed**
- **Keeping the architecture flexible across LLM providers**
- **Delivering a simple, intuitive user experience**

---

## 🧭 Future Improvements

Planned enhancements to extend this system toward a more production-ready solution:

- Integrate with ticketing platforms (Zendesk, Jira, ServiceNow)
- Capture user identity (name + work email) for real ticket creation
- Add Microsoft 365 / Entra ID authentication
- Expand knowledge base ingestion and retrieval accuracy
- Introduce role-based and context-aware responses
- Build an admin-facing assistant: **IT Ops Copilot (RAG)** for internal troubleshooting workflows

These improvements reflect how this type of system could evolve in a real-world IT environment.

---

## 📌 Notes

- This version simulates escalation (no live ticketing integration yet)
- Designed for demonstration, learning, and portfolio use
- Claude is the default active LLM in v1
- OpenAI support is included as an alternate provider
- Production versions would include authentication, integrations, and multi-tenant support

---

## 💡 Portfolio Value

This project demonstrates:

- Practical implementation of RAG architecture
- Multi-provider LLM integration
- AI-assisted support workflow design
- Safe handling of sensitive IT scenarios
- Full-stack prototyping with FastAPI and frontend UI
- Product thinking applied to real-world internal tools
