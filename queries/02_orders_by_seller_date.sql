-- Orders filtered by seller and date
SELECT
    order_id,
    order_date,
    seller_id,
    status,
    total_amount
FROM "order"
WHERE seller_id = 11
  AND order_date BETWEEN '2025-10-01' AND '2025-10-10'
ORDER BY order_date DESC;
