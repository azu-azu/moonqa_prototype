# tests/test_qa_search.py

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

def test_faiss_search():
    db = FAISS.load_local(
        folder_path="index/faiss_index",
        embeddings=OpenAIEmbeddings(),
        index_name="index",
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        retriever=retriever
    )

    query = "月の構造について教えて"
    result = qa.invoke({"query": query})

    print("🔍 Answer:", result["result"])
    for i, doc in enumerate(result.get("source_documents", [])):
        print(f"\n📄 Doc {i+1}:")
        print("source:", doc.metadata.get("source"))
        print("excerpt:", doc.page_content[:100])

# 👇 これが実行トリガーやで！
if __name__ == "__main__":
    test_faiss_search()