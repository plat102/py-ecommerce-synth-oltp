-- Required index
CREATE INDEX idx_order_item_product_id ON order_item(product_id);

-- Additional performance indexes ----------------------------------------------------------------
-- CREATE INDEX idx_order_date_desc ON "order"(order_date DESC);

-- create on parent table (if PostgreSQL version supports)
-- CREATE INDEX idx_order_item_prod_date ON order_item(product_id, order_date DESC);

-- CREATE INDEX idx_order_seller_date ON "order"(seller_id, order_date);
-- CREATE INDEX idx_order_status_date ON "order"(status, order_date);
-- CREATE INDEX idx_order_item_order_date ON order_item(order_date, product_id);


-- Indexes on partitions (if using partitioned tables) -------------------------------------------
-- CREATE INDEX idx_order_2025_10_date ON order_2025_10(order_date DESC);

-- Add composite index on each partition to eliminate sort
-- CREATE INDEX idx_order_item_2025_08_prod_date ON order_item_2025_08(product_id, order_date DESC);
-- CREATE INDEX idx_order_item_2025_09_prod_date ON order_item_2025_09(product_id, order_date DESC);
-- CREATE INDEX idx_order_item_2025_10_prod_date ON order_item_2025_10(product_id, order_date DESC);

-- CREATE INDEX idx_order_2025_08_seller ON order_2025_08(seller_id);
-- CREATE INDEX idx_order_2025_09_seller ON order_2025_09(seller_id);
-- CREATE INDEX idx_order_2025_10_seller ON order_2025_10(seller_id);

-- Analyze tables
-- ANALYZE "order";
-- ANALYZE order_item;
