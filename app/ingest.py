# app/ingest.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from app.config import get_pdf_path, get_index_path

def ingest():
    # Load PDF
    loader = PyPDFLoader(get_pdf_path())
    documents = loader.load()

    # Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(documents)

    # Embed and index
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding)

    # Save index
    vectorstore.save_local(get_index_path())
