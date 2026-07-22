# Retrieval-Augmented Generation (RAG) Workflow

## Overview

InfraPilot AI uses Retrieval-Augmented Generation (RAG) to provide accurate, reliable, and context-aware answers using the organization's infrastructure knowledge base.

Instead of relying solely on the Large Language Model's internal knowledge, the system retrieves relevant information from company documentation before generating a response. This ensures that responses are grounded in approved internal documentation, reducing hallucinations and improving trustworthiness.

---

# Question Answering Workflow

```
User Question
      │
      ▼
Streamlit Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Router Agent (LangGraph)
      │
      ▼
Knowledge Agent
      │
      ▼
Generate Question Embedding
      │
      ▼
Similarity Search in ChromaDB
      │
      ▼
Retrieve Top-K Relevant Chunks + Metadata
      │
      ▼
Construct Prompt
(Context + User Question)
      │
      ▼
Large Language Model
      │
      ▼
Generate Grounded Response
      │
      ▼
Return Response
      │
      ▼
Display:
• Generated Answer
• Source Document
• Document Type
• Section / Process Name
• Page Number(s)
• Related Screenshot(s) (if available)
```

---

# Document Ingestion Pipeline

Before users can query the knowledge base, uploaded documents must be processed and indexed.

```
Upload Document
      │
      ▼
Identify Document Type
(SOP, Runbook, FAQ, Policy, etc.)
      │
      ▼
Extract Text
      │
      ▼
Extract Images (Optional)
      │
      ▼
Clean & Normalize Text
      │
      ▼
Chunk Document
      │
      ▼
Generate Embeddings
      │
      ▼
Store Chunks + Metadata in ChromaDB
```

---

# Retrieval Process

When a user submits a question, the system performs the following steps:

1. Receive the user's question.
2. Convert the question into an embedding.
3. Perform semantic similarity search in ChromaDB.
4. Retrieve the most relevant document chunks and their metadata.
5. Build a prompt containing:
   - User question
   - Retrieved document context
6. Send the prompt to the Large Language Model.
7. Generate a grounded response.
8. Return the response together with its supporting references.

---

# Chunking Strategy

InfraPilot AI uses a document-aware chunking strategy rather than splitting every document into fixed-length chunks.

The chunking method depends on the type and structure of the uploaded document.

Examples:

- SOPs → Chunk by process or section.
- Runbooks → Chunk by procedure or operational task.
- FAQs → One question-answer pair per chunk.
- Policies → Chunk by policy section.

Each chunk may contain:

- Document Title
- Document Type
- Section or Process Title
- Main Content
- Page Number(s)
- Associated Screenshot(s) (if available)
- Additional Metadata

Preserving the logical structure of documents improves retrieval accuracy and produces more meaningful responses.

---

# Supported Knowledge Sources

InfraPilot AI is designed to support multiple types of infrastructure documentation, including:

- Standard Operating Procedures (SOPs)
- Runbooks
- Infrastructure FAQs
- Troubleshooting Guides
- Infrastructure Policies
- Incident Response Documentation
- Future Infrastructure Documents

All supported documents follow the same ingestion pipeline while allowing document-specific chunking strategies where appropriate.

---

# Why Retrieval-Augmented Generation (RAG)?

Using RAG enables InfraPilot AI to:

- Generate responses grounded in company documentation.
- Reduce hallucinations by providing relevant context to the LLM.
- Cite the original source document for transparency.
- Keep the knowledge base current without retraining the language model.
- Scale easily as new documents are added.

---

# Future Improvements

Future versions of InfraPilot AI may include:

- OCR for screenshots containing text.
- Multimodal retrieval for diagrams and images.
- Hybrid search (semantic + keyword).
- Document versioning.
- Confidence scoring.
- Support for local embedding models and local LLMs.