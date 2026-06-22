CREATE DATABASE auction_db;

USE auction_db;

CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100)
);

CREATE TABLE products(
id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100),
base_price DECIMAL(10,2)
);

CREATE TABLE bids(
id INT AUTO_INCREMENT PRIMARY KEY,
product_id INT,
bid_amount DECIMAL(10,2),
FOREIGN KEY(product_id) REFERENCES products(id)
);

INSERT INTO products(product_name,base_price)
VALUES
('Laptop',30000),
('Mobile Phone',15000),
('Smart Watch',5000);