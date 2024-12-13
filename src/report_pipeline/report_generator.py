from enum import Enum
import os
from typing import Dict, List, Literal
from dotenv import load_dotenv
from abc import ABC, abstractmethod

from langchain_openai import OpenAI
from langchain_core.documents import Document
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field

load_dotenv()

class ReportType(str, Enum):
    CFO = "cfo"
    CEO = "ceo"
    COO = "coo"

class SlideContent(BaseModel):
    title: str = Field(description="Section title", default="")
    table_caption: str = Field(description="Optional table caption, describing the data", default="")
    table: str = Field(description="Optional table diplaying header and auxiliary data to the content, formatted in Markdown", default="")
    content: List[str] = Field(description="Bullet points or paragraphs, formatted in Markdown. If there's a table, this should ONLY contain insights on the table contents.", default="")
    recommendations: List[str] = Field(description="Action items or recommendations", default=[])
    slide_type: Literal['summary', 'content', 'action_items'] = Field(description="Type of slide")

class Presentation(BaseModel):
    slides: List[SlideContent]


class ReportGenerator(ABC):
    def __init__(self):
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_tokens=2000, temperature=0.4)
        self.output_parser = PydanticOutputParser(pydantic_object=Presentation)
        self.report_content: Presentation = []
        self.presentation = None
    
    def create_report(self, data: List[Document]) -> None:
        """Create complete report with all sections."""

        self.report_content = self.generate_report_content(data)
        self.report_content = self._post_process_content()

    @abstractmethod
    def generate_report_content(self, data: List[Document]) -> Presentation:
        pass
    
    def _post_process_content(self):
        for slide in self.report_content.slides:
            bulleted = list(map(lambda sentence: " - " + sentence if not sentence.strip().startswith("-") and not sentence.strip().endswith(":") else sentence, slide.content))
            slide.content = bulleted
        return self.report_content

class CFOReportGenerator(ReportGenerator):
    def generate_report_content(self, data: List[Document]) -> Presentation:
        prompt = PromptTemplate(
            template="""
            Based on the following financial data, generate a CFO report designed for presentation purposes:
            
            Requirements:
            1. Focus Areas:
                - Highlight the most critical financial metrics and identify key trends.
                - Conduct a concise cost analysis and provide insights into revenue streams.
                - Identify financial risks and opportunities for improvement.
        
            2. Structure of the Report:
                - Summary Slide: this slide should summarize only the most critical insights in a concise format, no recommendations. Keep it short.
                - Pages: Provide a detailed breakdown of the focus areas across at least two slides or pages, using bullet points, tables, or other visual aids for clarity.
                    - IMPORTANT: If you add a table, make sure to provide also a short insight on the displayed data.
                - Actionable Suggestions Slide: End the report with actionable, CFO-specific recommendations generated by the LLM. These should be practical, data-driven, and directly address the risks and opportunities identified.

            3. Additional Instructions:
            - NEVER repeat the same information in both tables and content. 
            - Don't bloat every slide with too much content, limit every slide content to 3-4 bullet points + potential table or data visualization
            - All the content should be formatted in Markdown
            - Use clear, professional language tailored for a CFO audience.
            - Focus on high-impact insights rather than excessive detail.
            - Prioritize data visualization and clarity in summarizations to facilitate quick decision-making.
            
            Data:
            {data}

            Format Instructions:
            {format_instructions}
            """,
            input_variables=["data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        chain= prompt | self.llm
        result = chain.invoke({"data": data})
        
        print("*" * 100)
        print(result)
        print("*" * 100)
        
        return self.output_parser.parse(result)

class CEOReportGenerator(ReportGenerator):
    def generate_report_content(self, data: Dict) -> Presentation:
        
        prompt = PromptTemplate(
            template="""
            Based on the following business data, generate a CEO report:

            Requirements:
            1. Focus Areas:
                - Present a high-level overview of business performance, emphasizing key achievements, growth metrics, and challenges.
                - Highlight strategic opportunities, including competitive positioning, market trends, and areas for innovation or expansion.
                - Provide a long-term outlook, detailing key decisions required to achieve organizational goals and sustain growth.
            
            2. Structure of the Report:
                - Summary Slide: Condense the most critical insights into a single, CONCISE and impactful bullet point list. Keep it short.
                - Pages: Include at least two slides or pages that detail:
                    - Business performance insights, with a focus on high-level metrics and trends.
                    - Strategic opportunities and market positioning, supported by relevant data or examples.
                - Actionable Suggestions Slide: Conclude the report with specific, forward-looking recommendations tailored to a CEO's strategic priorities. These should focus on growth opportunities, competitive advantages, and key decision points.

            3. Additional Instructions:
                - NEVER repeat the same information in both tables and content. 
                - Don't bloat every slide with too much content, limit every slide content to 3-4 bullet points + potential table or data visualization
                - All the content should be formatted in Markdown
                - Use concise language that aligns with a CEO's strategic perspective.
                - Prioritize actionable insights over granular detail, focusing on the broader business context.
            
            Data:
            {data}

            Format Instructions:
            {format_instructions}
            """,
            input_variables=["data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"data": data})
        return self.output_parser.parse(result)

class COOReportGenerator(ReportGenerator):
    def generate_report_content(self, data: Dict) -> Presentation:
        prompt = PromptTemplate(
            template="""
            Based on the following operational data, generate a COO report tailored for presentation purposes:

            Requirements:
            1. Focus Areas:
            - Present key operational performance metrics, including efficiency, productivity, and other relevant KPIs.
            - Identify areas of process inefficiencies and highlight bottlenecks affecting overall performance.
            - Provide insights into resource utilization and opportunities for optimization.
            
            2. Structure of the Report:
            - Summary Slide: Deliver a concise summary of the most critical operational insights, emphasizing metrics and trends that demand immediate attention. Keep it short.
            - Pages: Provide at least two slides or pages that delve into:
                - Detailed operational performance metrics, highlighting trends, progress, and problem areas.
                - Analysis of process efficiency, bottlenecks, and opportunities for improvement.
                - Resource utilization insights, with actionable suggestions for optimization.
            - Actionable Suggestions Slide: Conclude with targeted, data-driven recommendations that address inefficiencies, improve resource allocation, and enhance operational outcomes.

            
            Additional Instructions:
            - NEVER repeat the same information in both tables and content. 
            - Don't bloat every slide with too much content, limit every slide content to 3-4 bullet points + potential table or data visualization
            - All the content should be formatted in Markdown
            - Use clear, actionable language tailored for a COO's operational focus.
            - Emphasize efficiency and execution, avoiding excessive high-level abstraction.
            
            Data:
            {data}

            Format Instructions:
            {format_instructions}
            """,
            input_variables=["data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"data": data})
        return self.output_parser.parse(result)
    
