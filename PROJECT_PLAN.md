# InfraPilot AI

## AI-Powered Infrastructure Copilot for Enterprise IT Operations

---

# Project Overview

**InfraPilot AI** is an AI-powered Infrastructure Copilot designed to assist the Infrastructure team at Xpress Payment Solutions by providing intelligent access to internal technical documentation, assisting with infrastructure troubleshooting, and generating standardized incident reports.

The application uses Retrieval-Augmented Generation (RAG) and an agentic architecture to retrieve information from approved company documentation and provide accurate, context-aware responses.

The goal is to reduce the time engineers spend searching through documentation while improving knowledge sharing and operational efficiency.

---

# Problem Statement

Infrastructure engineers frequently rely on Standard Operating Procedures (SOPs), runbooks, troubleshooting guides, and other technical documentation when carrying out operational tasks or responding to incidents.

Searching through multiple documents can be time-consuming, especially for repetitive questions or common troubleshooting scenarios.

There is an opportunity to improve knowledge accessibility by providing an AI-powered assistant that retrieves relevant information from approved documentation and presents it in a conversational and structured manner.

---

# Project Objectives

The objectives of this project are to:

* Develop an AI-powered Infrastructure Copilot.
* Build a Retrieval-Augmented Generation (RAG) system using company documentation.
* Design a multi-agent architecture using LangGraph.
* Develop a REST API using FastAPI.
* Build an interactive Streamlit web application.
* Store application data using PostgreSQL.
* Store document embeddings using ChromaDB.
* Generate standardized incident reports.
* Deploy the application on the company's local server.

---

# Project Scope

## In Scope

### Authentication

* User login
* JWT authentication
* Role-based access (future enhancement)

### Knowledge Agent

* Answer questions using approved documentation
* Cite document sources
* Retrieve relevant document sections

### Diagnostics Agent

* Accept infrastructure symptoms or alerts
* Suggest possible causes
* Recommend troubleshooting steps
* Reference relevant documentation

### Incident Report Agent

* Generate standardized incident reports
* Produce structured summaries
* Store reports in the database

### Data Management

* Upload approved documents
* Process documents
* Store embeddings
* Maintain document metadata

### User Interface

* Chat interface
* Conversation history
* Incident report generation
* Responsive dashboard

---

# Out of Scope

The following features are intentionally excluded from Version 1:

* Live infrastructure monitoring
* Automatic ticket creation
* Active Directory integration
* Email notifications
* Microsoft Teams or Slack integration
* Predictive infrastructure analytics
* Automated remediation
* Direct integration with Nutanix Prism

These may be considered in future versions.

---

# Target Users

* Infrastructure Engineers
* System Administrators
* IT Support Engineers
* SIWES Interns (future knowledge sharing)

---

# Functional Requirements

The system shall:

* Authenticate users.
* Allow users to ask infrastructure-related questions.
* Search company documentation using RAG.
* Generate AI responses with document references.
* Generate incident reports.
* Save chat history.
* Save incident reports.
* Store uploaded documents.
* Retrieve relevant document chunks.

---

# Non-Functional Requirements

* Fast response time
* Secure authentication
* Easy-to-use interface
* Modular architecture
* Scalable design
* Easy deployment
* Maintainable codebase

---

# System Architecture

The application consists of:

* Streamlit Frontend
* FastAPI Backend
* LangGraph Router Agent
* Knowledge Agent
* Diagnostics Agent
* Incident Report Agent
* PostgreSQL Database
* ChromaDB Vector Database
* Large Language Model (via OpenRouter during development)

---

# Technology Stack

## Backend

* Python
* FastAPI

## Frontend

* Streamlit
* HTML
* CSS

## AI

* LangChain
* LangGraph
* OpenRouter
* Retrieval-Augmented Generation (RAG)

## Database

* PostgreSQL
* ChromaDB

## Deployment

* Docker
* Local Server (Windows Server or Linux Server)

## Version Control

* Git
* GitHub

---

# Documents Required

The project requires the following approved documentation:

* Infrastructure SOP
* Runbooks
* Troubleshooting guides
* Infrastructure FAQs
* Incident report template
* Sample anonymized incident reports (if available)

# Knowledge Base Sources

## Infrastructure SOP

Source:
Infrastructure Team SOP provided by Xpress Payment Solutions.

Purpose:
Provides internal procedures and operational knowledge for the AI Knowledge Assistant.

Usage:
The document will be processed, embedded, and stored in ChromaDB for retrieval.

---

# Four-Week Development Plan

## Week 1

### Planning & Knowledge Base

* Project planning
* Repository setup
* Development environment setup
* Obtain project approval
* Collect documentation
* Organize documents
* Learn ChromaDB
* Learn RAG
* Build document ingestion pipeline

---

## Week 2

### Knowledge Agent

* Build FastAPI backend
* Configure PostgreSQL
* Configure ChromaDB
* Build Knowledge Agent
* Build retrieval pipeline
* Connect LLM
* Build initial Streamlit interface

---

## Week 3

### Agentic Workflow

* Build Router Agent
* Build Diagnostics Agent
* Build Incident Report Agent
* Improve prompts
* Test with sample documents

---

## Week 4

### Production & Deployment

* Authentication
* Chat history
* Testing
* Documentation
* Deployment preparation
* Final presentation
* SIWES defense preparation

---

# Deliverables

* GitHub repository
* FastAPI backend
* Streamlit frontend
* PostgreSQL database
* ChromaDB vector database
* Router Agent
* Knowledge Agent
* Diagnostics Agent
* Incident Report Agent
* User authentication
* Technical documentation
* Architecture diagram
* Deployment guide
* SIWES presentation

---

# Future Improvements

Possible future enhancements include:

* Integration with Nutanix Prism
* Microsoft Teams integration
* Slack integration
* Predictive infrastructure analytics
* Local LLM deployment using Ollama
* Voice interaction
* Infrastructure dashboard
* Ticketing system integration

---

# Success Criteria

The project will be considered successful if it:

* Successfully answers infrastructure questions using approved documentation.
* Retrieves relevant documents accurately.
* Generates standardized incident reports.
* Demonstrates a modular multi-agent architecture.
* Can be deployed on the company's local server.
* Is suitable for operational use by the Infrastructure team after further refinement.

---

# Project Status

**Status:** Planning Phase

**Current Version:** v0.1

**Start Date:** 20 July 2026

**Target Completion:** August 2026
