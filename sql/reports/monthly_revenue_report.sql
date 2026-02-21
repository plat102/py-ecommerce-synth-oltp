CREATE OR REPLACE FUNCTION monthly_revenue_report(
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    month DATE,
    total_orders BIGINT,
    total_quantity BIGINT,
    total_revenue NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        DATE_TRUNC('month', o.order_date)::DATE as month,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.subtotal) as total_revenue
    FROM "order" o
    JOIN order_item oi ON o.order_id = oi.order_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    GROUP BY DATE_TRUNC('month', o.order_date)
    ORDER BY month;
END;
$$ LANGUAGE plpgsql;

-- Usage:
-- SELECT * FROM monthly_revenue_report('2025-08-01', '2025-10-31');
