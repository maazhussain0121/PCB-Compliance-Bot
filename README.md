# PCB Compliance Bot

A FastAPI-powered compliance assistant that leverages Retrieval-Augmented Generation (RAG) to answer questions about PCB standards and regulations using Azure OpenAI.

## Overview

The PCB Compliance Bot is an intelligent system designed to provide quick and accurate answers to compliance-related questions by searching through a vector database of PCB documentation and standards. It combines:

- **Vector Database**: Chroma for efficient document retrieval
- **LLM**: Azure OpenAI (GPT-4.1) for intelligent response generation
- **Document Processing**: PDF extraction and chunking for compliance documents
- **Quality Evaluation**: RAGAS metrics for answer relevancy and faithfulness assessment

## Features

- 📄 **PDF Document Processing**: Automatically extracts and processes compliance documentation
- 🔍 **Semantic Search**: Uses embeddings to find relevant compliance information
- 🤖 **AI-Powered Responses**: Generates accurate answers using Azure OpenAI
- 📊 **Quality Metrics**: Evaluates answer relevancy and faithfulness
- ⚡ **Fast API**: RESTful API for easy integration
- 💾 **Persistent Vector DB**: Chroma vector store for efficient retrieval

## Project Structure

```
pcb/
├── app.py                 # FastAPI application setup
├── main.py               # Core RAG logic and vector DB management
├── model.py              # Pydantic models for requests
├── router/
│   └── response.py       # API endpoints
├── dataset/              # PCB compliance documents (PDFs)
├── chroma_db/            # Vector database storage
├── pyproject.toml        # Project metadata and dependencies
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Python >= 3.13
- Azure OpenAI API credentials
- Environment variables configured

### 3. Query the Compliance Bot

**Endpoint**: `POST /ask`

**Request:**
```json
{
  "question": "What are the RoHS compliance requirements?"
}
```

**Response:**
```json
{
  "answer": "RoHS compliance requires...",
  "sources": ["Source documentation references"],
  "relevancy_score": 0.95,
  "faithfulness_score": 0.92
}
```


## Quality Metrics

The system evaluates responses using:

- **AnswerRelevancy**: Measures how relevant the answer is to the question
- **Faithfulness**: Measures if the answer is grounded in the retrieved context


## Future Enhancements

- [ ] Support for multiple document types (HTML, DOCX)
- [ ] Web interface for easy querying
- [ ] Document upload functionality
- [ ] Answer caching and analytics
- [ ] Multi-language support
- [ ] Custom fine-tuning for PCB-specific terminology

## Support

For issues or questions, please contact [your contact information].
