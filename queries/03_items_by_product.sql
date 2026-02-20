-- Filter data in order_item by product_id
SELECT
    oi.order_item_id,
    oi.order_id,
    oi.order_date,
    oi.quantity,
    oi.unit_price,
    oi.subtotal,
    oi.product_id
FROM order_item oi
WHERE oi.product_id = 56
ORDER BY oi.order_date DESC;
