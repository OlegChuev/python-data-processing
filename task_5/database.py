# Import modules
import sqlite3
import random

from faker import Faker
from datetime import datetime, timedelta

# Function to create tables
def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS Product;''')
    cursor.execute('''DROP TABLE IF EXISTS Supplier;''')
    cursor.execute('''DROP TABLE IF EXISTS Inventory;''')
    cursor.execute('''DROP TABLE IF EXISTS TransactionType;''')
    cursor.execute('''DROP TABLE IF EXISTS TransactionData;''')


    # Create Product Table
    #
    # The Product table stores information about each product, including its name, price, and category.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            product_id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            category TEXT
        )
    ''')

    # Create Supplier Table
    #
    # The Supplier table stores information about the suppliers, such as their name, contact person, and email.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            supplier_id INTEGER PRIMARY KEY,
            name TEXT,
            contact_person TEXT,
            email TEXT
        )
    ''')

    # Create Inventory Table
    #
    # The Inventory table tracks the quantity of each product in stock and the last date it was stocked.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inventory (
            inventory_id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES Product(product_id),
            quantity INTEGER,
            last_stocked_date DATE
        )
    ''')

    # Create TransactionType Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TransactionType (
            transaction_type_id INTEGER PRIMARY KEY,
            type_name TEXT
        )
    ''')

    # Create TransactionData Table with transaction_type as integer foreign key
    #
    # The TransactionData table records transactions related to the inventory, including details about the product involved, the quantity, the type of transaction (purchase or sale), and the transaction date.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TransactionData (
            transaction_id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES Product(product_id),
            supplier_id INTEGER REFERENCES Supplier(supplier_id),
            quantity INTEGER,
            transaction_type_id INTEGER REFERENCES TransactionType(transaction_type_id),
            transaction_date DATE
        )
    ''')

    # Commit the changes
    conn.commit()


# Function to generate random data
def generate_random_data(conn, table_name, num_records):
    cursor = conn.cursor()
    fake = Faker()

    for _ in range(num_records):
        if table_name == 'Product':
            cursor.execute('''
                INSERT INTO Product (name, price, category) VALUES (?, ?, ?)
            ''', (fake.word(), round(random.uniform(1.0, 100.0), 2), fake.word()))

        elif table_name == 'Supplier':
            cursor.execute('''
                INSERT INTO Supplier (name, contact_person, email) VALUES (?, ?, ?)
            ''', (fake.company(), fake.name(), fake.email()))

        elif table_name == 'Inventory':
            cursor.execute('''
                INSERT INTO Inventory (product_id, quantity, last_stocked_date) VALUES (?, ?, ?)
            ''', (random.randint(1, num_records), random.randint(1, 100), fake.date_this_decade()))

        elif table_name == 'TransactionType':
            cursor.execute('''
                INSERT INTO TransactionType (type_name) VALUES (?)
            ''', (fake.word(),))

        elif table_name == 'TransactionData':
            cursor.execute('''
                INSERT INTO TransactionData (product_id, supplier_id, quantity, transaction_type_id, transaction_date) VALUES (?, ?, ?, ?, ?)
            ''', (
                random.randint(1, num_records),
                random.randint(1, num_records),
                random.randint(1, 50),
                random.randint(1, 2),  # Assuming 1 and 2 are the transaction_type_id for 'Purchase' and 'Sale'
                fake.date_this_year()
            ))

    conn.commit()


def execute_queries(conn):
    print("\nSimple SELECT Query: Retrieve all products with their names and prices.")
    query1 = "SELECT name, price FROM Product;"
    result1 = execute_query(conn, query1)
    print("\nQuery 1 Result:")
    print(result1)

    print("\nJOIN Query: Retrieve the product name, supplier name, and contact person for each product and its supplier.")
    query2 = """
        SELECT Product.name AS product_name, Supplier.name AS supplier_name, Supplier.contact_person
        FROM TransactionData
        JOIN Supplier ON TransactionData.supplier_id = Supplier.supplier_id
        JOIN Product ON TransactionData.product_id = Product.product_id
    """
    result2 = execute_query(conn, query2)
    print("\nQuery 2 Result:")
    print(result2)

    print("\nAggregated Query: Calculate the total quantity of each product in the inventory.")
    query3 = """
        SELECT Product.name, SUM(Inventory.quantity) AS total_quantity
        FROM Product
        JOIN Inventory ON Product.product_id = Inventory.product_id
        GROUP BY Product.product_id;
    """
    result3 = execute_query(conn, query3)
    print("\nQuery 3 Result:")
    print(result3)

    print("\nFiltering Query: Retrieve all transactions for sales (transaction_type = 'Sale') in the last year.")
    query4 = """
        SELECT *
        FROM TransactionData
        WHERE transaction_type_id = (SELECT transaction_type_id FROM TransactionType WHERE transaction_type_id = 1)
        AND transaction_date >= DATE('now', '-1 year');
    """
    result4 = execute_query(conn, query4)
    print("\nQuery 4 Result:")
    print(result4)

    print("\nNested Query: Find the product with the highest price.")
    query5 = """
        SELECT *
        FROM Product
        WHERE price = (SELECT MAX(price) FROM Product);
    """
    result5 = execute_query(conn, query5)
    print("\nQuery 5 Result:")
    print(result5)


# Function to execute a SQL query
def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


# Function to connect to SQLite database
def create_connection():
    try:
        connection = sqlite3.connect('inventory.db')
        print("Connected to SQLite")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None
