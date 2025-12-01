import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "data", "orders.db"
)
DB_PATH = os.path.normpath(DB_PATH)

def lookup_order(order_id: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT order_id, status, delivery_date FROM orders WHERE order_id = ?", (order_id,))
        row = cur.fetchone()
        conn.close()

        if row:
            return {
                "order_id": row[0],
                "status": row[1],
                "delivery_date": row[2],
            }
        else:
            return None

    except Exception as e:
        return {"error": str(e)}
