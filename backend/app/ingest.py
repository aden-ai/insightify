# Script to ingest files (pdf/txt/urls) into the vector DB

# 1. ✅ FIXED: Imports moved to langchain_community
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader, TextLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from .config import settings
import os


# 2. ✅ FIXED: Using settings.openrouter_api_key (based on config.py file content)
#    Note: This assumes OpenRouter API key works for OpenAIEmbeddings API Base.
emb = OpenAIEmbeddings(
    openai_api_key=settings.openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1" 
)


# Example: load all pdfs in ./data
# DirectoryLoader is now correctly imported and uses UnstructuredPDFLoader
loader = DirectoryLoader('./data', glob='**/*.pdf', loader_cls=UnstructuredPDFLoader)
docs = loader.load()


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)


vectordb = Chroma(persist_directory=settings.vector_dir, embedding_function=emb)
vectordb.add_documents(chunks)
vectordb.persist()
print('Ingested', len(chunks), 'chunks')