-- Orders by Seller in October
SELECT
    s.seller_id,
    s.seller_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue
FROM seller s
JOIN "order" o ON s.seller_id = o.seller_id
WHERE o.order_date >= '2025-10-01'
  AND o.order_date < '2025-11-01'
GROUP BY s.seller_id, s.seller_name
ORDER BY total_revenue DESC;