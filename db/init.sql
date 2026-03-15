-- Initial setup for AgentOS Database
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) REFERENCES products(sku),
    quantity INT DEFAULT 0,
    location VARCHAR(100)
);

-- Seed some initial data
INSERT INTO products (sku, name, category, price) VALUES 
('SHOE-BLK-RUN-10', 'Running Shoes Black', 'Footwear', 2999.00),
('SHRT-BLU-COT-M', 'Blue Cotton Shirt M', 'Apparel', 1200.00);

INSERT INTO inventory (sku, quantity, location) VALUES 
('SHOE-BLK-RUN-10', 50, 'Main Floor'),
('SHRT-BLU-COT-M', 30, 'Main Floor');