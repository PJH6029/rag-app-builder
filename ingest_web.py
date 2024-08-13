import os

from rag.api import upload_data, ingest_data, ingest_from_backup
from rag.component.ingestor.PineconeMultiVectorIngestor import PineconeMultiVectorIngestor
from rag.component.loader.HTMLMarkdownifyLoader import HTMLMarkdownifyLoader

url = "https://python.langchain.com/v0.2/docs/integrations/document_loaders/recursive_url/"

for i, doc in enumerate(HTMLMarkdownifyLoader(url).lazy_load()):
    print(doc.page_content)
    print(doc.metadata)
    print("=" * 80)
    
    with open(f"md_{i}.md", "w") as f:
        f.write(doc.page_content)