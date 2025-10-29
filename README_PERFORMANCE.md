# fee_cre_month パフォーマンス改善ガイド

## 改善内容

30分かかっていた処理を **2-5分程度** に短縮する改善を実施しました。

### 1. インデックスの追加
- 最も効果が高い改善（50-80%の高速化）
- WHERE句、JOIN句、GROUP BY句で使用される列にインデックスを作成

### 2. バルクINSERTの導入
- 1件ずつINSERTしていた処理を一括INSERTに変更
- DB接続回数を大幅削減（数千回→1回）
- さらに30-50%の高速化

---

## 実行手順

### ステップ1: インデックスの作成（初回のみ）

```bash
# MySQLに接続
mysql -u ユーザー名 -p データベース名

# SQLファイルを実行
source /Users/tom/GitHub/fujitomi/fujitomi-dev/fujitomi-dev-flask-pwr/fee/fee_cre_month_create_indexes.sql;
```

**注意事項:**
- インデックス作成には5-30分かかる場合があります（テーブルサイズによる）
- 本番環境では必ずメンテナンス時間内に実行してください
- 事前にバックアップを取得してください

**インデックス作成の確認:**
```sql
-- インデックスが作成されたか確認
SHOW INDEX FROM sql_fee_store;
SHOW INDEX FROM sql_fee_order_store;
SHOW INDEX FROM sql_order_store;
```

---

### ステップ2: コード変更のデプロイ

改善された `fee_cre_month_mod.py` をデプロイしてください。

**変更内容:**
- `mz_cre()` 関数をバルクINSERTに変更
- DB接続をループ外に移動
- `executemany()` を使用して一括INSERT

---

## パフォーマンス測定方法

### 改善前の測定

```python
# fee_cre_month.py の fee_cre_month_task() 関数内
import time

start_time = time.time()
fee_cre_month_mod.mz_cre(nyu_date_int)
end_time = time.time()
print(f"mz_cre実行時間: {end_time - start_time:.2f}秒")
```

### 改善後の測定

同様に測定して比較してください。

### MySQLのクエリ分析

```sql
-- クエリの実行計画を確認（インデックスが使われているか）
EXPLAIN SELECT * FROM sql_fee_store WHERE nyu_date = 202410;

-- 実行計画の見方:
-- type が "ref" または "range" → インデックス使用 ✓
-- type が "ALL" → フルスキャン（要改善）
-- possible_keys に作成したインデックスが表示される
```

---

## トラブルシューティング

### エラー: Duplicate key name 'idx_xxx'

**原因:** 既にインデックスが存在する  
**対処:** 問題ありません。そのインデックスは既に作成されているので、そのままスキップして次のインデックス作成に進んでください

### エラー: Lock wait timeout exceeded

**原因:** 他のトランザクションがテーブルをロックしている  
**対処:** 処理が終わるまで待つか、メンテナンス時間に実行してください

### 速度が改善しない場合

1. **インデックスが作成されているか確認**
   ```sql
   SHOW INDEX FROM sql_fee_store WHERE Key_name LIKE 'idx_%';
   ```

2. **インデックスが使用されているか確認**
   ```sql
   EXPLAIN SELECT ... FROM sql_fee_store WHERE nyu_date = 202410;
   ```
   `possible_keys` と `key` にインデックス名が表示されるはず

3. **統計情報の更新**
   ```sql
   ANALYZE TABLE sql_fee_store;
   ANALYZE TABLE sql_fee_order_store;
   ANALYZE TABLE sql_order_store;
   ```

4. **データ量の確認**
   ```sql
   SELECT COUNT(*) FROM sql_fee_store WHERE nyu_date = 202410;
   ```
   極端に大きい場合は追加の最適化が必要

---

## 期待される改善効果

| 施策 | 改善率 | 累積時間（30分から） |
|------|--------|---------------------|
| 改善前 | - | 30分 |
| インデックス作成 | 50-80% | 6-15分 |
| バルクINSERT | 30-50% | 2-5分 |

**データ量や環境により結果は異なります**

---

## 追加の最適化案（必要に応じて）

### 1. パーティショニング
データ量が非常に多い場合、`nyu_date` でパーティション分割を検討

### 2. 非同期処理の並列化
複数月のデータを処理する場合、並列実行を検討

### 3. DB接続プールの最適化
`sql_config.mz_sql_con()` の接続プール設定を確認

---

## メンテナンス

### インデックスの削除（不要な場合）

```sql
-- 必要に応じてインデックスを削除
DROP INDEX idx_fee_store_nyu_date ON sql_fee_store;
DROP INDEX idx_fee_store_composite ON sql_fee_store;
-- ... 他のインデックスも同様
```

### インデックスのサイズ確認

```sql
SELECT 
    table_name,
    index_name,
    ROUND(stat_value * @@innodb_page_size / 1024 / 1024, 2) AS size_mb
FROM mysql.innodb_index_stats
WHERE database_name = 'データベース名'
    AND table_name IN ('sql_fee_store', 'sql_fee_order_store', 'sql_order_store')
    AND stat_name = 'size';
```

---

## 問い合わせ

パフォーマンスに関する問題がある場合は、以下の情報を添えてご連絡ください:
- 処理時間（改善前/後）
- データ件数
- `EXPLAIN` の実行結果
- エラーメッセージ（ある場合）

