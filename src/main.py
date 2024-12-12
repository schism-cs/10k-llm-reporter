from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from report_pipeline.pdf_processor import PDFProcessor, VectorStoreManager
from report_pipeline.report_generator import Presentation, ReportType

from report_pipeline.utils.search_results import SearchResults
from report_pipeline.utils.generation import generators, queries

app = FastAPI(
    title="Report Generation API",
    description="API for generating stakeholder-specific reports from PDF documents"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ReportRequest(BaseModel):
    report_type: ReportType

@app.post("/generate_report", response_model=Presentation)
async def generate_report(request: ReportRequest):
    vector_store = VectorStoreManager()
    
    selected_type = request.report_type
    
    generator = generators[selected_type]
    query = queries[selected_type]

    search_results = SearchResults()
    for query in queries:
        docs = vector_store.retrieve_content(query)
        for doc in docs:
            search_results.add_result(doc)
        
    generator.create_report(search_results.get_results())
    
    print(generator.report_content)
    
    return generator.report_content
        
@app.get("/reindex_document")
async def reindex_doc():
    vector_store = VectorStoreManager()
    
    pdf_processor = PDFProcessor()
    
    vector_store.reset_store()
    
    content_blocks = pdf_processor.extract_text("./data/2023-annual-report.pdf")
    
    pdf_processor.document_stats()
    
    vector_store.store_content(content_blocks)
    
    return "ok"

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
