
#%%
import sqlite3 
import pandas as pd
#%%
try:
    with sqlite3.connect("../db/magazines.db") as conn: 
        print("Database created and connected")
except sqlite3.Error as e: 
    print(f"An SQLite error occurred: {e}")

# %%

cursor = conn.cursor()
conn.execute("PRAGMA foreign_keys =1")

cursor.execute("""
CREATE TABLE IF NOT EXISTS publishers (
    publisher_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS magazines (
    magazine_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    publisher_id INTEGER NOT NULL,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE CASCADE
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    subscriber_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    subscriber_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id) ON DELETE CASCADE,
    FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id) ON DELETE CASCADE,
    UNIQUE (subscriber_id, magazine_id)
);
""")

conn.commit()

print("Tables created successfully.")
# %%
def add_publisher(conn, name):
    try: 
        conn.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' already exists.")

def add_magazine(conn, name, publisher_name): 
    try: 
        current = conn.execute("SELECT publisher_id FROM publishers WHERE name=?", (publisher_name,))
        row = current.fetchone() 
        if not row: 
            print(f"Publisher '{publisher_name}' does not exist. Cannot add magazine '{name}'.")
            return
        publisher_id = row[0]

        conn.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' already exists.")

def add_subscriber(conn, name, address): 
    try: 
        conn.execute("INSERT INTO subscribers (name, address) VALUES (?,?)", (name, address))
        conn.commit()
    except sqlite3.IntegrityError: 
        print(f"Subscriber '{name},{address}' already exists.")

def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date): 
    try: 
        current = conn.execute("SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, subscriber_address))
        sub = current.fetchone() 
        if not sub: 
            print(f"Subscriber '{subscriber_name}, {subscriber_address}' not found.")
            return 
        subscriber_id = sub[0]

        current = conn.execute("SELECT magazine_id FROM magazines WHERE name = ?", (magazine_name,))
        magazine = current.fetchone() 
        if not magazine: 
            print(f"Magazine '{magazine_name}' not found.")
            return 
        magazine_id = magazine[0]

        conn.execute(""" 
                 INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) 
                 VALUES (?, ?, ?)
                 """, (subscriber_id, magazine_id, expiration_date))
        conn.commit() 
    except sqlite3.IntegrityError: 
        print(f"Subcription already exists for subscriber '{subscriber_name}' to magazine '{magazine_name}")

if __name__ == "__main__": 
    with sqlite3.connect("../db/magazines.db") as conn: 
        conn.execute("PRAGMA foreign_keys = 1")

        #Add publisher 

        add_publisher(conn, "TechWorld")
        add_publisher(conn, "HealthPlus")
        add_publisher(conn, "Daily News")

        #Add magazines 
        add_magazine(conn, "AI Monthly", "TechWorld")
        add_magazine(conn, "Wellness Weekly", "HealthPlus")
        add_magazine(conn, "Morning Times", "Daily News")

        #Add subsribers 
        add_subscriber(conn, "Alice Smith", "123 Main St")
        add_subscriber(conn, "Bob Johnson", "456 Oak Ave")
        add_subscriber(conn, "Charlie Brown", "789 Pine Rd")

        #Add subscriptions  
        add_subscription(conn, "Alice Smith", "123 Main St", "AI Monthly", "2025-12-31")
        add_subscription(conn, "Bob Johnson", "456 Oak Ave", "Wellness Weekly", "2025-10-15")
        add_subscription(conn, "Charlie Brown", "789 Pine Rd", "Morning Times", "2026-01-01")

print("Database populated successfully.")

#%% 

import sqlite3
import os

# Path to DB
db_path = os.path.join(os.path.dirname(__file__), "..", "db", "magazines.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

with sqlite3.connect(db_path) as conn:
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publishers (
        publisher_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magazines (
        magazine_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        publisher_id INTEGER NOT NULL,
        FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        subscriber_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        UNIQUE(name, address)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id INTEGER PRIMARY KEY,
        subscriber_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        expiration_date TEXT NOT NULL,
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id) ON DELETE CASCADE,
        FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id) ON DELETE CASCADE,
        UNIQUE(subscriber_id, magazine_id)
    );
    """)

    conn.commit()


# -------------------
# Helper functions
# -------------------
def add_publisher(conn, name):
    try:
        conn.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' already exists.")


def add_magazine(conn, name, publisher_name):
    try:
        # Look up publisher_id
        cur = conn.execute("SELECT publisher_id FROM publishers WHERE name = ?", (publisher_name,))
        row = cur.fetchone()
        if not row:
            print(f"Publisher '{publisher_name}' does not exist. Cannot add magazine '{name}'.")
            return
        publisher_id = row[0]

        conn.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' already exists.")


def add_subscriber(conn, name, address):
    try:
        conn.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Subscriber '{name}, {address}' already exists.")


def add_subscription(conn, subscriber_name, subscriber_address, magazine_name, expiration_date):
    try:
        # Look up subscriber_id
        cur = conn.execute("SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, subscriber_address))
        sub = cur.fetchone()
        if not sub:
            print(f"Subscriber '{subscriber_name}, {subscriber_address}' not found.")
            return
        subscriber_id = sub[0]

        # Look up magazine_id
        cur = conn.execute("SELECT magazine_id FROM magazines WHERE name = ?", (magazine_name,))
        mag = cur.fetchone()
        if not mag:
            print(f"Magazine '{magazine_name}' not found.")
            return
        magazine_id = mag[0]

        conn.execute("""
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
        """, (subscriber_id, magazine_id, expiration_date))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Subscription already exists for subscriber '{subscriber_name}' to magazine '{magazine_name}'.")


# -------------------
# Main
# -------------------
if __name__ == "__main__":
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = 1")

        # Add publishers
        add_publisher(conn, "TechWorld")
        add_publisher(conn, "HealthPlus")
        add_publisher(conn, "Daily News")

        # Add magazines
        add_magazine(conn, "AI Monthly", "TechWorld")
        add_magazine(conn, "Wellness Weekly", "HealthPlus")
        add_magazine(conn, "Morning Times", "Daily News")

        # Add subscribers
        add_subscriber(conn, "Alice Smith", "123 Main St")
        add_subscriber(conn, "Bob Johnson", "456 Oak Ave")
        add_subscriber(conn, "Charlie Brown", "789 Pine Rd")

        # Add subscriptions
        add_subscription(conn, "Alice Smith", "123 Main St", "AI Monthly", "2025-12-31")
        add_subscription(conn, "Bob Johnson", "456 Oak Ave", "Wellness Weekly", "2025-10-15")
        add_subscription(conn, "Charlie Brown", "789 Pine Rd", "Morning Times", "2026-01-01")

print("---------------------------------------------------")

current = conn.execute("SELECT * FROM subscribers;")
for row in current.fetchall():
    print("subsriber: ",row)
print("---------------------------------------------------")

current = conn.execute("SELECT * FROM magazines ORDER BY name;")
for row in current.fetchall():
    print("magazine: ",row)

print("---------------------------------------------------")
current = conn.execute("""
    SELECT m.magazine_id, m.name, p.name AS publisher
    FROM magazines m
    JOIN publishers p ON m.publisher_id = p.publisher_id
    WHERE p.name = 'TechWorld';
""")
for row in current.fetchall():
    print("TechWorld:", row)

print("\nDatabase populated and queries executed successfully.")

#%%