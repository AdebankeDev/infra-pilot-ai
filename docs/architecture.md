# InfraPilot AI — System Architecture

## Overview

InfraPilot AI is an AI-powered Infrastructure Copilot developed to assist enterprise infrastructure engineers with accessing internal technical knowledge, troubleshooting infrastructure-related issues, and managing operational conversations.

The system combines **Retrieval-Augmented Generation (RAG)** with a **LangGraph-based tool-calling agent**. Instead of relying on a general-purpose chatbot alone, the agent can determine when company-specific knowledge is required and invoke a knowledge retrieval tool to search the organization's internal documentation.

This architecture allows InfraPilot AI to provide conversational assistance while keeping company-specific responses grounded in internal documentation.

---

# High-Level Architecture

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
                  Infrastructure Copilot
                    (LangGraph Agent)
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
           Direct Response              Tool Calling
                  │                           │
                  │                           ▼
                  │                   knowledge_lookup()
                  │                           │
                  │                           ▼
                  │                      Retriever
                  │                           │
                  │                           ▼
                  │                       ChromaDB
                  │                           │
                  │                           ▼
                  │                  Company Documents
                  │
                  └─────────────┬─────────────┘
                                │
                                ▼
                              LLM
                                │
                                ▼
                       Grounded Response
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              Source Metadata          Screenshots
                    │                       │
                    └───────────┬───────────┘
                                ▼
                         Streamlit UI


                         PostgreSQL
                    ┌───────────┼───────────┐
                    │           │           │
                    ▼           ▼           ▼
                  Users    Chat History   Reports
```

---

# System Components

## 1. Streamlit Frontend

The Streamlit frontend provides the user interface for interacting with InfraPilot AI.

Authenticated users can:

* Ask infrastructure-related questions.
* Continue previous conversations.
* Start new conversations.
* View retrieved source documents and page numbers.
* View associated screenshots when available.
* Access the Knowledge Base management interface according to their permissions.
* Log in and log out securely.

The frontend communicates with the FastAPI backend through HTTP API requests.

---

## 2. FastAPI Backend

The FastAPI backend provides the application's API layer and coordinates the major application services.

Its responsibilities include:

* Authentication and authorization.
* Processing chat requests.
* Managing conversations and messages.
* Managing knowledge-base documents.
* Calling the Infrastructure Copilot agent.
* Returning generated responses and source information.
* Managing application data stored in PostgreSQL.
* Serving retrieved document screenshots where applicable.

The backend acts as the central integration layer between the frontend, AI components, databases, and knowledge base.

---

# 3. Infrastructure Copilot Agent

The core AI component is a **single LangGraph-based tool-calling agent**.

The agent is responsible for deciding how to respond to a user's request.

For general questions that do not require company-specific information, the agent can respond directly using the configured Large Language Model.

For company-specific or infrastructure-related questions that require internal knowledge, the agent can invoke the:

```text
knowledge_lookup()
```

tool.

This approach avoids unnecessary retrieval for general conversational requests while ensuring that company-specific answers can be grounded in internal documentation.

---

# 4. Knowledge Lookup Tool

The `knowledge_lookup()` tool provides the connection between the AI agent and the organization's internal knowledge base.

Its responsibilities include:

* Receiving a knowledge-related query.
* Searching the indexed company documentation.
* Retrieving the most relevant document chunks.
* Returning relevant context to the agent.
* Providing source metadata such as document names and page numbers.

The retrieved information is then used by the LLM to generate a grounded response.

---

# 5. Retrieval Layer

The retrieval layer is responsible for finding relevant information from the vector database.

The retrieval process involves:

1. Receiving the user's query.
2. Converting the query into an embedding.
3. Searching the vector database.
4. Selecting the most relevant document chunks.
5. Returning the retrieved content and metadata.

The retriever also provides metadata used to display document references and associated screenshots in the frontend.

---

# 6. Embedding Service

InfraPilot AI uses a local Sentence Transformers embedding model to convert text into numerical vector representations.

The configured model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model is used during both:

* Knowledge-base indexing.
* Query retrieval.

Because the model runs locally within the application environment, embedding generation does not require sending document content to an external embedding API.

---

# 7. ChromaDB

ChromaDB serves as the application's vector database.

It stores the vector representations of processed company documentation together with associated metadata.

Metadata can include:

* Document name.
* Page number.
* Source path.
* Associated screenshot information.

During retrieval, ChromaDB is searched for document chunks that are semantically similar to the user's query.

---

# 8. Company Knowledge Base

The knowledge base is built from internal company documentation, primarily PDF files.

Potential documents include:

* Standard Operating Procedures (SOPs).
* Infrastructure administration guides.
* Runbooks.
* Troubleshooting documentation.
* Technical reference documents.

Administrators can manage knowledge-base documents through the application.

The document processing pipeline consists of:

```text
PDF Document
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
```

Screenshots and other extracted images are stored separately and associated with the relevant document metadata.

---

# 9. Large Language Model

The application currently uses an LLM accessed through OpenRouter.

The LLM is responsible for:

* Generating conversational responses.
* Interpreting retrieved knowledge.
* Producing grounded answers.
* Handling general questions that do not require company documentation.

When company knowledge is retrieved, the relevant context is supplied to the LLM so that the response can be grounded in the organization's documentation.

---

# 10. PostgreSQL

PostgreSQL is used as the application's relational database.

It stores structured application data including:

* User information.
* Conversations.
* Chat messages.
* Incident report information.
* Document metadata where applicable.

Chat history allows users to resume previous conversations and provides the data required for generating incident reports.

PostgreSQL is persisted through a Docker volume so that rebuilding or restarting application containers does not remove stored application data.

---

# 11. Authentication and Authorization

InfraPilot AI uses authentication mechanisms based on Supabase Auth and JWT-based authentication.

Authenticated users receive access to protected application functionality.

Administrative permissions are used to restrict knowledge-base management operations such as:

* Uploading documents.
* Updating or re-indexing documents.
* Removing documents.

This prevents ordinary users from modifying the organization's knowledge base.

---

# Visual RAG

InfraPilot AI extends conventional text-based RAG by associating retrieved document chunks with screenshots extracted from the original PDF documents.

When relevant images are available, the backend returns:

* Source document.
* Page number.
* Associated screenshots.

The Streamlit frontend can then display these sources alongside the generated response.

The process is:

```text
Company PDF
     │
     ├──────────────► Extract Text
     │                    │
     │                    ▼
     │              Chunk + Embed
     │                    │
     │                    ▼
     │                ChromaDB
     │
     └──────────────► Extract Images
                          │
                          ▼
                    Storage / Images
                          │
                          ▼
                    Source Metadata
