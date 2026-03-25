USE ECOMERENCE;

CREATE TABLE IF NOT EXISTS PRODUCTS(
product_id INT auto_increment PRIMARY KEY,
PRODUCT_NAME VARCHAR(50) NOT NULL unique,
category VARCHAR(50) NOT NULL,
price DECIMAL(10,2) NOT NULL,
stock INT NOT NULL);


CREATE TABLE CUSTOMERS(
customer_id INT auto_increment PRIMARY KEY,
customer_name VARCHAR(50) NOT NULL,
email VARCHAR(50)  unique,
city VARCHAR(50) default "ERNAKULAM");

CREATE TABLE orders(
order_id INT auto_increment PRIMARY KEY,
customer_id INT,
product_id INT,
quantity INT NOT NULL,
order_date TIMESTAMP DEFAULT NOW(),
FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id),
FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id)
);


INSERT INTO PRODUCTS(PRODUCT_NAME,category,price,stock)
values
("T-Shirt","Clothing",499.00,50),
("JEANS","Clothing",1200.00,30),
("SmartPhone","Electronics",15000.00,20),
("HeadPhone","Electronics",1500.00,25),
("Shoes","Footwear",2500.00,40);


INSERT INTO CUSTOMERS(customer_name,email,city)
values
("Parvathi","paru@example.com","ERNAKULAM"),
("Lakshmi","laks@example.com","BANGLORE"),
("Amit","amit@example.com","MUMBAI"),
("Vijay","vij@example.com","CHENNAI"),
("Veena","vee@example.com","DELHI");

INSERT INTO  orders (customer_id, product_id,quantity)
VALUES
(1,1,2),
(2,3,1),
(3,2,3),
(4,5,1),
(5,4,2),
(1,3,1),
(2,2,2);


SELECT * FROM PRODUCTS;
SELECT * FROM  CUSTOMERS;
SELECT * FROM  orders;

SELECT * FROM CUSTOMERS WHERE CITY="CHENNAI";

SELECT * FROM PRODUCTS WHERE PRICE>1000;

SELECT o.order_id,c.customer_name,p.product_name,o.quantity,o.order_date
FROM orders o
JOIN customers c ON O.customer_id=c.customer_id
JOIN products p ON O.product_id=p.product_id;

SELECT distinct c.customer_name, p.category
FROM orders o
JOIN customers c ON O.customer_id=c.customer_id
JOIN products p ON O.product_id=p.product_id
WHERE p.category="Electronics";

update products
SET stock=stock-2
where product_id=1;

SELECT * FROM PRODUCTS WHERE product_id=1;

Select c.customer_name,COUNT(O.ORDER_ID) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id =o.customer_id
GROUP BY c.customer_name;

Select p.product_name,sum(O.quantity) AS total_sold
FROM PRODUCTS p
JOIN orders o ON p.product_id =o.product_id
GROUP BY p.product_name;

SELECT 
    o.order_id,
    c.customer_name,
    p.product_name,
    o.quantity,
    CASE
        WHEN o.quantity >= 3 THEN 'DISCOUNT APPLIED'
        ELSE 'NO DISCOUNT'
    END AS OFFER
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id;













