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
        "Strategic insights, market position, and business performance",
        "Revenue growth trends and competitive positioning",
        "Business expansion opportunities and challenges",
        "Market share analysis and industry trends",
        "High-level performance overview and key milestones",
        "Long-term vision and strategic planning",
        "Leadership priorities and organizational direction",
        "Key risks impacting business strategy",
        "Emerging market opportunities and innovation potential"
    ],
    ReportType.COO: [
        "Operational efficiency, processes, and resource utilization",
        "Bottleneck identification and resolution strategies",
        "Key operational performance indicators (KPIs)",
        "Supply chain performance and logistics optimization",
        "Workforce productivity and resource allocation",
        "Process improvements and cost-saving initiatives",
        "Infrastructure utilization and capacity planning",
        "Operational risks and mitigation plans",
        "Sustainability and environmental efficiency in operations"
    ]
}