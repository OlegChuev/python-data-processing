# Import modules
import database

# Establish connection
conn = database.create_connection()

if conn is not None:
    print("Creating tables..")
    database.create_tables(conn)

    print("Filling tables with data..")
    database.generate_random_data(conn, 'Product', 15)
    database.generate_random_data(conn, 'Supplier', 15)
    database.generate_random_data(conn, 'Inventory', 15)
    database.generate_random_data(conn, 'TransactionType', 2)
    database.generate_random_data(conn, 'TransactionData', 15)

    database.execute_queries(conn)

    print("Closing connection closed")
    conn.close()
    print("Connection closed")
