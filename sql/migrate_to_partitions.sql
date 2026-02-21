-- Copy data from original table into partitioned table
-- 1: Migrate orders
INSERT INTO order_partitioned (order_id, order_date, seller_id, status, total_amount, created_at)
SELECT order_id, order_date, seller_id, status, total_amount, created_at
FROM "order";

-- 2: Migrate order items
INSERT INTO order_item_partitioned (order_item_id, order_id, product_id, order_date, quantity, unit_price, subtotal, created_at)
SELECT order_item_id, order_id, product_id, order_date, quantity, unit_price, subtotal, created_at
FROM order_item;

-- 3: Validate row counts
SELECT 'order' AS table_name,
    (SELECT COUNT(*) FROM "order") AS source_count,
    (SELECT COUNT(*) FROM order_partitioned) AS dest_count;

SELECT 'order_item' AS table_name,
    (SELECT COUNT(*) FROM order_item) AS source_count,
    (SELECT COUNT(*) FROM order_item_partitioned) AS dest_count;

-- 4: Validate partition distribution
SELECT 'order_2025_08' AS partition, COUNT(*) FROM order_2025_08
UNION ALL SELECT 'order_2025_09', COUNT(*) FROM order_2025_09
UNION ALL SELECT 'order_2025_10', COUNT(*) FROM order_2025_10;

SELECT 'order_item_2025_08' AS partition, COUNT(*) FROM order_item_2025_08
UNION ALL SELECT 'order_item_2025_09', COUNT(*) FROM order_item_2025_09
UNION ALL SELECT 'order_item_2025_10', COUNT(*) FROM order_item_2025_10;

-- 5: Swap table names (rename old -> _old, partitioned -> canonical)
ALTER TABLE "order" RENAME TO order_old;
ALTER TABLE order_item RENAME TO order_item_old;

ALTER TABLE order_partitioned RENAME TO "order";
ALTER TABLE order_item_partitioned RENAME TO order_item;

-- Step 6: Drop backup tables after confirming everything is correct
-- DROP TABLE order_old;
-- DROP TABLE order_item_old;
