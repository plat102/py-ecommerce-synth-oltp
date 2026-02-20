-- Find order with highest total_amount
SELECT
    order_id,
    order_date,
    seller_id,
    status,
    total_amount
FROM "order"
ORDER BY total_amount DESC
LIMIT 1;