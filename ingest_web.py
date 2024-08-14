import os

from rag.api import upload_data, ingest_data, ingest_from_backup
from rag.component.ingestor.PineconeMultiVectorIngestor import PineconeMultiVectorIngestor
from rag.component.loader.HTMLMarkdownifyLoader import HTMLMarkdownifyLoader

url = "https://www.op.gg/summoners/kr/%EC%A7%84%EC%A7%9C%EB%B0%95%EC%A0%95%ED%9B%88-KRI"

for i, doc in enumerate(HTMLMarkdownifyLoader(url).lazy_load()):
    print(doc.page_content)
    print(doc.metadata)
    print("=" * 80)
    
    with open(f"md_test/md_{i}.md", "w") as f:
        f.write(doc.page_content)