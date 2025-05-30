# tests/manual_vector_check.py

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

def manual_vector_check():
    db = FAISS.load_local(
        folder_path="index/faiss_index",
        embeddings=OpenAIEmbeddings(),
        index_name="index",
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        retriever=retriever,
        return_source_documents=True  # 🔑 これ重要！
    )

    # question = "このPDFは何について書かれていますか？"
    # question = "月って何？"
    # question = "月の特徴は？"
    question = "月って、どうやってできたの？"
    # question = "地球とはどんな関係にあるの？"
    # question = "なんか面白いこと教えて。"

    result = qa.invoke({"query": question})

    print("💬 質問:", question)
    print("💡 回答:", result["result"])
    print("\n🔍 ソース付きチャンク確認:\n")

    for i, doc in enumerate(result["source_documents"]):
        print(f"--- Doc {i+1} ---")
        print("📁 source:", doc.metadata.get("source", "❌ 不明"))
        print("📝 content preview:")
        print(doc.page_content[:300])
        print()

if __name__ == "__main__":
    manual_vector_check()
