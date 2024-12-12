from typing import Dict
from report_pipeline.report_generator import CEOReportGenerator, CFOReportGenerator, COOReportGenerator, ReportGenerator, ReportType


generators : Dict[ReportType, ReportGenerator]= {
    ReportType.CFO: CFOReportGenerator(),
    ReportType.CEO: CEOReportGenerator(),
    ReportType.COO: COOReportGenerator()
}

queries : Dict[ReportType, list[str]] = {
    ReportType.CFO: ["Key financial metrics and trends", "Cost analysis and revenue insights", "Financial risks and opportunities"],
    ReportType.CEO: ["strategic insights, market position, and business performance"],
    ReportType.COO: ["operational efficiency, processes, and resource utilization"]
}