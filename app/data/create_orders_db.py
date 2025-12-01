import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        status TEXT,
        delivery_date TEXT
    )
""")

cursor.execute("""
    INSERT INTO orders (order_id, status, delivery_date) VALUES
    ("1001", "Out for delivery", "2025-11-30"),
    ("1002", "Processing", "2025-12-02"),
    ("1003", "Delivered", "2025-11-28")
""")

conn.commit()
conn.close()

print("orders.db created successfully.")
