# PDFからチャンクを作って、ベクトル化して、FAISSに保存する、「学習データのインデックスを作る専用スクリプト」

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

# 対象PDFファイル
pdf_path = "data/about_moon.pdf"

# 1. 読み込み
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# チャンクに "source" を付ける
for i, page in enumerate(pages):
    page.metadata["source"] = f"{os.path.basename(pdf_path)} (p.{i+1})"

# 2. 分割（チャンク設計を自由に調整可）
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
docs = splitter.split_documents(pages)

# 3. 埋め込み
embedding = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embedding)

# 4. 保存（保存先は app/config.py の get_index_path() を参照する前提でもOK）
os.makedirs("index", exist_ok=True)
db.save_local("index/faiss_index")

print("✅ FAISSインデックス保存完了！")
