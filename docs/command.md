# build_vectorstore.py 実行
- PDFを追加・削除・修正したら、毎回実行してインデックスを再構築する

```
python scripts/build_vectorstore.py
```

---

# test
## どのチャンクが使われたかを詳細確認する
```
python tests/manual_vector_check.py
```


## pytest
```
poetry run pytest
```


## ログ出力付きで実行する
```
poetry run pytest tests/test_qa_search.py --log-output
```

---

# ディレクトリ操作
## 削除
```
git rm xxx.py
```