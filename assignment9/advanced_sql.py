#%%
import sqlite3

import pandas as pd
import sys
#%%

#Task 1 
def main():
    # Open the database connection
    conn = sqlite3.connect("../db/lesson.db",isolation_level='IMMEDIATE')  # Replace with your actual database file name
    cursor = conn.cursor()
    
    # SQL query to find total price of first 5 orders
    query = """
    SELECT 
        o.order_id,
        SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    
    try:
        
        cursor.execute(query)
        
        
        results = cursor.fetchall()
        
        
        print("Order ID | Total Price")
        print('\n')
        for row in results:
            order_id, total_price = row
            print(f"{order_id:8} | ${total_price:10.2f}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        
        conn.close()
 

if __name__ == "__main__":
    main()

#%%
import sqlite3

def get_order_totals(cursor):
    """Part 1: Find total price of first 5 orders"""
    query1 = """
    SELECT 
        o.order_id,
        SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    
    cursor.execute(query1)
    results = cursor.fetchall()
    
    print("PART 1: Total Price of First 5 Orders")
    print("=" * 40)
    print("Order ID | Total Price")
    print("-" * 25)
    for row in results:
        order_id, total_price = row
        print(f"{order_id:8} | ${total_price:.2f}")
    print()

def get_customer_averages(cursor):
    """Part 2: Find average price of orders for each customer"""
    query2 = """
    SELECT 
        c.customer_name,
        AVG(order_totals.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT 
            o.customer_id AS customer_id_b,
            SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id, o.customer_id
    ) AS order_totals ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id, c.customer_name
    ORDER BY c.customer_name;
    """
    
    cursor.execute(query2)
    results = cursor.fetchall()
    
    print("PART 2: Average Order Price by Customer")
    print('\n')
    print("Customer Name          --- Average Total Price")
    print('\n')
    for row in results:
        customer_name, avg_price = row
        if avg_price is not None:
            print(f"{customer_name:22} | ${avg_price:.2f}")
        else:
            print(f"{customer_name:22} | No orders")
    print()

def main():
    conn = sqlite3.connect("../db/lesson.db",isolation_level='IMMEDIATE')  # Replace with your actual database file name
    cursor = conn.cursor()
    
    try:
        get_order_totals(cursor)
        get_customer_averages(cursor)
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
# %%


DB_PATH = "../db/lesson.db"  


CUSTOMER_NAME = "Perez and Sons"
FIRST_NAME = "Miranda"
LAST_NAME = "Harris"
LINE_ITEM_QUANTITY = 10
LEAST_EXPENSIVE_LIMIT = 5


conn = sqlite3.connect(DB_PATH)

conn.row_factory = sqlite3.Row
cur = conn.cursor()


cur.execute("PRAGMA foreign_keys = 1")

try:

    cur.execute("SELECT customer_id FROM customers WHERE customer_name = ? LIMIT 1", (CUSTOMER_NAME,))
    r = cur.fetchone()
    if r is None:
        raise ValueError(f"Customer not found: {CUSTOMER_NAME}")
    customer_id = r["customer_id"]


    cur.execute("SELECT employee_id FROM employees WHERE first_name = ? LIMIT 1", (FIRST_NAME,))
    r = cur.fetchone()
    if r is None:
        raise ValueError(f"Employee not found: {FIRST_NAME}")
    employee_id = r["employee_id"]

    print(f"Found customer_id={customer_id}, employee_id={employee_id}")


    conn.execute("BEGIN TRANSACTION;")


    cur.execute(
        "INSERT INTO orders (customer_id, employee_id,date) VALUES (?, ?, DATE('now'))",
        (customer_id, employee_id)
    )

    order_id = cur.lastrowid
    print(f"Inserted order with order_id = {order_id}")


    cur.execute(
        "SELECT product_id FROM products ORDER BY price ASC LIMIT ?",
        (LEAST_EXPENSIVE_LIMIT,)
    )
    products = [row["product_id"] for row in cur.fetchall()]
    if not products:
        raise ValueError("No products found to insert line_items for.")

    print(f"Selected least expensive product_ids: {products}")

    insert_sql = "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)"
    for pid in products:
        cur.execute(insert_sql, (order_id, pid, LINE_ITEM_QUANTITY))
        print(f"  -> inserted line_item for product_id={pid} (quantity={LINE_ITEM_QUANTITY})")


    conn.commit()
    print("Transaction committed.")

except Exception as e:
    conn.rollback()
    print("Transaction rolled back due to error:", str(e), file=sys.stderr)
    raise
finally:
    cur.close()


cur = conn.cursor()
result_sql = """
SELECT li.line_item_id, li.order_id, li.product_id, li.quantity, p.product_name, p.price
FROM line_items li
JOIN products p ON li.product_id = p.product_id
WHERE li.order_id = ?
ORDER BY li.line_item_id;
"""
df = pd.read_sql_query(result_sql, conn, params=(order_id,))
print("Inserted line items for order_id =", order_id)
print(df)
print()


csv_path = f"order_{order_id}_line_items.csv"
df.to_csv(csv_path, index=False)
print(f"Wrote results to '{csv_path}'")


conn.close()

# %%

DB_PATH = Path("../db/lesson.db")   # adjust path if necessary
CSV_OUTPUT = "employees_with_more_than_5_orders.csv"


conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")


sql_query = """
SELECT e.employee_id,
       e.first_name,
       e.last_name,
       COUNT(o.order_id) AS order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;
"""


df = pd.read_sql_query(sql_query, conn)


if df.empty:
    print("No employees found with more than 5 orders.")
else:
    print("Employees with more than 5 orders:")
    # ensure order_count is integer
    df['order_count'] = df['order_count'].astype(int)
    print(df.to_string(index=False))
    print()

# Step: write to CSV (optional but requested in previous tasks)
df.to_csv(CSV_OUTPUT, index=False)
print(f"Wrote results to '{CSV_OUTPUT}'")

# Close connection
conn.close()
#%%
#%%

DB_PATH = "../db/lesson.db"   
CSV_OUTPUT = "employees_with_more_than_5_orders.csv"


conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")

sql_query = """
SELECT e.employee_id,
       e.first_name,
       e.last_name,
       COUNT(o.order_id) AS order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;
"""


df = pd.read_sql_query(sql_query, conn)


if df.empty:
    print("No employees found with more than 5 orders.")
else:
    print("Employees with more than 5 orders:")
    # ensure order_count is integer
    df['order_count'] = df['order_count'].astype(int)
    print(df.to_string(index=False))
    print()

# Step: write to CSV (optional but requested in previous tasks)
df.to_csv(CSV_OUTPUT, index=False)
print(f"Wrote results to '{CSV_OUTPUT}'")


conn.close()
#%%
