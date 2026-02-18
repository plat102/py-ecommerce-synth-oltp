UPDATE "order" o
SET total_amount = totals.amount
FROM (
    SELECT order_id, COALESCE(SUM(subtotal), 0) as amount
    FROM order_item
    GROUP BY order_id
) totals
WHERE o.order_id = totals.order_id;
