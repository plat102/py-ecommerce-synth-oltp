-- Revenue per Product per Month
SELECT
    DATE_TRUNC('month', oi.order_date) as month,
    p.product_id,
    p.product_name,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue
FROM order_item oi
JOIN product p ON oi.product_id = p.product_id
GROUP BY DATE_TRUNC('month', oi.order_date), p.product_id, p.product_name
ORDER BY month, total_revenue DESC;
