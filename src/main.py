from enum import Enum
from typing import Dict

from report_pipeline.pdf_processor import PDFProcessor, VectorStoreManager
from report_pipeline.report_generator import CEOReportGenerator, CFOReportGenerator, COOReportGenerator, ReportGenerator


class ReportType(str, Enum):
    CFO = "cfo"
    CEO = "ceo"
    COO = "coo"
    
    
if __name__ == "__main__":
    pdf_processor = PDFProcessor()
    
    vector_store = VectorStoreManager()
    vector_store.reset_store()
    
    content_blocks = pdf_processor.extract_text("./data/2023-annual-report-short.pdf")
    
    pdf_processor.document_stats()

    vector_store.store_content(content_blocks)
    
    selected_type = ReportType.CFO
    
    generators : Dict[ReportType, ReportGenerator]= {
        ReportType.CFO: CFOReportGenerator(),
        ReportType.CEO: CEOReportGenerator(),
        ReportType.COO: COOReportGenerator()
    }
    
    queries : Dict[ReportType, str] = {
        ReportType.CFO: "financial metrics, costs, and revenue analysis",
        ReportType.CEO: "strategic insights, market position, and business performance",
        ReportType.COO: "operational efficiency, processes, and resource utilization"
    }
    
    generator = generators[selected_type]
    query = queries[selected_type]

    docs = vector_store.retrieve_content(query)
    for d in docs:
        print(d)
        
    generator.create_report(docs)
    
    print(generator.report_content)
    