# SCG RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application that analyzes sample documents against security classification guidance and recommends portion markings with supporting source citations.

## Project Goal

The goal of this project is to demonstrate how a RAG-based AI system can assist a human reviewer with classification-guidance analysis.

The system will:

1. Ingest a fictional or publicly releasable Security Classification Guide (SCG).
2. Break the guide into searchable sections.
3. Generate embeddings and store them in a vector database.
4. Accept sample email or document text from a user.
5. Retrieve the most relevant classification guidance.
6. Use an LLM to analyze individual portions of the document.
7. Recommend portion markings.
8. Explain the recommendation.
9. Cite the relevant source guidance.
10. Require human review before accepting the recommendation.

## Important Security Notice

This project is for educational and portfolio purposes only.

Do not upload, process, or store:

* Classified information
* Controlled Unclassified Information (CUI)
* Proprietary company information
* Export-controlled information
* Real security classification guides that are not publicly releasable
* Real work emails or documents

All demonstration data used in this repository will be fictional or publicly releasable.

## Example

### Sample Guidance

> Information revealing the operational range of Project Falcon is classified CONFIDENTIAL.

### Sample Email

```text
Team,

The customer meeting has been moved to Thursday.

Testing confirmed Project Falcon can operate at a range of 425 miles.

Please update the schedule accordingly.
```

### Example AI Recommendation

```text
(U) Team,

(U) The customer meeting has been moved to Thursday.

(C) Testing confirmed Project Falcon can operate at a range of 425 miles.

(U) Please update the schedule accordingly.
```

Overall recommended classification:

```text
CONFIDENTIAL
```

Supporting guidance:

```text
SCG Section 3.2:
Operational range information for Project Falcon is classified CONFIDENTIAL.
```

Human review is required before accepting the recommendation.

## Planned Architecture

```text
Security Classification Guide
            |
            v
      Document Parser
            |
            v
         Chunking
            |
            v
        Embeddings
            |
            v
      Vector Database
            |
            |
Sample Document
            |
            v
        Retriever
            |
            v
 Relevant SCG Sections
            |
            v
           LLM
            |
            v
 Portion Marking Recommendation
            |
            v
 Explanation + SCG Citations
            |
            v
       Human Review
```

## Planned Technology Stack

* Python
* LLM API
* Embeddings
* Vector database
* RAG
* FastAPI
* Pydantic
* pytest
* Docker
* GitHub Actions

The specific libraries and providers may change as the project develops.

## Development Milestones

### Milestone 1 — Basic LLM Classification

Send sample guidance and a sample document directly to an LLM and receive structured classification recommendations.

### Milestone 2 — Structured Output

Return predictable JSON containing:

* document classification
* portion markings
* explanations
* confidence
* supporting guidance

### Milestone 3 — SCG Document Ingestion

Load a fictional SCG and divide it into searchable chunks.

### Milestone 4 — Embeddings and Vector Search

Create embeddings for SCG sections and store them in a vector database.

### Milestone 5 — RAG Pipeline

Retrieve relevant guidance automatically before requesting a classification recommendation from the LLM.

### Milestone 6 — Source Citations

Associate recommendations with the exact SCG sections retrieved by the system.

### Milestone 7 — Evaluation

Create a test dataset and measure:

* Retrieval accuracy
* Classification accuracy
* Unsupported recommendations
* Citation accuracy

### Milestone 8 — API

Expose the application through a FastAPI REST API.

### Milestone 9 — User Interface

Create a simple interface for:

* Uploading guidance
* Entering sample document text
* Reviewing recommendations
* Viewing citations

### Milestone 10 — Production Engineering

Add:

* Automated tests
* Logging
* Error handling
* Docker
* GitHub Actions
* Deployment

## AI Safety and Design Principles

This application is designed as a decision-support system rather than an autonomous classification authority.

The AI should:

* Cite supporting guidance.
* Clearly indicate uncertainty.
* Avoid making unsupported classification determinations.
* Distinguish retrieved guidance from generated analysis.
* Allow a human reviewer to accept or reject recommendations.
* Prefer "insufficient guidance" over inventing a classification rule.

## Project Status

🚧 Early development
