from typing import List
from langchain_core.documents import Document

class SearchResults:
    def __init__(self) -> None:
        self.unique_docs: List[Document] = []
        self.doc_ids: List[int] = []
        
    def add_result(self, document: Document):
        if document.metadata["block_idx"] in self.doc_ids:
            return
        self.unique_docs.append(document)
        self.doc_ids.append(document.metadata["block_idx"])
        
    def get_results(self) -> List[Document]:
        return self.unique_docs