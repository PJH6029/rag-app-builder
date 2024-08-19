from typing import Iterator, Optional, Union, Any, Iterable, Callable
from pathlib import Path
from wasabi import msg

from langchain_core.documents import Document
from langchain_community.document_loaders import RecursiveUrlLoader

from rag import util
from rag.component.loader.base import BaseRAGLoader
from rag.type import *

def extractor(raw_html: str) -> str:
    return util.markdownify(raw_html, strip=["footer", "a"])

class WebHTMLMarkdownifyLoader(BaseRAGLoader):
    def __init__(
        self,
        file_path: str,
        *,
        metadata_handler: Optional[Callable[[dict], tuple[dict, dict]]] = None,
    ) -> None:
        super().__init__(metadata_handler=metadata_handler)
        self.recursive_url_loader = RecursiveUrlLoader(
            url=file_path,
            extractor=extractor,
            max_depth=1,
        )

    def lazy_load(self) -> Iterator[Document]:
        return self.recursive_url_loader.lazy_load()
