from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enum import Enum
import os
from typing import Optional
from pdf_processor import PDFProcessor
from report_generator import CFOReportGenerator, CEOReportGenerator, COOReportGenerator, ReportType

class ReportRequest(BaseModel):
    pdf_path: str
    report_type: ReportType
    output_dir: Optional[str] = "reports"

class ReportResponse(BaseModel):
    report_path: str
    status: str

app = FastAPI(
    title="Report Generation API",
    description="API for generating stakeholder-specific reports from PDF documents"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/generate_report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    try:
        # Initialize PDF processor
        processor = PDFProcessor()
        
        # Extract and store content
        content = processor.extract_text(request.pdf_path)
        
        # Initialize appropriate generator based on report type
        openai_api_key = os.getenv("OPENAI_API_KEY")
        generators = {
            ReportType.CFO: CFOReportGenerator(),
            ReportType.CEO: CEOReportGenerator(),
            ReportType.COO: COOReportGenerator()
        }
        
        generator = generators[request.report_type]
        
        # Define queries for each stakeholder type
        queries = {
            ReportType.CFO: "financial metrics, costs, and revenue analysis",
            ReportType.CEO: "strategic insights, market position, and business performance",
            ReportType.COO: "operational efficiency, processes, and resource utilization"
        }
        
        # Ensure output directory exists
        os.makedirs(request.output_dir, exist_ok=True)
        
        # Generate report
        output_path = f"{request.output_dir}/{request.report_type.value}_report.pptx"
        generator.create_report(content, output_path)
        
        return ReportResponse(
            report_path=output_path,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 