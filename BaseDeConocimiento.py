from langchain_chroma import Chroma
import chromadb

def get_chroma_vector_store(splits, embeddings):
    return Chroma.from_documents(documents=splits, embedding=embeddings);
