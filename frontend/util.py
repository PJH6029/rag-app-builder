import streamlit as st
from wasabi import msg

from langchain_core.messages import AIMessage, HumanMessage

from rag.type import Chunk, CombinedChunks, TransformationResult
from rag.util import combine_chunks

def session_init(session_state):
    if "messages" not in session_state:
        session_state.messages = []
    if "translated_messages" not in session_state:
        session_state.translated_messages = []

def display_chat_history(session_state):
    for message in session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def write_queries(queries: TransformationResult):
    for i, k in enumerate(queries):
        st.markdown(f"- query {i+1}:")
        st.markdown(f"```\n{queries[k]}\n```")

def write_chunks(chunks: list[Chunk]):
    for i, chunk in enumerate(chunks):
        st.markdown(f"- chunk {i+1}:")
        st.markdown(f"```\n{chunk.text[:70]}...\n```")

def write_source_docs(chunks: list[Chunk]):
    combined_chunks = combine_chunks(chunks, attach_url=True)
    
    st.divider()
    st.markdown(f"# Total {len(chunks)} chunks")
    write_combined_chunks(combined_chunks)

def write_combined_chunks(combined_chunks: list[CombinedChunks]) -> None:
    for i, combined_chunk in enumerate(combined_chunks):
        st.markdown(f"## {combined_chunk.doc_meta.get('doc_name', 'Untitled')}")

        st.markdown(f"- Average Score: {combined_chunk.doc_mean_score:.2f}")
        if combined_chunk.link:
            st.markdown(f"- URL: [link]({combined_chunk.link})")
        
        for j, chunk in enumerate(combined_chunk.chunks):
            try:
                page = int(chunk.chunk_meta.get("page"))
            except ValueError:
                msg.warn(f"Page number is not an integer: {chunk.chunk_meta.get('page')}")
                page = None
            with st.expander(f"### Chunk {j+1} (page: {page if page else 'N/A'}, score: {chunk.score:.2f})"):
                with st.container(height=400):
                    st.markdown(chunk.text)
        
        if i < len(combined_chunks) - 1:
            st.divider()