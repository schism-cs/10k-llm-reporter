from enum import Enum
from llmsherpa.readers import LayoutPDFReader, Block, Paragraph, Section, Table, ListItem, Document
from chromadb import Client, Settings
from langchain_community.embeddings import OpenAIEmbeddings
from dataclasses import dataclass, field

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

@dataclass
class ContentBlock:
    block_idx: int = 0
    bbox: tuple = (0,0,0,0)
    original_text: str = ""
    processed_text: str = ""
    page_idx: int = 0
    parent_chain: list[str] = field(default_factory=list)
    block_type: BlockType = BlockType.PARAGRAPH
    

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
        self.list_items.sort(key=lambda x: x.block_idx)
        
        current_list : List[ListItem] = []
        processed_lists : List[ContentBlock] = []
        
        for item in self.list_items:
            if not current_list:
                current_list.append(item)
            else:
                prev_idx = current_list[-1].block_idx
                curr_idx = item.block_idx
                
                if curr_idx == prev_idx + 1:
                    current_list.append(item)
                else:
                    processed_lists.append(self._aggregate_list_items(current_list))
                    current_list = [item]
        
        if current_list:
            processed_lists.append(self._aggregate_list_items(current_list))
        
        for p_l in processed_lists:
            self.content_blocks.append(p_l)
        
        return processed_lists
        
    def _aggregate_list_items(self, items: List[ListItem]) -> ContentBlock:
        """Combine list items into a single entry. Add context"""
        
        block = ContentBlock()
        block.block_idx = min([item.block_idx for item in items])
        block.bbox = (
            min([item.bbox[0] for item in items]),
            min([item.bbox[1] for item in items]),
            max([item.bbox[2] for item in items]),
            max([item.bbox[3] for item in items])
        )
        block.block_type = BlockType.LIST
        block.page_idx = min([item.page_idx for item in items])
        block.parent_chain = self._format_parent_chain(items[0])
        
        text = ""
        for item in items:
            text += " ".join(item.sentences)
            text += "\n"
        
        block.original_text = text
        block.processed_text = self._sanitize_text(text)
        
        return block
        
    def _process_tables(self):
        # to_text -> markdown + context (parent_chain)
        return []
    

from markdownify import markdownify as md
    
if __name__ == "__main__":
    pdf_processor = PDFProcessor()
    
    content_blocks = pdf_processor.extract_text("./data/2023-annual-report-short.pdf")
    
    pdf_processor.document_stats()

    for block in pdf_processor.content_blocks:
        if block.block_type == BlockType.LIST:
            print(block.parent_chain)
            print(block.processed_text)
            print()