```

This provides visual context in addition to the generated textual answer.

---

# Chat and Conversation Management

The chat system supports multi-turn conversations.

When a user sends a message:

1. The frontend sends the request to the FastAPI backend.
2. The backend identifies the current conversation.
3. Previous messages are retrieved from PostgreSQL.
4. Conversation history is converted into LangChain message objects.
5. The Infrastructure Copilot processes the request.
6. The response is returned to the frontend.
7. The user message and AI response are persisted in PostgreSQL.

Users can later select previous conversations from the sidebar and continue them.

---

# Incident Reporting

InfraPilot AI can generate structured incident reports using information from stored conversations.

The conversation history provides the context required to produce a standardized operational report.

This allows engineers to move from troubleshooting conversations toward documented incident records without manually reconstructing the entire interaction.

---

# Request Flow

A typical company-specific request follows this process:

```text
1. User submits question
          │
          ▼
2. Streamlit sends API request
          │
          ▼
3. FastAPI receives request
          │
          ▼
4. Conversation history retrieved
          │
          ▼
5. LangGraph agent processes request
          │
          ▼
6. Agent determines knowledge is required
          │
          ▼
7. knowledge_lookup() is invoked
          │
          ▼
8. Retriever searches ChromaDB
          │
          ▼
9. Relevant document chunks returned
          │
          ▼
10. Context provided to LLM
          │
          ▼
11. Grounded response generated
          │
          ▼
12. Sources and screenshots attached
          │
          ▼
13. Response returned to Streamlit
          │
          ▼
14. Conversation persisted in PostgreSQL
```

For a general question that does not require company knowledge, the retrieval step can be skipped and the agent can generate a direct response.

---

# Document Indexing Flow

When an administrator uploads a document, the knowledge-base pipeline processes it before it becomes available for retrieval.

```text
Administrator
      │
      ▼
Upload PDF
      │
      ▼
Document Processing
      │
      ├──────────────► Extract Text
      │
      └──────────────► Extract Images
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
       Indexed Knowledge
```

Document metadata and processing status are managed by the backend.

---

# Deployment Architecture

InfraPilot AI is containerized using Docker and Docker Compose.

The application consists of three primary services:

```text
Docker Compose
│
├── Frontend
│     └── Streamlit
│
├── Backend
│     ├── FastAPI
│     ├── LangGraph
│     ├── RAG Pipeline
│     └── Embedding Model
│
└── PostgreSQL
```

ChromaDB data, document storage, Hugging Face model cache, and PostgreSQL data are persisted using Docker volumes.

The application can therefore be deployed on an organization's local infrastructure without requiring the frontend, backend, and database to be manually started as separate development processes.

The current deployment architecture supports environments such as:

* Windows Server.
* Linux Server.

The application exposes the frontend and backend through configurable ports, while internal Docker services communicate using Docker's service names.

---

# Technology Stack

| Layer                | Technology              |
| -------------------- | ----------------------- |
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
| Programming Language | Python                  |

---

# Design Principles

The system was designed around several engineering principles:

### Grounded AI

Company-specific responses should be based on retrieved organizational documentation rather than unsupported assumptions.

### Modular Architecture

The frontend, backend, AI agent, retrieval layer, database, and document-processing components are separated into distinct responsibilities.

### Explainability

Retrieved source documents, page numbers, and associated screenshots can be presented alongside responses.

### Data Persistence

Application data and knowledge-base data are persisted independently of individual Docker containers.

### Security

Authentication and authorization are applied to protect application functionality and administrative knowledge-base operations.

### Enterprise Deployment

The application is containerized so it can be deployed within the organization's infrastructure and maintained independently of the development environment.

---

# Future Enhancements

Potential future improvements include:

* Integration with Active Directory.
* Integration with infrastructure monitoring platforms.
* Real-time infrastructure alerts.
* Microsoft Teams or Slack integration.
* Infrastructure analytics and reporting dashboards.
* Advanced conversation search and pagination.
* Expanded administrative controls.

```
```
