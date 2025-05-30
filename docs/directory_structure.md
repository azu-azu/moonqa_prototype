```
moonbase_qa/
├── app/ # アプリケーションのメインコード
│   ├── qa.py
│   ├── config.py
│   ├── settings.py
│   └── ...
│
├── scripts/
│   ├── build_vectorstore.py
│   └── multi_run.py
│
├── docs/
│
├── tests/
│   ├── manual_embedding_check.py  # ✅ 手動確認：chunkの分割数やベクトル次元などを確認
│   ├── manual_qa_run_log.py       # ✅ 手動確認：回答を生成してログを残す簡易チェック用スクリプト。source確認は行わない。
│   ├── manual_vector_check.py     # ✅ 手動確認：実際にどのチャンクが使われたかを確認する詳細用スクリプト。
│   └── test_qa_search.py          # ✅ 自動テスト：pytest等の対象
│
├── data/
│   ├── about_moon.pdf
│   └── questions.json
│
├── logs/
│   └── qa_log.jsonl
│
├── index/
│   └── faiss_index/
│
├── pyproject.toml     # Poetry設定ファイル
├── poetry.lock        # 依存関係ロックファイル
├── README.md
├── main.py
├── .gitignore
```