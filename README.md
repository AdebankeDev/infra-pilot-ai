# InfraPilot AI

## AI-Powered Infrastructure Copilot for Enterprise IT Operations

InfraPilot AI is an AI-powered Infrastructure Copilot developed to assist infrastructure engineers with internal knowledge retrieval, infrastructure troubleshooting, and incident reporting.

The system combines **Retrieval-Augmented Generation (RAG)** with a **LangGraph-based tool-calling agent** to provide conversational assistance grounded in company documentation.

Unlike a general-purpose AI chatbot, InfraPilot AI can determine when company-specific knowledge is required and invoke a `knowledge_lookup()` tool to retrieve relevant information from the organization's internal knowledge base before generating a response.

---

## Overview

Infrastructure engineers often spend significant time searching through Standard Operating Procedures (SOPs), administration guides, runbooks, and troubleshooting documentation when resolving operational issues.

InfraPilot AI provides a centralized conversational interface for accessing this knowledge.

The system can:

* Answer general questions.
* Retrieve company-specific infrastructure knowledge.
* Provide grounded responses based on internal documentation.
* Reference source documents and page numbers.
* Display associated screenshots from source documents.
* Maintain persistent multi-turn conversations.
* Manage the organization's knowledge base.
* Generate structured incident reports.

---

## System Architecture

```text
                         User
                           │
                           ▼
                 Streamlit Frontend
                           │
                           ▼
                    FastAPI Backend
                           │
                           ▼
              LangGraph Copilot Agent
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
           Direct LLM Response   knowledge_lookup()
                                      │
                                      ▼
                                  Retriever
                                      │
                                      ▼
                                  ChromaDB
                                      │
                                      ▼
                             Company Documents
                                      │
                                      ▼
                              Retrieved Context
                                      │
                                      ▼
                                  LLM Response
                                      │
                                      ▼
                             Grounded Response
                              + Source Metadata
                              + Screenshots


                         PostgreSQL
                    ┌────────┼────────┐
                    │        │        │
                  Users  Conversations Messages
                                      │
                                      ▼
                              Incident Reports
```

### Main Components

#### Streamlit Frontend

Provides the user interface for:

* Authentication.
* Conversational chat.
* Viewing previous conversations.
* Starting new conversations.
* Knowledge base management.
* Viewing retrieved sources and screenshots.
* Interacting with the Infrastructure Copilot.

#### FastAPI Backend

Provides the application's API and application services.

Responsibilities include:

* Authentication and authorization.
* Chat processing.
* Conversation persistence.
* Knowledge-base management.
* Document processing and indexing.
* Retrieval.
* AI agent execution.
* Incident report generation.

#### LangGraph Copilot Agent

InfraPilot AI uses a **single tool-calling agent** implemented with LangGraph.

The agent determines whether the user's request requires company-specific knowledge.

When knowledge retrieval is required, the agent invokes the `knowledge_lookup()` tool. Otherwise, it can respond directly using the configured LLM.

This design avoids unnecessary retrieval while allowing company-specific questions to be grounded in internal documentation.

#### ChromaDB

ChromaDB stores the vector representations of indexed company documentation and enables semantic retrieval of relevant document chunks.

#### PostgreSQL

PostgreSQL stores structured application data including:

* Users.
* Conversations.
* Messages.
* Incident reports.
* Document metadata.

#### Company Document Storage

Uploaded documents and extracted screenshots are stored using persistent Docker volumes.

---

# Retrieval-Augmented Generation

The knowledge base follows a document processing and retrieval pipeline.

```text
PDF Documents
     │
     ▼
Text & Image Extraction
     │
     ▼
Text Chunking
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB
     │
     ▼
Semantic Retrieval
     │
     ▼
Retrieved Context
     │
     ▼
LLM
     │
     ▼
Grounded Response
```

### Document Processing

When an administrator uploads a document, InfraPilot AI:

1. Extracts text from the PDF.
2. Extracts embedded screenshots/images.
3. Splits the extracted text into chunks.
4. Generates embeddings for the chunks.
5. Stores the embeddings in ChromaDB.
6. Stores metadata such as:

   * Document name.
   * Page number.
   * Associated screenshot paths.

This metadata allows retrieved information to be presented together with its original source.

---

# AI Knowledge Assistant

Users can ask infrastructure-related questions through the conversational interface.

For company-specific questions, the LangGraph agent can invoke:

```text
knowledge_lookup()
```

The retrieval tool searches the indexed company documentation and returns relevant context to the agent.

The LLM then generates a response based on the retrieved information.

This helps reduce unsupported answers to company-specific questions and makes responses more explainable.

---

# Visual Knowledge Retrieval

InfraPilot AI supports visual RAG.

When a retrieved document section contains relevant screenshots, the system can display the associated images alongside the generated response.

Sources can include:

* Source document.
* Page number.
* Associated screenshots.

This allows infrastructure engineers to verify procedures using the original documentation rather than relying solely on generated text.

---

# Conversational Chat

InfraPilot AI supports persistent multi-turn conversations.

Users can:

* Start a new conversation.
* Continue previous conversations.
* View previous conversations.
* Maintain conversation context.
* Access stored chat history.

Conversation data is persisted in PostgreSQL.

---

# Knowledge Base Management

Authorized administrators can manage the infrastructure knowledge base.

Supported operations include:

* Uploading documents.
* Processing documents.
* Indexing documents.
* Viewing indexed documents.
* Removing documents.

The indexed knowledge is stored in ChromaDB and can be retrieved by the Infrastructure Copilot.

---

# Incident Reporting

InfraPilot AI can generate structured incident reports using information from relevant conversations.

