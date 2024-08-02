# LLM Project

Application builder for Advanced RAG, based on Pinecone vectorstore

- OpenAI LLM, embedding model
- Upstage Layout Analyzer

## Description

## Installation

1. install requirements
    - `pip install -r requirements.txt`

2. create pinecone index
    - from console: [pinecone-console](https://app.pinecone.io/)
    - from code: [documentation](https://docs.pinecone.io/guides/indexes/create-an-index)

3. set environments
    - Set API Keys to `.streamlit/secrets.toml` (already registered in `.gitignore`)
    - `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, ...

## Usage

### Data ingestion
`ingest.py`

1. Source documents
    - `<repo_path>/source_documents/`에 file들을 upload
    - metadata 제공을 위해선, 동일 위치에 `.metadata.json` format으로 제공
        - ex. `source_documents/doc1/test.pdf`, `source_documents/doc1/test.pdf.metadata.json`

2. Upload to S3 (optional)
    - If you want to provide link in your app, you can upload your file to S3 first.
    - Additional environment setting is required. (`S3_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`)
    - `upload_to_s3`는 자동으로 `.metadata.json`을 찾아 함께 업로드. `metadata: dict` argument로 maual하게 줄 수도 있음 (자동으로 `.metadata.json` 생성)
3. Ingest data
    - `ingest()`
    - configuration에 지정한 namespace를 자동으로 생성하여 ingest

### Run

`streamlit run chat.py`