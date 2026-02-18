-- Generate 2-4 order items per order with seller-product matching
WITH orders_with_item_count AS (
    SELECT
        order_id,
        seller_id,
        order_date,
        (floor(random() * 3) + 2)::int AS num_items -- 2-4
    FROM "order"
),
orders_expanded AS (
    SELECT
        order_id,
        seller_id,
        order_date,
        generate_series(1, num_items) as item_seq
    FROM orders_with_item_count
)
INSERT INTO order_item (order_id, product_id, order_date, quantity, unit_price, subtotal, created_at)
SELECT
    oe.order_id,
    p.product_id,
    oe.order_date,
    floor(random() * 9 + 1)::int as quantity,  -- 1-10
    COALESCE(p.discount_price, p.price) as unit_price,
    floor(random() * 9 + 1) * COALESCE(p.discount_price, p.price) as subtotal,
    now() as created_at
FROM orders_expanded oe
CROSS JOIN LATERAL (
    -- Select product from same seller
    SELECT
        product_id, price, discount_price
    FROM product
    WHERE oe.seller_id = oe.seller_id
        AND is_active = true
        AND stock_qty > 0
    ORDER BY  random()
    LIMIT 1
) p
