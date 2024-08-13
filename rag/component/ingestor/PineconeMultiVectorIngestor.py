from typing import Optional, Iterable
from wasabi import msg
import time
import itertools

from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel, RunnablePassthrough

from rag.component.ingestor.base import BaseRAGIngestor
from rag.component.ingestor.PineconeVectorstoreIngestor import PineconeVectorstoreIngestor
from rag.type import Chunk
from rag.component import chunker, embeddings, llm
from rag.component.ingestor import prompt
from rag.util import time_logger

class ChunkGenerator:
    def __init__(
        self, 
        llm_model_name: str = "gpt-4o-mini",
        parent_id_key: str = "parent_id",
        lang: str = "English",
    ) -> None:
        self.llm_model_name = llm_model_name
        self.parent_id_key = parent_id_key
        self.lang = lang
        
        
    def generate(self, chunks: list[Chunk]) -> list[Chunk]:
        parallel_chain = RunnableParallel(
            split=RunnableLambda(self._split_runnable),
            summarize=RunnableLambda(self._summarize_runnable),
            hypothetical_query=RunnableLambda(self._hypothetical_query_runnable),
        )
        
        result = parallel_chain.invoke({"chunks": chunks})
        return list(itertools.chain(*result.values()))

    def _split_runnable(self, _dict):
        return self._split(_dict["chunks"])
    
    def _summarize_runnable(self, _dict):
        return self._summarize(_dict["chunks"])

    def _hypothetical_query_runnable(self, _dict):
        return self._hypothetical_query(_dict["chunks"])

    def _split(
        self, 
        chunks: list[Chunk],
        chunk_size: int = 400,
        chunk_overlap: int = 100,
        with_parent_mark: bool = True,
    ) -> list[Chunk]:
        with time_logger(
            lambda: f"Splitting {len(chunks)} chunks...",
            lambda: f"Splitting completed. {len(splitted_chunks)} chunks generated"
        ):
            # TODO temporal sub-chunking
            splitted_chunks = chunker.chunk_with(
                RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                ),
                chunks,
                with_parent_mark=with_parent_mark,
            )
            return splitted_chunks
    
    def _summarize(self, chunks: list[Chunk]) -> list[Chunk]:
        with time_logger(
            lambda: f"Summarizing {len(chunks)} chunks...",
            lambda: f"Summarizing completed. {len(new_chunks)} chunks generated"
        ):
            chunks = list(chunks)
        
            chain = prompt.summarize_prompt.partial(lang=self.lang) | llm.get_model(self.llm_model_name) | StrOutputParser()
            summaries = chain.batch([{"text": chunk.text, "doc_meta": chunk.doc_meta, "chunk_meta": chunk.chunk_meta} for chunk in chunks])
            new_chunks = []
            for chunk, summary in zip(chunks, summaries):
                new_chunk_id = f"{chunk.chunk_id}-summary"
                new_chunk = Chunk(
                    text=summary,
                    doc_id=chunk.doc_id,
                    chunk_id=new_chunk_id,
                    doc_meta={**chunk.doc_meta},
                    # chunk_meta={**chunk.chunk_meta, "chunk_id": new_chunk_id}
                    chunk_meta={**chunk.chunk_meta}, # TODO check if chunk_id is ingested
                )
                new_chunk.chunk_meta[self.parent_id_key] = chunk.chunk_id
                new_chunks.append(new_chunk)
            return new_chunks

    def _hypothetical_query(self, chunks: list[Chunk]) -> list[Chunk]:
        # reverse hyde
        with time_logger(
            lambda: f"Generating hypothetical queries for {len(chunks)} chunks...",
            lambda: f"Generating hypothetical queries completed. {len(new_chunks)} chunks generated"
        ):
            chunks = list(chunks)
        
            chain = prompt.hypothetical_queries_prompt.partial(lang=self.lang) | llm.get_model(self.llm_model_name) | StrOutputParser()
            queries_list = chain.batch([{"n": 3 , "text": chunk.text, "doc_meta": chunk.doc_meta, "chunk_meta": chunk.chunk_meta} for chunk in chunks])
            
            new_chunks = []
            for chunk, queries in zip(chunks, queries_list):
                queries = [q for q in queries.split("\n") if q]

                _new_chunks = []
                for i, query in enumerate(queries):
                    new_chunk_id = f"{chunk.chunk_id}-query-{i}"
                    new_chunk = Chunk(
                        text=query,
                        doc_id=chunk.doc_id,
                        chunk_id=new_chunk_id,
                        doc_meta=chunk.doc_meta,
                        chunk_meta={**chunk.chunk_meta, "chunk_id": new_chunk_id}
                    )
                    new_chunk.chunk_meta[self.parent_id_key] = chunk.chunk_id
                    _new_chunks.append(new_chunk)
                new_chunks.extend(_new_chunks)
            return new_chunks

