-- ============================================================================
-- fee_cre_month パフォーマンス改善用インデックス作成SQL
-- ============================================================================
-- 実行前に必ずバックアップを取得してください
-- 実行時間: テーブルサイズにより5-30分程度かかる可能性があります
-- 
-- 注意: 既にインデックスが存在する場合はエラーが出ますが問題ありません
--       「Duplicate key name」エラーの場合はそのインデックスは既に存在しています
-- ============================================================================

-- 1. sql_fee_store テーブルのインデックス
-- メインクエリで使用される最重要インデックス
CREATE INDEX idx_fee_store_nyu_date 
ON sql_fee_store(nyu_date);

-- GROUP BY句で使用される複合インデックス
CREATE INDEX idx_fee_store_composite 
ON sql_fee_store(nyu_date, coltd_cd, syoken_cd_main, syoken_cd_sub);

-- カテゴリでのソートに使用
CREATE INDEX idx_fee_store_cat_cd 
ON sql_fee_store(cat_cd);


-- 2. sql_fee_order_store テーブルのインデックス
-- DELETE処理の高速化
CREATE INDEX idx_fee_order_store_nyu_date 
ON sql_fee_order_store(nyu_date);

-- UPDATE処理（kaime更新）の高速化
CREATE INDEX idx_fee_order_store_update 
ON sql_fee_order_store(nyu_date, kind_cd, coltd_cd, syoken_cd_main);


-- 3. sql_order_store テーブルのインデックス
-- JOIN条件で使用される複合インデックス
CREATE INDEX idx_order_store_composite 
ON sql_order_store(coltd_cd, syoken_cd_main, syoken_cd_sub);


-- 4. JOIN用テーブルのインデックス
-- sql_kei_nyu_pay
CREATE INDEX idx_kei_nyu_pay_int 
ON sql_kei_nyu_pay(nyu_year_month_int);

-- sql_staff (既に存在する可能性が高いが念のため)
CREATE INDEX idx_staff_cd 
ON sql_staff(staff_cd);

-- sql_gyotei
CREATE INDEX idx_gyotei_cd 
ON sql_gyotei(gyotei_cd);


-- ============================================================================
-- インデックス作成確認クエリ
-- ============================================================================
-- 以下のクエリで作成されたインデックスを確認できます

-- sql_fee_store のインデックス確認
SHOW INDEX FROM sql_fee_store;

-- sql_fee_order_store のインデックス確認
SHOW INDEX FROM sql_fee_order_store;

-- sql_order_store のインデックス確認
SHOW INDEX FROM sql_order_store;


-- ============================================================================
-- パフォーマンス確認用クエリ
-- ============================================================================
-- インデックス作成後、以下のクエリでEXPLAINを確認してください

-- EXPLAIN SELECT ... FROM sql_fee_store WHERE nyu_date = 202410;
-- type が "ref" または "range" になっていればインデックスが使用されています
-- type が "ALL" の場合はフルスキャンなので要確認

