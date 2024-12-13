# PDF Report Generator

An AI-powered service that generates stakeholder-specific reports from PDF documents. The service extracts content using LLMSherpa, processes it through LangChain, and generates tailored presentations for different stakeholders (CFO, CEO, COO).

## Features

- PDF content extraction with structural understanding
- Content processing for different block types (paragraphs, lists, tables)
- Vector-based content storage using ChromaDB
- Customized report generation for different stakeholders
- FastAPI-based REST API

## Prerequisites

- Python 3.11+
- Docker (optional)
- OpenAI API key
- LLMSherpa API endpoint

## Environment Variables (dev only)

Create a `.env` file with the following variables:

OPENAI_API_KEY=your_openai_api_key
LLMSHERPA_ENDPOINT=your_llmsherpa_endpoint (this is required only if the vector store must be reindexed)

## Installation

1. Clone the repository
2. Install dependencies from requirements.txt
3. Set up environment variables in .env file

## Running the Service

### Local Development
Run the FastAPI application using uvicorn on port 8000

### Using Docker
1. Build the Docker image 
    > docker build -t report-generator .

2. Run the container with environment variables and port 8000 exposed
    > docker run -p 8000:8000 \
    > -e OPENAI_API_KEY=your_openai_key \
    > -e LLMSHERPA_ENDPOINT=your_llmsherpa_endpoint \
    > report-generator

## API Endpoints

### POST /generate_report
Generates a stakeholder-specific report from a PDF document.

Request body:
```json
{
    "report_type": "cfo|ceo|coo",
}
```

Response:
```json
[
    {
        title: str
        table_caption: strthe data", default="")
        table: str 
        content: list[str]
        recommendations: List[str]
        slide_type
    }, ...
]
```

### GET /health
Health check endpoint that returns service status.


## Notes

- The service processes PDFs using LLMSherpa for structural understanding
- Content is stored in ChromaDB for efficient retrieval
- Reports are generated using LangChain and OpenAI
- Different processing pipelines for paragraphs, lists, and tables