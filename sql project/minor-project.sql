-- 🏪 Step 1: Create and select the database
DROP DATABASE IF EXISTS retail_inventory;
CREATE DATABASE retail_inventory;
USE retail_inventory;

-- 👥 Step 2: Create tables

-- Suppliers table
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(100),
    contact_no VARCHAR(15)
);

-- Products table
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    phone VARCHAR(15)
);

-- Sales table
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    sale_date DATE DEFAULT (CURRENT_DATE),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Sale items table
CREATE TABLE sale_items (
    sale_item_id INT PRIMARY KEY AUTO_INCREMENT,
    sale_id INT,
    product_id INT,
    quantity_sold INT,
    price_each DECIMAL(10,2),
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 📦 Step 3: Insert sample data

-- Suppliers
INSERT INTO suppliers (supplier_name, contact_no) VALUES
('ABC Traders', '9876543210'),
('Global Wholesales', '9998887777');

-- Products
INSERT INTO products (product_name, price, quantity, supplier_id) VALUES
('Soap', 40.00, 100, 1),
('Shampoo', 120.00, 80, 2),
('Rice Bag 10kg', 550.00, 50, 1);

-- Customers
INSERT INTO customers (customer_name, phone) VALUES
('Atul Mehta', '9998887776'),
('Neha Sharma', '9887766554');

-- 🧾 Step 4: Record a sale

INSERT INTO sales (customer_id, total_amount)
VALUES (1, 200.00);

-- Record sold items
INSERT INTO sale_items (sale_id, product_id, quantity_sold, price_each)
VALUES 
(1, 1, 2, 40.00),
(1, 2, 1, 120.00);

-- Update stock after sale
UPDATE products SET quantity = quantity - 2 WHERE product_id = 1;
UPDATE products SET quantity = quantity - 1 WHERE product_id = 2;

-- 📊 Step 5: Display reports

-- Show all products
SELECT * FROM products;

-- Show all customers
SELECT * FROM customers;

-- Show all sales
SELECT * FROM sales;

-- Show detailed sales report (joined data)
SELECT 
    s.sale_id,
    c.customer_name,
    p.product_name,
    si.quantity_sold,
    si.price_each,
    s.sale_date
FROM sale_items si
JOIN sales s ON si.sale_id = s.sale_id
JOIN customers c ON s.customer_id = c.customer_id
JOIN products p ON si.product_id = p.product_id;

-- Show low stock products
SELECT product_name, quantity 
FROM products 
WHERE quantity < 20;

