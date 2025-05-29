# tests/run_qa_test.py

from app.qa import load_vectorstore, get_answer, append_json_log

if __name__ == "__main__":
    vectorstore = load_vectorstore()
    question = "このPDFは何について書かれていますか？"
    answer, docs_and_scores = get_answer(question, vectorstore)

    print("💬 質問:", question)
    print("💡 回答:", answer)
    print("\n🔍 スコア付き文書:\n")
    for doc, score in docs_and_scores:
        print(f"- score: {score:.3f}")
        print(f"  content: {doc.page_content[:100]}...\n")

    append_json_log(question, answer, docs_and_scores)
