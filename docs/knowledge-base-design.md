# Knowledge Base Design

## Overview

The InfraPilot AI Knowledge Base is a centralized repository of organizational infrastructure documentation used to power the application's Retrieval-Augmented Generation (RAG) capabilities.

Rather than relying solely on the Large Language Model's pre-trained knowledge, InfraPilot AI retrieves relevant information from the organization's internal documentation before generating a response. This ensures that answers are accurate, grounded, and based on approved company knowledge.

The knowledge base is designed to be scalable, allowing new documents to be added over time without requiring changes to the system architecture.

---

# Objectives

The Knowledge Base is designed to:

- Centralize infrastructure documentation.
- Provide accurate and grounded responses.
- Preserve organizational knowledge.
- Reduce time spent searching through documentation.
- Support multiple document types.
- Scale as new documents are added.
- Serve as the primary source of truth for the AI assistant.

---

# Supported Document Types

The system is designed to support various types of infrastructure documentation rather than relying on a single Standard Operating Procedure (SOP).

Examples include:

- Standard Operating Procedures (SOPs)
- Runbooks
- Troubleshooting Guides
- Infrastructure FAQs
- Infrastructure Policies
- Incident Response Documentation
- Onboarding Guides
- Technical Manuals
- Knowledge Articles

This design ensures that the application remains flexible and can grow with the organization's documentation.

---

# Knowledge Base Architecture

```text
                Knowledge Base

                        │

        ┌───────────────┼───────────────┐
        │               │               │

        ▼               ▼               ▼

     Documents     ChromaDB      PostgreSQL

        │               │               │

        │               │               │

Original Files   Embeddings &     Document Metadata
                 Document Chunks
```

The knowledge base consists of three primary components:

- Original documents
- Vector database (ChromaDB)
- Relational database (PostgreSQL)

Each component has a specific responsibility.

---

# Original Documents

Original documents are stored separately from the vector database.

Examples include:

- PDF documents
- Word documents (future support)
- Markdown files (future support)

Keeping the original files allows the system to:

- Reprocess documents when chunking strategies change.
- Regenerate embeddings.
- Display original document pages.
- Extract screenshots.
- Preserve the original source of truth.

---

# ChromaDB

ChromaDB serves as the vector database for the application.

It stores:

- Document chunks
- Vector embeddings
- Chunk metadata

ChromaDB enables semantic similarity search, allowing the AI assistant to retrieve the most relevant information based on meaning rather than exact keyword matches.

The vector database does **not** replace the original documents. Instead, it provides an efficient mechanism for retrieving relevant knowledge.

---

# PostgreSQL

PostgreSQL stores structured application data related to the knowledge base.

Examples include:

- Document information
- Upload history
- Document status
- Document type
- File location
- Document hash

PostgreSQL also stores application data such as:

- Users
- Chat history
- Incident reports

Embeddings are **not** stored in PostgreSQL.

---

# Document Organization

Each document belongs to a document type.

Examples include:

| Document | Type |
|----------|------|
| Infrastructure SOP | SOP |
| Password Reset Runbook | Runbook |
| Infrastructure Policy | Policy |
| VPN Troubleshooting Guide | Troubleshooting Guide |
| Infrastructure FAQ | FAQ |

Document type determines how the document will be processed during ingestion.

---

# Document Metadata

Each document stored in the knowledge base contains descriptive metadata.

Typical metadata includes:

| Field | Description |
|---------|-------------|
| document_id | Unique identifier |
| document_name | Original file name |
| document_type | SOP, Runbook, Policy, etc. |
| file_path | Storage location |
| file_hash | Used to detect duplicate documents |
| uploaded_by | Administrator who uploaded the document |
| upload_date | Date uploaded |
| status | Active or Archived |

At the chunk level, additional metadata is stored in ChromaDB:

| Field | Description |
|---------|-------------|
| chunk_id | Unique chunk identifier |
| document_id | Parent document |
| section | Document section title |
| page_start | Starting page |
| page_end | Ending page |
| image_references | Associated screenshots |
| chunk_text | Text used for embedding |

This metadata improves retrieval accuracy and source attribution.

---

# Knowledge Base Management

The knowledge base is managed exclusively by users with the **Admin** role.

Administrators can:

- Upload new documents.
- Update existing documents.
- Delete outdated documents.
- Trigger document indexing.
- Maintain the quality of organizational knowledge.

Infrastructure Engineers cannot modify the knowledge base.

---

# Integration with RAG

The knowledge base is the foundation of the Retrieval-Augmented Generation (RAG) pipeline.

When an engineer submits a question:

1. The question is converted into an embedding.
2. ChromaDB performs a semantic similarity search.
3. The most relevant document chunks are retrieved.
4. The retrieved context is supplied to the Large Language Model.
5. The model generates a grounded response.
6. The application returns the answer along with the source document and, where available, supporting screenshots.

This process ensures responses are based on company-approved documentation rather than the model's internal knowledge alone.

---

# Scalability

The knowledge base has been designed to support future growth.

Adding new documentation does not require changes to the application architecture.

Instead, administrators simply upload additional documents, which are automatically processed and indexed.

This approach enables the system to evolve alongside the organization's documentation.

---

# Design Principles

The Knowledge Base follows several key design principles:

- **Single Source of Truth** – Organizational documentation serves as the authoritative source for AI responses.
- **Scalability** – New document types can be added without redesigning the system.
- **Maintainability** – Documents can be updated or replaced independently.
- **Separation of Responsibilities** – Original files, vector embeddings, and relational data are stored separately in systems optimized for their respective purposes.
- **Grounded AI Responses** – Every response is generated using retrieved organizational knowledge instead of relying solely on the LLM's pre-trained knowledge.

---

# Future Enhancements

The knowledge base architecture supports future capabilities, including:

- Automatic document versioning
- Incremental document indexing
- Optical Character Recognition (OCR) for scanned documents
- Image caption generation
- Hybrid search (semantic + keyword)
- Support for additional document formats
- Knowledge quality analytics
- Scheduled re-indexing of updated documents

These enhancements are outside the scope of the current SIWES project but have been considered during the system design to ensure future extensibility.