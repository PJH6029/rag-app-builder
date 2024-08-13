import os

from rag.api import upload_data, ingest_data, ingest_from_backup
from rag.component.ingestor.PineconeMultiVectorIngestor import PineconeMultiVectorIngestor

source_doc_dir = "source_documents"
source_doc_root = os.path.join(os.path.dirname(__file__), source_doc_dir)

def upload_to_s3():
    for root, dirs, files in os.walk(source_doc_root):
        for file in files:
            if not file.endwith(".pdf"):
                continue
            file_path = os.path.join(root, file)
            object_location = os.path.relpath(file_path, source_doc_root)
            upload_data(file_path, f"{source_doc_dir}/{object_location}")

# def prepare_metadata():
#     for root, dirs, files in os.walk(source_doc_root):
#         for file in files:
#             if not file.endwith(".pdf"):
#                 continue
#             file_path = os.path.join(root, file)
#             object_location = os.path.relpath(file_path, source_doc_root)
#             generate_metadata(file_path, metadata=metadata)

def ingest():
    cnt = 0
    PineconeMultiVectorIngestor.CHILD_INGESTION_CNT = 0
    for root, dirs, files in os.walk(source_doc_root):
        for file in files:
            if not file.endswith(".pdf"):
                continue
            file_path = os.path.join(root, file)
            cnt += ingest_data(file_path)
    
    print(f"{cnt} parent chunks ingested")
    print(f"{PineconeMultiVectorIngestor.CHILD_INGESTION_CNT} child chunks ingested")
    
def ingest_from_backup():
    cnt = ingest_from_backup("./backup")
    print(f"{cnt} parent chunks ingested")
    

if __name__ == "__main__":
    # upload()
    ingest()
    # ingest_from_backup()