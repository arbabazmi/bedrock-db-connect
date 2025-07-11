import sqlite3

def setup_database():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            amount REAL,
            order_date TEXT
        )
    ''')
    orders = [
        (1, 'Alice', 1200, '2025-06-30'),
        (2, 'Bob', 800, '2025-07-01'),
        (3, 'Charlie', 2200, '2025-07-02'),
        (4, 'Alice', 500, '2025-07-03'),
        (5, 'Eve', 1500, '2025-07-04'),
    ]
    c.executemany('INSERT INTO orders VALUES (?, ?, ?, ?)', orders)
    conn.commit()
    return conn