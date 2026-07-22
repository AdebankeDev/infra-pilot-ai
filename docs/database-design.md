# Database Design

## Overview

InfraPilot AI uses two databases:

1. PostgreSQL - Stores application data.
2. ChromaDB - Stores vector embeddings for document retrieval.

---

# PostgreSQL Database Design

## Users

Purpose:
Stores user authentication and account information.

| Field | Type | Description |
|------|------|-------------|
| id | UUID | Primary Key |
| username | VARCHAR | Username |
| email | VARCHAR | Email Address |
| password_hash | TEXT | Hashed Password |
| role | VARCHAR | User Role |
| created_at | TIMESTAMP | Account Creation Date |

---

## Chat History

Purpose:
Stores conversations between users and the AI assistant.

| Field | Type | Description |
|------|------|-------------|
| id | UUID | Primary Key |
| user_id | UUID | References Users |
| question | TEXT | User Question |
| answer | TEXT | AI Response |
| agent | VARCHAR | Knowledge / Diagnostics / Incident |
| created_at | TIMESTAMP | Timestamp |

---

## Incident Reports

Purpose:
Stores AI-generated incident reports.

| Field | Type | Description |
|------|------|-------------|
| id | UUID | Primary Key |
| user_id | UUID | References Users |
| title | VARCHAR | Incident Title |
| description | TEXT | User Description |
| severity | VARCHAR | Low / Medium / High / Critical |
| generated_report | TEXT | AI Generated Report |
| created_at | TIMESTAMP | Timestamp |

---

## Uploaded Documents

Purpose:
Stores metadata for uploaded documents.

| Field | Type | Description |
|------|------|-------------|
| id | UUID | Primary Key |
| filename | VARCHAR | Document Name |
| document_type | VARCHAR | SOP / Runbook / FAQ |
| uploaded_by | UUID | User ID |
| upload_date | TIMESTAMP | Upload Date |
| status | VARCHAR | Processing Status |

---

# ChromaDB Design

ChromaDB stores document embeddings instead of relational data.

Each stored chunk contains:

- Chunk Text
- Embedding Vector
- Metadata

{
    "document_name": "<Document Name>",
    "document_type": "SOP",
    "section": "<Section Title>",
    "page_start": 26,
    "page_end": 27,
    "images": [
        "page26_img1.png"
    ]
}

---

# Why Two Databases?

PostgreSQL stores structured application data.

Examples:

- Users
- Chat History
- Incident Reports
- Uploaded Documents

ChromaDB stores semantic representations of document chunks for similarity search.

Examples:

- SOP text chunks
- Runbooks
- Troubleshooting guides
- FAQs

Using two databases allows the application to efficiently manage operational data while performing intelligent document retrieval.