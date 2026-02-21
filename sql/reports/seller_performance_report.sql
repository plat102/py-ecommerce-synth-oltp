CREATE OR REPLACE FUNCTION seller_performance_report(
    p_start_date DATE,
    p_end_date DATE,
    p_category_id INT DEFAULT NULL,
    p_brand_id INT DEFAULT NULL
)
RETURNS TABLE (
    seller_id INT,
    seller_name VARCHAR,
    total_orders BIGINT,
    total_quantity BIGINT,
    total_revenue NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.seller_id,
        s.seller_name,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.subtotal) as total_revenue
    FROM seller s
    JOIN "order" o ON s.seller_id = o.seller_id
    JOIN order_item oi ON o.order_id = oi.order_id
    JOIN product p ON oi.product_id = p.product_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    AND (p_category_id IS NULL OR p.category_id = p_category_id)
    AND (p_brand_id IS NULL OR p.brand_id = p_brand_id)
    GROUP BY s.seller_id, s.seller_name
    ORDER BY total_revenue DESC;
END;
$$ LANGUAGE plpgsql;

-- Usage:
-- SELECT * FROM seller_performance_report('2025-08-01', '2025-10-31', NULL, NULL);
-- SELECT * FROM seller_performance_report('2025-08-01', '2025-10-31', 19, NULL);
