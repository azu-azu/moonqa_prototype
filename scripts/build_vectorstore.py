# scripts/build_vectorstore.py

# ✅ 本番用スクリプト
# PDFからベクトルインデックスを構築して保存する
# 新しいPDFを追加・削除・修正したときに毎回実行する

import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# データとインデックスの保存先
DATA_DIR = "data"
INDEX_DIR = "index/faiss_index"

def load_all_pdfs(data_dir):
    all_docs = []

    # 複数のPDFファイルを読み込む
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))

    for pdf_path in pdf_files:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        file_name = os.path.basename(pdf_path)
        for i, page in enumerate(pages):
            # 表示用 source（ファイル名＋ページ番号）
            page.metadata["source"] = f"{file_name} (p.{i+1})"

            # フィルタ用 pdf_name（ファイル名のみ）
            page.metadata["pdf_name"] = file_name

        all_docs.extend(pages)

    return all_docs

def build_vectorstore(docs):
    # チャンク設定は用途に応じて調整可能
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    split_docs = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    vectorstore.save_local(INDEX_DIR)

if __name__ == "__main__":
    print("📄 PDFを読み込んでインデックスを作成中...")
    docs = load_all_pdfs(DATA_DIR)
    build_vectorstore(docs)
    print("✅ FAISSインデックス作成完了！")
