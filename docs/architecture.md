# InfraPilot AI - System Architecture

## Overview

InfraPilot AI is an AI-powered Infrastructure Copilot designed to assist the Infrastructure team by providing intelligent access to company documentation, troubleshooting guidance, and incident reporting.

The application follows a client-server architecture with an AI-powered backend that uses Retrieval-Augmented Generation (RAG) and multiple AI agents to process user requests.

---

# High-Level Architecture

```
                         User
                           │
                           ▼
                Streamlit Frontend (UI)
                           │
                           ▼
                  FastAPI Backend (API)
                           │
                           ▼
                     Router Agent
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 Knowledge Agent   Diagnostics Agent   Incident Report Agent
          │                │                │
          ▼                ▼                ▼
     ChromaDB          Knowledge Base    PostgreSQL
          │
          ▼
     Company Documents
          │
          ▼
      Large Language Model
```

---

# System Components

## 1. Streamlit Frontend

The frontend provides a simple and user-friendly interface where authenticated users can:

- Ask infrastructure-related questions.
- Receive AI-generated responses.
- Generate incident reports.
- View previous conversations.

---

## 2. FastAPI Backend

The backend serves as the application's core.

Responsibilities include:

- Authentication
- Processing user requests
- Calling AI agents
- Managing databases
- Returning responses to the frontend

---

## 3. Router Agent

The Router Agent determines the user's intent and sends the request to the appropriate AI agent.

Possible intents include:

- Knowledge Retrieval
- Infrastructure Troubleshooting
- Incident Report Generation

---

## 4. Knowledge Agent

The Knowledge Agent uses Retrieval-Augmented Generation (RAG).

Responsibilities:

- Search company documentation.
- Retrieve relevant document sections.
- Provide accurate answers using retrieved context.
- Include document references where applicable.

---

## 5. Diagnostics Agent

The Diagnostics Agent assists engineers during troubleshooting.

Responsibilities:

- Analyze infrastructure symptoms.
- Suggest possible causes.
- Recommend troubleshooting steps.
- Reference relevant documentation.

---

## 6. Incident Report Agent

The Incident Report Agent generates standardized incident reports based on user input.

Reports can be stored for future reference.

---

# Databases

## PostgreSQL

Stores structured application data, including:

- User accounts
- Chat history
- Incident reports
- Application metadata

---

## ChromaDB

Stores vector embeddings created from company documentation.

These embeddings allow the Knowledge Agent to retrieve the most relevant information during question answering.

---

# Knowledge Base

The knowledge base may include:

- Infrastructure SOPs
- Runbooks
- Troubleshooting guides
- Infrastructure FAQs
- Incident report templates

---

# Request Flow

1. User logs into the application.
2. User submits a request.
3. FastAPI receives the request.
4. Router Agent determines the request type.
5. The request is sent to the appropriate AI agent.
6. If needed, the Knowledge Agent retrieves relevant documents from ChromaDB.
7. The Large Language Model generates a response using the retrieved context.
8. The response is returned to the frontend.
9. The interaction is stored in PostgreSQL (where applicable).

---

## Authentication & Authorization

InfraPilot AI uses JWT authentication and Role-Based Access Control (RBAC).

Two user roles are supported:

- Admin
- Engineer

Only administrators can manage the Knowledge Base.

Infrastructure Engineers can ask questions, use the Diagnostics Agent, and generate incident reports.

# Deployment

The application is designed to support deployment on the company's local server.

Possible deployment environments include:

- Windows Server
- Linux Server

The architecture is platform-independent to allow flexibility based on the organization's infrastructure.

---

# Future Enhancements

Possible future improvements include:

- Active Directory integration
- Monitoring tool integration
- Real-time infrastructure alerts
- Slack or Microsoft Teams integration
- Role-Based Access Control (RBAC)
- Local Large Language Models (LLMs)
- Infrastructure analytics dashboard