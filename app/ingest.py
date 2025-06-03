# app/ingest.py

import json
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from app.config import get_pdf_path, get_index_path
from app.settings import CHUNK_SIZE, CHUNK_OVERLAP

# jsonからメタ情報を読み込む
def load_pdf_meta():
    with open("data/pdf_meta.json", "r", encoding="utf-8") as f:
        return json.load(f)

def ingest():
    # Load PDF
    loader = PyPDFLoader(get_pdf_path())
    documents = loader.load()

    # ファイル名取得
    pdf_path = get_pdf_path()
    filename = pdf_path.name
    pdf_meta = load_pdf_meta()
    meta = pdf_meta.get(filename, {})

    # Split text
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    # メタデータを各チャンクに追加
    for i, chunk in enumerate(chunks):
        # 表示用 source（ファイル名＋ページ番号）
        chunk.metadata["source"] = f"{filename} (p.{chunk.metadata.get('page', i+1)})"
        # フィルタ用 pdf_name（ファイル名のみ）
        chunk.metadata["pdf_name"] = filename
        if "tag" in meta:
            chunk.metadata["tag"] = meta["tag"]
        if "date" in meta:
            chunk.metadata["date"] = meta["date"]

    # Embed and index
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embedding)

    # Save index
    vectorstore.save_local(get_index_path())