Incident reports are persisted in PostgreSQL for future reference.

---

# Authentication and Authorization

The application uses authenticated access to protect application functionality.

Authentication is implemented using:

* Supabase Authentication.
* JWT-based authenticated API requests.

Administrative functionality is restricted to authorized users.

---

# Technology Stack

| Component            | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Frontend             | Streamlit               |
| Backend              | FastAPI                 |
| Agent Framework      | LangGraph               |
| LLM Integration      | LangChain / OpenRouter  |
| Embeddings           | Sentence Transformers   |
| Vector Database      | ChromaDB                |
| Relational Database  | PostgreSQL              |
| Authentication       | Supabase Auth / JWT     |
| PDF Processing       | PyMuPDF / pdfplumber    |
| ORM                  | SQLAlchemy              |
| Database Migrations  | Alembic                 |
| Containerization     | Docker / Docker Compose |
| Package Management   | uv                      |

---

# Project Structure

```text
infra-pilot-ai/
│
├── app/
│   ├── agent/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── rag/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── utils/
│   ├── api.py
│   ├── auth.py
│   └── app.py
│
├── alembic/
│   └── migrations/
│
├── storage/
│
├── data/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

---

# Running the Application

InfraPilot AI is containerized using Docker Compose.

## Prerequisites

Install:

* Docker Desktop or Docker Engine.
* Docker Compose.

## Configuration

Create a `.env` file using `.env.example` as a template.

```bash
cp .env.example .env
```

Configure the required environment variables and credentials.

**Never commit `.env` or real credentials to version control.**

## Start the Application

Build and start the services:

```bash
docker compose up --build
```

The application can then be accessed through the Streamlit frontend:

```text
http://localhost:8501
```

The FastAPI backend is available at:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# Docker Services

The application is composed of three primary services:

```text
┌─────────────────────────────┐
│         Frontend            │
│         Streamlit           │
│          :8501              │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Backend            │
│           FastAPI           │
│           :8000             │
└──────────┬─────────┬────────┘
           │         │
           ▼         ▼
┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │   ChromaDB   │
│    :5432     │  │   Volume     │
└──────────────┘  └──────────────┘
```

Docker volumes are used to persist application data independently of the application containers.

---

# Data Persistence

The Docker deployment uses persistent volumes for:

* PostgreSQL data.
* ChromaDB data.
* Uploaded documents and screenshots.
* Hugging Face model cache.

This means rebuilding or recreating the application containers does not automatically remove stored conversations, indexed knowledge, uploaded documents, or downloaded embedding models.

To stop the application without removing persistent data:

```bash
docker compose down
```

To intentionally remove the persistent volumes:

```bash
docker compose down -v
```

> **Warning:** Removing the volumes permanently deletes the associated persistent application data.

---

# Knowledge Base Workflow

The administrator uploads a company document through the application.

The document passes through the following pipeline:

```text
Upload PDF
    │
    ▼
Extract Text
    │
    ├──────────────► Extract Images
    │
    ▼
Chunk Text
    │
    ▼
Generate Embeddings
    │
    ▼
Store in ChromaDB
    │
    ▼
Available for Retrieval
```

During a user query:

```text
User Question
     │
     ▼
LangGraph Agent
     │
     ▼
knowledge_lookup()
     │
     ▼
Retriever
     │
     ▼
ChromaDB
     │
     ▼
Relevant Document Chunks
     │
     ▼
LLM
     │
     ▼
Grounded Response
```

---

# Security Considerations

InfraPilot AI includes several security-related measures:

* Authenticated application access.
* JWT-based API authentication.
* Environment-based configuration of credentials.
* Separation of frontend, backend, and database services.
* Persistent data stored through Docker volumes.
* Sensitive credentials excluded from source control.

For enterprise deployment, environment variables and secrets should be managed according to the organization's security policies.

---

# Deployment

InfraPilot AI is designed to support deployment on the organization's local infrastructure.

The Dockerized application can be deployed on:

* Windows Server.
* Linux Server.

Docker Compose allows the frontend, backend, and PostgreSQL database to be deployed together while maintaining persistent application data.

For an enterprise deployment, the deployment environment should provide:

* Appropriate server resources.
* Secure environment configuration.
* Network access between application services.
* Access to the required LLM provider, unless a local LLM is configured.
* Appropriate access controls and firewall rules.
* Regular backup of persistent application data.

---

# Current Implementation

The current implementation includes:

* Streamlit frontend.
* FastAPI backend.
* LangGraph tool-calling agent.
* RAG-based company knowledge retrieval.
* ChromaDB vector storage.
* Local sentence-transformer embeddings.
* PostgreSQL persistence.
* Supabase authentication.
* Persistent multi-turn conversations.
* Knowledge-base document management.
* Visual RAG with document screenshots.
* Incident report generation.
* Docker and Docker Compose deployment.

---

# Future Enhancements

Potential future improvements include:

* Active Directory integration.
* Integration with infrastructure monitoring platforms.
* Real-time infrastructure alerts.
* Microsoft Teams or Slack integration.
* Local LLM deployment for fully on-premises inference.
* Infrastructure analytics dashboards.
* Advanced conversation search and pagination.
* Expanded administrative controls.

---

# Project Context

InfraPilot AI was developed as a **SIWES internship project** within the Infrastructure team at **Xpress Payment Solutions**.

The project focuses on applying AI engineering, backend development, Retrieval-Augmented Generation, agentic workflows, database management, and containerization to an enterprise infrastructure operations use case.

---

# License

This project was developed for educational and enterprise use within the scope of the SIWES project.

The project should not be redistributed or deployed outside its intended environment without appropriate authorization.
