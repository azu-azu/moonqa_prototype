# app/qa.py

import argparse
import os
import pickle
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OpenAIEmbeddings

# .env を読み込む
load_dotenv()

# --- FAISSインデックスを読み込む ---
def load_faiss_index():
    vectorstore = FAISS.load_local(
        folder_path="index/faiss_index",
        embeddings=OpenAIEmbeddings(),
        index_name="index",
        allow_dangerous_deserialization=True # 👈 これが必要
    )
    return vectorstore

# --- 質問応答処理 ---
def question_answer(query):
    vectorstore = load_faiss_index()
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo"
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    return qa.run(query)

# --- Markdown形式でログを追記保存 ---
def append_markdown_log(question: str, answer: str):
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/qa_log.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n## 💬 Question\n{question}\n\n## 📖 Answer\n{answer}\n\n---\n")

# --- CLI実行 ---
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True, help="質問を入力してください")
    args = parser.parse_args()

    answer = question_answer(args.question)
    append_markdown_log(args.question, answer)
    print(f"💬 質問: {args.question}\n💡 回答: {answer}")

if __name__ == "__main__":
    main()
