"""
DDL Module
- SQL commands for init db structure
"""
TBL_BRAND = "brand"
TBL_CATEGORY = "category"
TBL_SELLER = "seller"
TBL_PROMOTION = "promotion"
TBL_PRODUCT = "product"
TBL_PROMOTION_PRODUCT = "promotion_product"
TBL_ORDER = "order"
TBL_ORDER_ITEM = "order_item"
ALL_TABLES = [
    TBL_BRAND,
    TBL_CATEGORY,
    TBL_SELLER,
    TBL_PROMOTION,
    TBL_PRODUCT,
    TBL_PROMOTION_PRODUCT
]

# ===================================================
# Independent master & reference
# ===================================================
_CREATE_BRAND = """
CREATE TABLE IF NOT EXISTS brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_CATEGORY = """
CREATE TABLE IF NOT EXISTS category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    -- Self-referencing FK: Level 1 (Null) -> Level 2 (Parent ID)
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT CHECK (level IN (1, 2)), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_SELLER = """
CREATE TABLE IF NOT EXISTS seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL,
    join_date DATE,
    seller_type VARCHAR(50), -- 'Official', 'Marketplace'
    rating DECIMAL(3,2),     -- 0.00 - 5.00
    country VARCHAR(50) DEFAULT 'Vietnam',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_PROMOTION = """
CREATE TABLE IF NOT EXISTS promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100),
    promotion_type VARCHAR(50),
    discount_type VARCHAR(20),   -- 'PERCENTAGE', 'FIXED_AMOUNT'
    discount_value DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ===================================================
# Dependent master
# ===================================================
_CREATE_PRODUCT = """
CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INT REFERENCES category(category_id),
    brand_id INT REFERENCES brand(brand_id),
    seller_id INT REFERENCES seller(seller_id),
    price DECIMAL(12,2),
    discount_price DECIMAL(12,2),
    stock_qty INT CHECK (stock_qty >= 0),
    rating DECIMAL(3,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ===================================================
# Associative data
# ===================================================
_CREATE_PROMOTION_PRODUCT = """
CREATE TABLE IF NOT EXISTS promotion_product (
    promo_product_id SERIAL PRIMARY KEY,
    promotion_id INT REFERENCES promotion(promotion_id),
    product_id INT REFERENCES product(product_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ===================================================
# Transactional data (header & detail)
# ===================================================
_CREATE_ORDER = """
CREATE TABLE IF NOT EXISTS "order" (
    order_id SERIAL PRIMARY KEY,
    order_date TIMESTAMP,
    seller_id INT REFERENCES seller(seller_id),
    status VARCHAR(20), -- 'PLACED', 'DELIVERED', 'CANCELLED',...
    total_amount DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CREATE_ORDER_ITEM = """
CREATE TABLE IF NOT EXISTS order_item (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES "order"(order_id),
    product_id INT REFERENCES product(product_id),
    quantity INT CHECK (quantity > 0),
    unit_price DECIMAL(12,2), -- Snapshot price
    subtotal DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ===================================================
# TODO: Index
# ===================================================
# _CREATE_INDEXES

DDL_STATEMENTS = [
    _CREATE_BRAND,
    _CREATE_CATEGORY,
    _CREATE_SELLER,
    _CREATE_PROMOTION,
    _CREATE_PRODUCT,
    _CREATE_PROMOTION_PRODUCT,
    _CREATE_ORDER,
    _CREATE_ORDER_ITEM
]

def get_ddl_statements():
    return DDL_STATEMENTS
