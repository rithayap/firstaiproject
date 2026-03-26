import mysql.connector
from mysql.connector import Error
from getpass import getpass


class EcommerceDB:
    def __init__(self):
        password = getpass("Enter MySQL password: ")

        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=password
        )

        self.cursor = self.conn.cursor()
        print(" Connected to MySQL successfully")

    # DATABASE SETUP 
    def setup_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
        self.cursor.execute("USE ecommerce")

        print("📦 Using database: ecommerce")

        # Products Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(50) NOT NULL UNIQUE,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock INT NOT NULL
        )
        """)

        # Customers Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE,
            city VARCHAR(50) DEFAULT 'ERNAKULAM'
        )
        """)

        # Orders Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)

        print(" Tables created successfully")

    # INSERT DATA 
    def insert_data(self):
        products = [
            ("T-Shirt", "Clothing", 499.00, 50),
            ("JEANS", "Clothing", 1200.00, 30),
            ("SmartPhone", "Electronics", 15000.00, 20),
            ("HeadPhone", "Electronics", 1500.00, 25),
            ("Shoes", "Footwear", 2500.00, 40)
        ]

        customers = [
            ("Parvathi", "paru@example.com", "ERNAKULAM"),
            ("Lakshmi", "laks@example.com", "BANGALORE"),
            ("Amit", "amit@example.com", "MUMBAI"),
            ("Vijay", "vij@example.com", "CHENNAI"),
            ("Veena", "vee@example.com", "ERNAKULAM")
        ]

        orders = [
            (1, 1, 2),
            (2, 3, 1),
            (3, 2, 3),
            (4, 5, 1),
            (5, 4, 2),
            (1, 3, 1),
            (2, 2, 2)
        ]

        self.cursor.executemany(
            "INSERT IGNORE INTO products(product_name, category, price, stock) VALUES (%s,%s,%s,%s)",
            products
        )

        self.cursor.executemany(
            "INSERT IGNORE INTO customers(customer_name, email, city) VALUES (%s,%s,%s)",
            customers
        )

        self.cursor.executemany(
            "INSERT INTO orders(customer_id, product_id, quantity) VALUES (%s,%s,%s)",
            orders
        )

        self.conn.commit()
        print(" Sample data inserted")

    # SHOW DATA 
    def show_data(self):
        print("\n PRODUCTS:")
        self.cursor.execute("SELECT * FROM products")
        for row in self.cursor.fetchall():
            print(row)

        print("\n CUSTOMERS:")
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            print(row)

        print("\n ORDERS:")
        self.cursor.execute("SELECT * FROM orders")
        for row in self.cursor.fetchall():
            print(row)

        print("\n ORDERS WITH DETAILS:")
        self.cursor.execute("""
            SELECT o.order_id, c.customer_name, p.product_name, o.quantity, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
        """)
        for row in self.cursor.fetchall():
            print(row)

    #  UPDATE & DELETE 
    def update_and_delete(self):
        # Update stock
        self.cursor.execute("""
            UPDATE products 
            SET stock = stock - 2 
            WHERE product_id = 1 AND stock >= 2
        """)
        self.conn.commit()
        print("\n Stock updated")

        # Delete orders with quantity = 1
        self.cursor.execute("DELETE FROM orders WHERE quantity = 1")
        self.conn.commit()
        print(" Orders with quantity = 1 deleted")

    #  GROUP BY 
    def group_data(self):
        print("\n TOTAL PRODUCTS SOLD:")
        self.cursor.execute("""
            SELECT p.product_name, SUM(o.quantity) AS total_sold
            FROM products p
            JOIN orders o ON p.product_id = o.product_id
            GROUP BY p.product_name
        """)

        for row in self.cursor.fetchall():
            print(row)

    #  CLOSE 
    def close(self):
        self.cursor.close()
        self.conn.close()
        print("\n Connection closed")


# object create
try:
    db = EcommerceDB()

    db.setup_database()
    db.insert_data()
    db.show_data()
    db.group_data()
    db.update_and_delete()

    db.close()

    print("\n PROJECT COMPLETED SUCCESSFULLY!")

except Exception as e:
    print(" Error:", e)