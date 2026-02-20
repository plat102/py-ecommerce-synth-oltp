-- Products Sold per Seller
SELECT
    s.seller_id,
    s.seller_name,
    COUNT(DISTINCT oi.product_id) as unique_products,
    SUM(oi.quantity) as total_quantity,
    SUM(oi.subtotal) as total_revenue
FROM seller s
JOIN product p ON s.seller_id = p.seller_id
JOIN order_item oi ON p.product_id = oi.product_id
GROUP BY s.seller_id, s.seller_name
ORDER BY total_revenue DESC;
