from typing import Generator, Any, Optional
from wasabi import msg

from langchain_community.callbacks import get_openai_callback
from langchain.globals import set_debug

from rag.rag_manager import RAGManager
from rag import util
from rag.type import *

recent_chunks = None
recent_translated_query = None
rag_manager = None

# TODO make config class
DEFAULT_RAG_CONFIG = {
    "global": {
        "lang": {
            "user": "Korean",
            "source": "Korean",
        }
    },
    "ingestion": { # optional
        "ingestor": "pinecone-multivector",
        "embeddings": "text-embedding-3-small",
        "namespace": "parent",
        "sub-namespace": "child",
    },
    "transformation": { # optional
        "model": "gpt-4o-mini",
        "enable": {
            "translation": True, # if English, unnecessary
            "rewriting": True,
            "expansion": False,
            "hyde": True,
        },
    },
    "retrieval": { # mandatory
        # "retriever": ["pinecone-multivector", "kendra"],
        "retriever": ["pinecone-multivector"],
        # "weights": [0.5, 0.5],
        
        "namespace": "parent",
        "sub-namespace": "child",
        
        "embeddings": "text-embedding-3-small", # may be optional
        "top_k": 6, # for multi-vector retriever, context size is usually big. Use small top_k
    },
    "generation": { # mandatory
        "model": "gpt-4o",
    },
    "fact_verification": { # optional
        "model": "gpt-4o-mini",
        "enable": False,
    },
}

def init():    
    util.load_secrets()
    global rag_manager
    rag_manager = RAGManager()
    
    config = util.load_config()
    if config is None:
        msg.warn("No config provided. Using default config.")
        _config = DEFAULT_RAG_CONFIG
    else:
        _config = config
    rag_manager.set_config(_config)

init()

def query(query: str, history: list[ChatLog]=None) -> GenerationResult:
    history = history or []
    with get_openai_callback() as cb:
        queries = rag_manager.transform_query(query, history)
        translated_query = queries["translation"]
        chunks = rag_manager.retrieve(queries)
        
        global recent_chunks, recent_translated_query
        recent_chunks = chunks
        recent_translated_query = translated_query

        generation_response = rag_manager.generate(translated_query, history, chunks)
        verification_response = rag_manager.verify_fact(generation_response, chunks)
        
        print(cb)
    return util.remove_falsy({"transformation": queries, "retrieval": chunks, "generation": generation_response, "fact_verification": verification_response})
    

def query_stream(query: str, history: list[ChatLog]=None) -> Generator[GenerationResult, None, None]:
    history = history or []
    with get_openai_callback() as cb:
        queries = rag_manager.transform_query(query, history)
        yield {"transformation": queries}
        
        translated_query = queries["translation"]
        chunks = rag_manager.retrieve(queries)
        yield {"retrieval": chunks}
        
        global recent_chunks, recent_translated_query
        recent_chunks = chunks
        recent_translated_query = translated_query

        generation_response = ""
        for response in rag_manager.generate_stream(translated_query, history, chunks):
            yield {"generation": response}
            generation_response += response
        
        verification = rag_manager.verify_fact(generation_response, chunks)
        if verification is not None:
            yield {"fact_verification": rag_manager.verify_fact(generation_response, chunks)}
        
        print(cb)
    
def upload_data(file_path: str, object_location: str, metadata: Optional[dict] = None) -> bool:
    return rag_manager.upload_data(file_path, object_location, metadata)

def ingest_data(file_path: str) -> int:
    return rag_manager.ingest(file_path)

async def aingest_data(s3_url: str) -> int:
    return await rag_manager.aingest(s3_url)

def ingest_from_backup(backup_dir: str, object_location: str) -> int:
    return rag_manager.ingest_from_backup(backup_dir, object_location)
