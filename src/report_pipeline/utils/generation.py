from typing import Dict
from report_pipeline.report_generator import CEOReportGenerator, CFOReportGenerator, COOReportGenerator, ReportGenerator, ReportType


generators : Dict[ReportType, ReportGenerator]= {
    ReportType.CFO: CFOReportGenerator(),
    ReportType.CEO: CEOReportGenerator(),
    ReportType.COO: COOReportGenerator()
}

queries : Dict[ReportType, list[str]] = {
    ReportType.CFO: [
        "Key financial metrics and trends",
        "Revenue growth analysis and cost management strategies",
        "Profit margins and expense breakdowns",
        "Cash flow performance and liquidity insights",
        "Debt ratios and financial stability",
        "Investment returns and ROI analysis",
        "Quarter-over-quarter financial performance comparison",
        "Forecasting financial risks and opportunities"
    ],
    ReportType.CEO: [
        "strategic insights, market position, and business performance"
    ],
    ReportType.COO: [
        "operational efficiency, processes, and resource utilization"
    ]
}