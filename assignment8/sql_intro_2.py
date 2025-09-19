#%%
import sqlite3
import pandas as pd
#%%
with sqlite3.connect('../db/lesson.db') as conn:
    conn.execute("PRAGMA foreign_key = 1")
#%%
sql_query = """
SELECT line_items.line_item_id, line_items.quantity, line_items.product_id, 
       products.product_name, products.price
FROM line_items
JOIN products ON line_items.product_id = products.product_id
"""
#%%
df = pd.read_sql_query(sql_query, conn)
#%%

print("Step 3 - First 5 lines of the DataFrame:")
print(df.head())
print()

# Step 4: Add a 'total' column (quantity * price)
df['total'] = df['quantity'] * df['price']

print("Step 4 - DataFrame with 'total' column:")
print(df.head())
print()

# Step 5: Group by product_id with aggregation
grouped_df = df.groupby('product_id').agg({
    'line_item_id': 'count',
    'total': 'sum',
    'product_name': 'first'
})

print("Step 5 - Grouped DataFrame:")
print(grouped_df.head())
print()

# Step 6: Sort by product_name
grouped_df = grouped_df.sort_values('product_name')

print("Step 6 - Sorted by product_name:")
print(grouped_df.head())
print()

# Step 7: Write to CSV file
grouped_df.to_csv('order_summary.csv')

print("Step 7 - DataFrame written to 'order_summary.csv'")
print("Final summary:")
print(grouped_df)

# Close the database connection
conn.close()