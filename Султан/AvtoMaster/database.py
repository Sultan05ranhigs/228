import sqlite3

class Database:
    def __init__(self, db_name="workshop.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    image TEXT,
                    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    part_id INTEGER,
                    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(part_id) REFERENCES parts(id)
                )
            """)

    def register_user(self, username, password, role):
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, password, role)
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, role FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return cursor.fetchone()

    def get_purchase_history(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT parts.name, parts.price, parts.image, purchases.purchase_date
            FROM purchases
            JOIN parts ON purchases.part_id = parts.id
            WHERE purchases.user_id = ?
            ORDER BY purchases.purchase_date DESC
        """, (user_id,))
        return cursor.fetchall()
