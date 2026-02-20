-- List products with highest quantity sold
SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue
FROM order_item oi
JOIN product p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity DESC
LIMIT 20;
