-- Create partitioned tables
CREATE TABLE order_partitioned (
    order_id SERIAL,
    order_date TIMESTAMP NOT NULL,
    seller_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT order_part_pkey PRIMARY KEY (order_id, order_date),
    CONSTRAINT order_part_seller_fkey FOREIGN KEY (seller_id) REFERENCES seller(seller_id)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE order_2025_08 PARTITION OF order_partitioned
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE order_2025_09 PARTITION OF order_partitioned
    FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE order_2025_10 PARTITION OF order_partitioned
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

-- Same for order_item
CREATE TABLE order_item_partitioned (
    order_item_id BIGSERIAL,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT order_item_part_pkey PRIMARY KEY (order_item_id, order_date)
) PARTITION BY RANGE (order_date);

CREATE TABLE order_item_2025_08 PARTITION OF order_item_partitioned
    FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE order_item_2025_09 PARTITION OF order_item_partitioned
    FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE order_item_2025_10 PARTITION OF order_item_partitioned
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
