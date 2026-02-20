-- Total revenue per month
SELECT
    TO_CHAR(order_date, 'YYYY-MM') as month,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_revenue
FROM "order"
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;
