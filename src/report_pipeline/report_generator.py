import os
from typing import Dict, List, Literal
from dotenv import load_dotenv
from abc import ABC, abstractmethod

from langchain_openai import OpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.documents import Document
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field, RootModel

load_dotenv()

class SlideContent(BaseModel):
    title: str = Field(description="Section title")
    content: List[str] = Field(description="Bullet points or paragraphs")
    recommendations: List[str] = Field(description="Action items or recommendations")
    slide_type: Literal['cover', 'content', 'action_items'] = Field(description="Type of slide")


class Presentation(RootModel):
    root: List[SlideContent]


class ReportGenerator(ABC):
    def __init__(self):
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_tokens=2000)
        self.output_parser = PydanticOutputParser(pydantic_object=Presentation)
        self.report_content: Presentation = []
        self.presentation = None
    
    def create_report(self, data: List[Document]) -> None:
        """Create complete report with all sections."""

        self.report_content = self.generate_report_content(data)
        
        self._create_cover_slide()
        self._create_content_slides()
        self._create_action_items_slide()

    @abstractmethod
    def generate_report_content(self, data: List[Document]) -> Presentation:
        pass
    
    def _create_cover_slide(self):
        pass
        
    def _create_content_slides(self):
        pass
    
    def _create_action_items_slide(self):
        pass
        

class CFOReportGenerator(ReportGenerator):
    def generate_report_content(self, data: List[Document]) -> Presentation:
        prompt = PromptTemplate(
            template="""
            Based on the following financial data, create a CFO report:
            {data}
            
            Focus on:
            1. Key financial metrics and trends
            2. Cost analysis and revenue insights
            3. Financial risks and opportunities
            
            Each report should have:
            - a first cover slide containing only the most critical information
            - at least two slides or pages containing summarizations
            - a final slide providing LLM action item suggestions
            
            {format_instructions}
            """,
            input_variables=["data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        chain= prompt | self.llm
        result = chain.invoke({"data": data})
        
        return self.output_parser.parse(result)

class CEOReportGenerator(ReportGenerator):
    def generate_report_content(self, data: Dict) -> Presentation:
        prompt = PromptTemplate(
            template="""
            Based on the following business data, create a CEO report:
            {data}
            
            Focus on:
            1. High-level business performance
            2. Strategic opportunities and market position
            3. Long-term outlook and key decisions
            
            Each report should have:
            - a first cover slide containing critical information
            - at least two slides or pages containing summarizations
            - a final slide providing LLM action item suggestions
            
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
            Based on the following operational data, create a COO report:
            {data}
            
            Focus on:
            1. Operational performance metrics
            2. Process efficiency and bottlenecks
            3. Resource utilization and optimization
            
            Each report should have:
            - a first cover slide containing critical information
            - at least two slides or pages containing summarizations
            - a final slide providing LLM action item suggestions
            
            {format_instructions}
            """,
            input_variables=["data"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm
        result = chain.invoke({"data": data})
        return self.output_parser.parse(result)