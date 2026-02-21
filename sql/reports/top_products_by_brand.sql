CREATE OR REPLACE FUNCTION top_products_by_brand(
    p_start_date DATE,
    p_end_date DATE,
    p_seller_ids INT[] DEFAULT NULL,
    p_top_n INT DEFAULT 5
)
RETURNS TABLE (
    brand_id INT,
    brand_name VARCHAR,
    product_id INT,
    product_name VARCHAR,
    total_quantity BIGINT,
    total_revenue NUMERIC,
    rank_in_brand INT
) AS $$
BEGIN
    RETURN QUERY
    WITH product_sales AS (
        SELECT
            p.brand_id AS ps_brand_id,
            b.brand_name AS ps_brand_name,
            p.product_id AS ps_product_id,
            p.product_name AS ps_product_name,
            SUM(oi.quantity) AS ps_total_quantity,
            SUM(oi.subtotal) AS ps_total_revenue,
            ROW_NUMBER() OVER (
                PARTITION BY p.brand_id
                ORDER BY SUM(oi.quantity) DESC
            ) AS ps_rank_in_brand
        FROM order_item oi
        JOIN product p ON oi.product_id = p.product_id
        JOIN brand b ON p.brand_id = b.brand_id
        JOIN "order" o ON oi.order_id = o.order_id
        WHERE o.order_date BETWEEN p_start_date AND p_end_date
        AND (p_seller_ids IS NULL OR p.seller_id = ANY(p_seller_ids))
        GROUP BY p.brand_id, b.brand_name, p.product_id, p.product_name
    )
    SELECT
        ps_brand_id,
        ps_brand_name,
        ps_product_id,
        ps_product_name,
        ps_total_quantity,
        ps_total_revenue,
        ps_rank_in_brand::INT
    FROM product_sales
    WHERE ps_rank_in_brand <= p_top_n
    ORDER BY ps_brand_id, ps_rank_in_brand;
END;
$$ LANGUAGE plpgsql;

-- Usage:
SELECT * FROM top_products_by_brand('2025-08-01', '2025-10-31', NULL, 5);
SELECT * FROM top_products_by_brand('2025-08-01', '2025-10-31', ARRAY[11,12,13], 10);

