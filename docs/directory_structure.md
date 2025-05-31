```
moonbase_qa/
├── app/ # アプリケーションのメインコード
│   ├── qa.py
│   ├── config.py
│   ├── ingest.py
│   ├── settings.py
│   └── ...
│
├── data/
│   ├── about_moon.pdf
│   ├── about_sun.pdf
│   └── questions.json
│
├── docs/
│
├── index/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
│
├── logs/
│   └── qa_log.jsonl
│
├── scripts/
│   ├── build_vectorstore.py       # ✅ 必須｜PDFを追加・削除・修正したら、毎回実行してインデックスを再構築する
│   ├── manual_run.py
│   └── multi_run.py
│
├── tests/
│   ├── manual_embedding_check.py  # ✅ 手動確認：chunkの分割数やベクトル次元などを確認
│   ├── manual_qa_run_log.py       # ✅ 手動確認：回答を生成してログを残す簡易チェック用スクリプト。source確認なし
│   ├── manual_vector_check.py     # ✅ 手動確認：実際にどのチャンクが使われたかを確認する詳細用スクリプト。
│   └── test_qa_search.py          # ✅ 自動テスト：pytest等の対象
│
├── main.py
├── poetry.lock        # 依存関係ロックファイル
├── pyproject.toml     # Poetry設定ファイル
├── README.md
├── .gitignore
```