class PineconeMultiVectorIngestor(BaseRAGIngestor):
    CHILD_INGESTION_CNT: int = 0
    
    def __init__(
        self,
        embeddings: Embeddings,
        parent_namespace: str,
        child_namespace: str,
        source_lang: str = "English",
    ) -> None:
        super().__init__()
        self.parent_ingestor = PineconeVectorstoreIngestor(
            embeddings=embeddings,
            namespace=parent_namespace
        )
        self.child_ingestor = PineconeVectorstoreIngestor(
            embeddings=embeddings,
            namespace=child_namespace
        )
        self._embeddings = embeddings
        self._parent_namespace = parent_namespace
        self._child_namespace = child_namespace
        self._source_lang = source_lang
    
    def ingest(self, chunks: list[Chunk]) -> bool:
        """In addition to the parent ingestion, this ingestor also chunks further and ingests the chunks into the child namespace.
 
        Args:
            chunks (list[Chunk]): List of chunks to ingest

        Returns:
            bool: True if ingestion is successful
        """
        
        msg.info(f"Ingesting {len(chunks)} chunks")
        chunk_generator = ChunkGenerator(lang=self._source_lang)
        children_chunks = chunk_generator.generate(chunks)
        
        parent_ingestion_cnt = self.parent_ingestor.ingest(chunks)
        child_ingestion_cnt = self.child_ingestor.ingest(children_chunks)
        PineconeMultiVectorIngestor.CHILD_INGESTION_CNT += child_ingestion_cnt

        num_chunk_ids = len(set([c.chunk_id for c in chunks]))
        if len(chunks) != num_chunk_ids:
            msg.warn(f"Duplicate chunk ids found in parent chunks. # of chunks: {len(chunks)}, # of unique chunk ids: {num_chunk_ids}")
            return 0
        
        num_child_chunk_ids = len(set([c.chunk_id for c in children_chunks]))
        if len(children_chunks) != num_child_chunk_ids:
            msg.warn(f"Duplicate chunk ids found in child chunks. # of chunks: {len(children_chunks)}, # of unique chunk ids: {num_child_chunk_ids}")
            return 0
    
        msg.good(f"{len(chunks)} chunks ingested into parent namespace `{self.parent_ingestor.namespace}`")
        msg.good(f"{len(children_chunks)} chunks ingested into child namespace `{self.child_ingestor.namespace}`")
        
        return parent_ingestion_cnt
    
    @classmethod
    def from_config(cls, config: dict) -> "PineconeMultiVectorIngestor":
        embeddings_name = config.get("embeddings")
        parent_namespace = config.get("namespace")
        child_namespace = config.get("sub-namespace")
        
        embeddings_model = embeddings.get_model(embeddings_name)
        
        source_lang = config.get("lang", {}).get("source", "English")
        
        return cls(
            embeddings=embeddings_model,
            parent_namespace=parent_namespace,
            child_namespace=child_namespace,
            source_lang=source_lang,
        )