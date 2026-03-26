import mysql.connector
from mysql.connector import Error
from getpass import getpass


def connect_db():
    password = getpass("Enter your password: ")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=password,
        port=3306
    )
    return conn


def setup_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
    cursor.execute("USE ecommerce")

    print("Using database: ecommerce")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(50) NOT NULL UNIQUE,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock INT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE,
        city VARCHAR(50) DEFAULT 'ERNAKULAM'
    )
    """)

    cursor.execute("""
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

    print("Tables created successfully!")


def insert_data(cursor, conn):
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

    cursor.executemany(
        "INSERT IGNORE INTO products(product_name, category, price, stock) VALUES (%s,%s,%s,%s)",
        products
    )

    cursor.executemany(
        "INSERT IGNORE INTO customers(customer_name, email, city) VALUES (%s,%s,%s)",
        customers
    )

    cursor.executemany(
        "INSERT INTO orders(customer_id, product_id, quantity) VALUES (%s,%s,%s)",
        orders
    )

    conn.commit()


def show_products(cursor, conn):
    print("\nProducts:")
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(row)

    print("\nCustomers:")
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        print(row)

    print("\nOrders:")
    cursor.execute("SELECT * FROM orders")
    for row in cursor.fetchall():
        print(row)

    print("\nOrders with details:")
    cursor.execute("""
        SELECT o.order_id, c.customer_name, p.product_name, o.quantity, o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
    """)
    for row in cursor.fetchall():
        print(row)

    cursor.execute("UPDATE products SET stock = stock - 2 WHERE product_id = 1 AND stock >= 2")
    conn.commit()
    print("\nStock updated for product ID 1")

    cursor.execute("DELETE FROM orders WHERE quantity = 1")
    conn.commit()
    print("\nOrders with quantity = 1 deleted")


def group_data(cursor):
    print("\nTotal Products Sold:")

    cursor.execute("""
        SELECT p.product_name, SUM(o.quantity) AS total_sold
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.product_name
    """)

    for row in cursor.fetchall():
        print(row)


# MAIN
try:
    conn = connect_db()
    cursor = conn.cursor()

    setup_database(cursor)
    insert_data(cursor, conn)
    group_data(cursor)

    print("\nProduct List:")
    show_products(cursor, conn)

    cursor.close()
    conn.close()

    print("\nProject Completed Successfully!")

except Exception as e:
    print("Error:", e)