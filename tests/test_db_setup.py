import unittest
from src.db_setup import setup_database

class TestDBSetup(unittest.TestCase):
    def test_orders_table_and_data(self):
        conn = setup_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM orders")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 5)
        conn.close()

if __name__ == "__main__":
    unittest.main()