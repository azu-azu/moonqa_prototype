qa_pdf/
├── app/ # アプリケーションのメインコード
│   ├── qa.py
│   ├── config.py
│   ├── ingest.py    # 🌙 CLI entry point｜PDF to chunk → embed → FAISS
│   ├── filters.py
│   ├── logger.py
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
│   ├── build_vectorstore.py       # ✅ 本番用｜PDFを追加・削除・修正したら、毎回実行してインデックスを再構築する
│   ├── manual_run.py              # 🔧 テスト用｜QAロジックの検証や、埋め込み結果の妥当性チェックに使用
│   └── multi_run.py               # 🔧 テスト用｜精度検証や回帰テストに使用
│   └── README.md                  # scriptsの使用方法
│
├── tests/
│   ├── log_utils.py               # 🔧 ログ関連のユーティリティ関数
│   ├── manual_embedding_check.py  # 🔧 手動確認：chunkの分割数やベクトル次元などを確認
│   ├── manual_qa_run_log.py       # 🔧 手動確認：回答を生成してログを残す簡易チェック用スクリプト。source確認なし
│   ├── manual_vector_check.py     # 🔧 手動確認：実際にどのチャンクが使われたかを確認する詳細用スクリプト。
│   └── test_qa_search.py          # 🔧 自動テスト：pytest等の対象
│
├── conftest.py        # pytest が自動で読み込む特殊ファイル：各種フック（pytest_addoption, pytest_configure）を定義
├── poetry.lock        # 依存関係ロックファイル
├── pyproject.toml     # Poetry設定ファイル
├── README.md
├── .gitignore
```
