CREATE OR REPLACE FUNCTION orders_status_summary(
    p_start_date DATE,
    p_end_date DATE,
    p_seller_ids INT[] DEFAULT NULL,
    p_category_ids INT[] DEFAULT NULL
)
RETURNS TABLE (
    status VARCHAR,
    total_orders BIGINT,
    total_revenue NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    WITH filtered_orders AS (
        SELECT DISTINCT
            o.order_id AS fo_order_id,
            o.status AS fo_status,
            o.total_amount AS fo_total_amount
        FROM "order" o
        LEFT JOIN order_item oi ON o.order_id = oi.order_id
        LEFT JOIN product p ON oi.product_id = p.product_id
        WHERE o.order_date BETWEEN p_start_date AND p_end_date
        AND (p_seller_ids IS NULL OR o.seller_id = ANY(p_seller_ids))
        AND (p_category_ids IS NULL OR p.category_id = ANY(p_category_ids))
    )
    SELECT
        fo_status,
        COUNT(fo_order_id) as total_orders,
        SUM(fo_total_amount) as total_revenue
    FROM filtered_orders
    GROUP BY fo_status
    ORDER BY total_orders DESC;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM orders_status_summary('2025-08-01', '2025-10-31', NULL, NULL);
SELECT * FROM orders_status_summary('2025-08-01', '2025-10-31', ARRAY[19, 11]);
SELECT * FROM orders_status_summary('2025-08-01', '2025-10-31', ARRAY[6, 3]);
SELECT * FROM orders_status_summary('2025-08-01', '2025-10-31', ARRAY[19, 11], ARRAY[6, 3]);
