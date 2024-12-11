from enum import Enum
from llmsherpa.readers import LayoutPDFReader, Block, Paragraph, Section, Table, ListItem, Document
from chromadb import Client, Settings
from langchain_community.embeddings import OpenAIEmbeddings


import json
import os
from typing import List, Dict, NamedTuple

class BlockType(Enum):
    PARAGRAPH = 0
    HEADER = 1
    LIST = 2
    TABLE = 3

class ParsedDocument:
    pass

class ContentBlock(NamedTuple):
    block_idx: int
    bbox: tuple
    original_text: str
    processed_text: str
    page_idx: int
    parent_chain: list[str]
    block_type: BlockType

class PDFProcessor:
    def __init__(self):
        self.pdf_reader = LayoutPDFReader("http://localhost:5010/api/parseDocument?renderFormat=all&useNewIndentParser=true")
        
        self.all_chunks: Dict[int, Block]= {}
        self.paragraphs: List[Paragraph]= []
        self.headers: List[Section]= []
        self.list_items: List[ListItem] = []
        self.tables: List[Table] = []
        
        self.content_blocks: List[ContentBlock] = []
    
    def extract_text(self, pdf_path: str) -> List[ContentBlock]:
        """Extract and process different types of content from PDF."""
        doc = self.pdf_reader.read_pdf(pdf_path)
        
        self._categorize_document_blocks(doc)
        self._process_paragraphs()
        self._process_list_items()
        self._process_tables()
        
        return self.content_blocks
    
    def document_stats(self):
        print(f"All chunks: {len(self.all_chunks)}")
        print(f"Paragraphs: {len(self.paragraphs)}")
        print(f"List items: {len(self.list_items)}")
        print(f"Tables: {len(self.tables)}")        
        print(f"Sections: {len(self.headers)}")        
    
    def _categorize_document_blocks(self, document: Document):
        chunk : Block
        for chunk in document.chunks():
            if chunk.tag == "para":
                self.paragraphs.append(chunk)
            elif chunk.tag == "list_item":
                self.list_items.append(chunk)
            elif chunk.tag == "table":
                self.tables.append(chunk)
                
        section : Section
        for section in document.sections():
            self.headers.append(section)
    
    def _process_paragraphs(self):
        for para in self.paragraphs:
            merged_text_content = self._merge_sentences(para)
            block = ContentBlock(
                block_idx = para.block_idx,
                bbox = para.bbox,
                block_type = BlockType.PARAGRAPH,
                original_text = merged_text_content,
                processed_text = self._sanitize_text(merged_text_content),
                page_idx=para.page_idx,
                parent_chain=self._format_parent_chain(para)
            )
            self.content_blocks.append(block)    
    
    @staticmethod
    def _sanitize_text(text: str) -> str:
        return text
    
    @staticmethod
    def _merge_sentences(block: Block) -> str:
        return " ".join(block.sentences)
    
    @staticmethod
    def _format_parent_chain(block: Block) -> str:
        ancestors = [a.title for a in block.parent_chain() if isinstance(a, Section)]
        return " > ".join(ancestors)
    
    def _process_list_items(self):
        # aggregate by id
        return []
        
    def _process_tables(self):
        # to_text -> markdown + context (parent_chain)
        return []
    

from markdownify import markdownify as md
    
if __name__ == "__main__":
    pdf_processor = PDFProcessor()
    
    content_blocks = pdf_processor.extract_text("./data/2023-annual-report-short.pdf")
    
    pdf_processor.document_stats()
    
    for t in pdf_processor.tables:
        print(t.to_context_text())
        print("=" * 80)
        print(t.to_html())
        print("Markdown")
        print(md(t.to_html()))