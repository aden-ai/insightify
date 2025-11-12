import os
# Core Imports
from langchain_core.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI, OpenAIEmbeddings 
from langchain_chroma import Chroma
# The fix for your current error
# ✅ CORRECTED Import for RetrievalQA (using the full, detailed path)
from langchain_community.chains import RetrievalQA 

from .config import settings

# ✅ Setup embeddings + vector DB (Chroma)
embeddings = OpenAIEmbeddings(
    model=settings.embed_model,
    # ✅ FIXED: Using the general 'api_key' setting
    openai_api_key=settings.api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

chroma_persist_dir = settings.vector_dir
os.makedirs(chroma_persist_dir, exist_ok=True)

vectordb = Chroma(persist_directory=chroma_persist_dir, embedding_function=embeddings)

# ✅ Initialize Llama-3 through OpenRouter
llm = ChatOpenAI(
    model=settings.llm_model,
    temperature=0.2,
    # ✅ FIXED: Using the general 'api_key' setting
    openai_api_key=settings.api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

# ✅ PROMPT Template (now properly imported)
PROMPT = PromptTemplate(
    input_variables=["question", "context"],
    template=(
        "You are a concise and intelligent assistant.\n\n"
        "Context:\n{context}\n\n"
        "Question:\n{question}\n\n"
        "Answer clearly and briefly. Cite sources if available."
    )
)

retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
# ✅ Uses the corrected RetrievalQA import
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", # Explicitly setting chain_type is good practice
    retriever=retriever, 
    return_source_documents=True,
    # ✅ FIXED: Uncommented to apply custom prompt
    chain_type_kwargs={"prompt": PROMPT} 
) 

# ✅ run_rag is already correctly defined to accept 'mode'
def run_rag(text: str, mode: str = "summary") -> dict:
    query = text if mode == "summary" else f"{mode}: {text}"
    result = qa_chain.invoke({"query": query})
    return {
        "summary": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }