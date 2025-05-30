# tests/test_embedding.py

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from app.config import get_pdf_path

def test_embedding_vector_output():
    # PDF読み込み
    loader = PyPDFLoader(get_pdf_path())
    documents = loader.load()

    # チャンク分割
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(documents)

    # ベクトル化
    embedding = OpenAIEmbeddings()
    vectors = embedding.embed_documents([chunk.page_content for chunk in chunks])

    # 出力確認
    print(f"✅ chunk数: {len(vectors)}")
    print(f"✅ 1つあたりのベクトル次元: {len(vectors[0])}")
    print(f"✅ 最初のベクトル例: {vectors[0][:10]}...")  # 先頭10要素だけ

if __name__ == "__main__":
    test_embedding_vector_output()
