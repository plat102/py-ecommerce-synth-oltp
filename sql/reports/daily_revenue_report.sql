CREATE OR REPLACE FUNCTION daily_revenue_report(
  p_start_date DATE,
  p_end_date DATE,
  p_product_ids INT[] DEFAULT NULL
  )
RETURNS TABLE (
    date DATE,
    total_orders BIGINT,
    total_quantity BIGINT,
    total_revenue NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        o.order_date::DATE as date,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.subtotal) as total_revenue
    FROM "order" o
    JOIN order_item oi ON o.order_id = oi.order_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    AND (p_product_ids IS NULL OR oi.product_id = ANY(p_product_ids))
    GROUP BY o.order_date::DATE
    ORDER BY date;
END;
$$ LANGUAGE plpgsql;

-- Usage:
-- SELECT * FROM daily_revenue_report('2025-08-01', '2025-08-31', NULL);
-- SELECT * FROM daily_revenue_report('2025-08-01', '2025-08-31', ARRAY[1, 56, 138]);
