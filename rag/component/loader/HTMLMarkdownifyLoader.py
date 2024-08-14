from typing import Iterator, Optional, Union, Any
from pathlib import Path
import os
from wasabi import msg

from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_community.document_loaders import RecursiveUrlLoader

from rag import util

def extractor(raw_html: str) -> str:
    return util.markdownify(raw_html, strip=["footer", "a"])

class HTMLMarkdownifyLoader(BaseLoader):
    def __init__(
        self,
        file_path: str,
    ) -> None:
        super().__init__()
        self.recursive_url_loader = RecursiveUrlLoader(
            url=file_path,
            extractor=extractor,
            max_depth=1,
        )

    def lazy_load(self) -> Iterator[Document]:
        return self.recursive_url_loader.lazy_load()
