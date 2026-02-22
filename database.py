import sqlite3
import logging
from contextlib import contextmanager

logging.basicConfig(filename="app_data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseManager:
    def __init__(self, db_name="bmi_data.db"):
        self.db_name = db_name
        self._create_tables()
        self._ensure_default_user()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def _create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    age INTEGER DEFAULT 0,
                    gender TEXT DEFAULT 'Not Specified',
                    target_weight REAL DEFAULT 0.0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER, 
                    date TEXT,
                    weight REAL,
                    height REAL,
                    bmi REAL,
                    category TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_user_date ON history(user_id, date)')
            conn.commit()

    def _ensure_default_user(self):
        if not self.get_users():
            self.add_user("Guest")

    def add_user(self, username, age=0, gender="Not Specified", target_weight=0.0):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, age, gender, target_weight) VALUES (?, ?, ?, ?)", 
                               (username, age, gender, target_weight))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_users(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users")
            return cursor.fetchall()

    def add_entry(self, user_id, weight, height, bmi, category):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO history (user_id, date, weight, height, bmi, category) VALUES (?, strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'), ?, ?, ?, ?)",
                    (user_id, weight, height, bmi, category)
                )
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Failed to add entry: {e}")
            return False

    def get_history(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, date, weight, height, bmi, category FROM history WHERE user_id = ? ORDER BY date ASC", (user_id,))
            return cursor.fetchall()

    def delete_entry(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (entry_id,))
            conn.commit()