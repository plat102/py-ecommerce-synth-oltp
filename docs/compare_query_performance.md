```
Write query for listing requirement and snapshot the result (run time and execution plan)
    1. Total revenue per month
    2. Orders filtered by seller and date
    3. Filter data in `order_item` by product_id
    4. Find order with highest total_amount
    5. List products with highest quantity sold
    6. Orders by Seller in October
    7. Revenue per Product per Month
    8. Products Sold per Seller
- Create monthly partitions for the two tables above and create an index on the `product_id` column of `order_item` table.
- Write query for above requirements again and snapshot the result (run time and execution plan); then compare
```

![img.png](images/data_gen.png)


#### 1. Total revenue per month
![query1_plan.png](images/q1_plan.png)
![query1_analyze.png](images/q1_analyze.png)
After:

#### 2. Orders filtered by seller and date
![q2_plan.png](images/q2_plan.png)
![q2_analyze.png](images/q2_analyze.png)

#### 3. Filter data in `order_item` by product_id
![q3_plan.png](images/q3_plan.png)
![q3_analysis.png](images/q3_analysis.png)

#### 4. Find order with highest total_amount
![q4_plan.png](images/q4_plan.png)
![q4_analysis.png](images/q4_analysis.png)

#### 5. List products with highest quantity sold
![explain_plan_1771604702752.svg](images/q5_explain_plan_1771604702752.svg)
![q5_plan.png](images/q5_plan.png)
![q5_analysis.png](images/q5_analysis.png)
#### 6. Orders by Seller in October
![q6_explain_plan_1771605249782.svg](images/q6_explain_plan_1771605249782.svg)
![q6_plan.png](images/q6_plan.png)
![q6_analyze.png](images/q6_analyze.png)

#### 7. Revenue per Product per Month
![q7_explain_plan_1771605498713.svg](images/q7_explain_plan_1771605498713.svg)
![q7_plan.png](images/q7_plan.png)
![q7_analysis.png](images/q7_analysis.png)

#### 8. Products Sold per Seller
![q8_explain_plan_1771605676335.svg](images/q8_explain_plan_1771605676335.svg)
![q8_plan.png](images/q8_plan.png)
![q8_analysis.png](images/q8_analysis.png)

### Create partition

Run script: [create_partitions.sql](../sql/create_partitions.sql)
```shell
[2026-02-21 15:40:28] completed in 5 ms
[2026-02-21 15:40:28] ecommerce_oltp.public> CREATE TABLE order_2025_10 PARTITION OF order_partitioned
                                                 FOR VALUES FROM ('2025-10-01') TO ('2025-11-01')
[2026-02-21 15:40:28] completed in 4 ms
[2026-02-21 15:40:28] ecommerce_oltp.public> CREATE TABLE order_item_partitioned (
                                                 order_item_id BIGSERIAL,
                                                 order_id INT NOT NULL,
                                                 product_id INT NOT NULL,
                                                 order_date TIMESTAMP NOT NULL,
                                                 quantity INT NOT NULL,
                                                 unit_price NUMERIC(10,2) NOT NULL,
                                                 subtotal NUMERIC(12,2) NOT NULL,
                                                 created_at TIMESTAMP DEFAULT NOW(),
                                                 CONSTRAINT order_item_part_pkey PRIMARY KEY (order_item_id, order_date)
                                             ) PARTITION BY RANGE (order_date)
[2026-02-21 15:40:28] completed in 5 ms
[2026-02-21 15:40:28] ecommerce_oltp.public> CREATE TABLE order_item_2025_08 PARTITION OF order_item_partitioned
                                                 FOR VALUES FROM ('2025-08-01') TO ('2025-09-01')
[2026-02-21 15:40:28] completed in 5 ms
[2026-02-21 15:40:28] ecommerce_oltp.public> CREATE TABLE order_item_2025_09 PARTITION OF order_item_partitioned
                                                 FOR VALUES FROM ('2025-09-01') TO ('2025-10-01')
```

#### Migrate from generated data
Script: [migrate_to_partitions.sql](../sql/migrate_to_partitions.sql)

```shell
[2026-02-21 15:46:44] ecommerce_oltp.public> INSERT INTO order_partitioned (order_id, order_date, seller_id, status, total_amount, created_at)
                                             SELECT order_id, order_date, seller_id, status, total_amount, created_at
                                             FROM "order"
[2026-02-21 15:46:59] 2,700,000 rows affected in 15 s 377 ms
[2026-02-21 15:46:59] ecommerce_oltp.public> INSERT INTO order_item_partitioned (order_item_id, order_id, product_id, order_date, quantity, unit_price, subtotal, created_at)
                                             SELECT order_item_id, order_id, product_id, order_date, quantity, unit_price, subtotal, created_at
                                             FROM order_item
[2026-02-21 15:47:11] 8,099,837 rows affected in 11 s 528 ms
```
### Create indexes