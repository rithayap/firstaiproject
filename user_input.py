import mysql.connector
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
        print("✅ Connected to MySQL")

    # ---------------- SETUP ----------------
    def setup_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce")
        self.cursor.execute("USE ecommerce")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(50) UNIQUE,
            category VARCHAR(50),
            price DECIMAL(10,2),
            stock INT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(50),
            email VARCHAR(50) UNIQUE,
            city VARCHAR(50)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """)

        print("✅ Database & Tables Ready")

    # ---------------- ADD PRODUCT ----------------
    def add_product(self):
        name = input("Enter product name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))

        self.cursor.execute(
            "INSERT INTO products(product_name, category, price, stock) VALUES (%s,%s,%s,%s)",
            (name, category, price, stock)
        )
        self.conn.commit()
        print("✅ Product added successfully")

    # ---------------- ADD CUSTOMER ----------------
    def add_customer(self):
        name = input("Enter customer name: ")
        email = input("Enter email: ")
        city = input("Enter city: ")

        self.cursor.execute(
            "INSERT INTO customers(customer_name, email, city) VALUES (%s,%s,%s)",
            (name, email, city)
        )
        self.conn.commit()
        print("✅ Customer added successfully")

    # ---------------- PLACE ORDER ----------------
    def place_order(self):
        customer_id = int(input("Enter customer ID: "))
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity: "))

        # Check stock
        self.cursor.execute("SELECT stock FROM products WHERE product_id=%s", (product_id,))
        result = self.cursor.fetchone()

        if result and result[0] >= quantity:
            self.cursor.execute(
                "INSERT INTO orders(customer_id, product_id, quantity) VALUES (%s,%s,%s)",
                (customer_id, product_id, quantity)
            )

            self.cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE product_id=%s",
                (quantity, product_id)
            )

            self.conn.commit()
            print("✅ Order placed successfully")
        else:
            print("❌ Not enough stock")

    # ---------------- VIEW DATA ----------------
    def view_data(self):
        print("\n📦 PRODUCTS:")
        self.cursor.execute("SELECT * FROM products")
        for row in self.cursor.fetchall():
            print(row)

        print("\n👤 CUSTOMERS:")
        self.cursor.execute("SELECT * FROM customers")
        for row in self.cursor.fetchall():
            print(row)

        print("\n🛒 ORDERS:")
        self.cursor.execute("""
        SELECT o.order_id, c.customer_name, p.product_name, o.quantity
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        """)
        for row in self.cursor.fetchall():
            print(row)

    # ---------------- MENU ----------------
    def menu(self):
        while True:
            print("\n====== E-COMMERCE MENU ======")
            print("1. Add Product")
            print("2. Add Customer")
            print("3. Place Order")
            print("4. View Data")
            print("5. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.add_customer()
            elif choice == "3":
                self.place_order()
            elif choice == "4":
                self.view_data()
            elif choice == "5":
                print("👋 Exiting...")
                break
            else:
                print("❌ Invalid choice")

    # ---------------- CLOSE ----------------
    def close(self):
        self.cursor.close()
        self.conn.close()
        print("🔒 Connection closed")


# ---------------- MAIN ----------------
try:
    db = EcommerceDB()
    db.setup_database()
    db.menu()
    db.close()

except Exception as e:
    print("❌ Error:", e)