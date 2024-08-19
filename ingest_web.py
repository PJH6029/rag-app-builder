import os

from langchain_community.document_loaders import TextLoader

from rag.api import upload_data, ingest_data
from rag.component.ingestor.PineconeMultiVectorIngestor import PineconeMultiVectorIngestor
from rag.component.loader.WebHTMLMarkdownifyLoader import WebHTMLMarkdownifyLoader



url = "https://yann.lecun.com/exdb/mnist/"

if not os.path.exists("md_test"):
    os.makedirs("md_test")

# for i, doc in enumerate(WebHTMLMarkdownifyLoader(url).lazy_load()):
#     print(doc.page_content)
#     print(doc.metadata)
#     print("=" * 80)
    
#     with open(f"md_test/md_{i}.md", "w") as f:
#         f.write(doc.page_content)

ingest_data(
    # WebHTMLMarkdownifyLoader(url),
    TextLoader("requirements.txt"),
)