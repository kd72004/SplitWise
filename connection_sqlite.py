import sqlite3
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()
    
    def connect(self):
        try:
            db_path = os.getenv('DB_PATH', 'splitwise.db')
            self.conn = sqlite3.connect(db_path)
            self.cur = self.conn.cursor()
            self.setup_tables()
            logger.info("Database connection successful")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def setup_tables(self):
        """Create tables if they don't exist"""
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS group_members (
                group_id TEXT,
                user_id INTEGER,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (group_id, user_id),
                FOREIGN KEY (group_id) REFERENCES groups(group_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''',
            '''CREATE TABLE IF NOT EXISTS expense (
                expense_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                paid_by INTEGER,
                total_amount REAL NOT NULL,
                split_type TEXT NOT NULL CHECK (split_type IN ('equal', 'unequal', 'percentage')),
                group_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paid_by) REFERENCES users(user_id),
                FOREIGN KEY (group_id) REFERENCES groups(group_id)
            )''',
            '''CREATE TABLE IF NOT EXISTS expense_share (
                expense_id TEXT,
                borrower_id INTEGER,
                paid_by_id INTEGER,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (expense_id, borrower_id),
                FOREIGN KEY (expense_id) REFERENCES expense(expense_id),
                FOREIGN KEY (borrower_id) REFERENCES users(user_id),
                FOREIGN KEY (paid_by_id) REFERENCES users(user_id)
            )''',
            '''CREATE TABLE IF NOT EXISTS balance_sheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT,
                borrower_id INTEGER,
                receiver_id INTEGER,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(group_id),
                FOREIGN KEY (borrower_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )'''
        ]
        
        for table in tables:
            self.cur.execute(table)
        
        # Add migration for existing users table
        self.migrate_users_table()
        self.conn.commit()
    
    def migrate_users_table(self):
        """Add email and password_hash columns if they don't exist"""
        try:
            # Check if email column exists
            self.cur.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in self.cur.fetchall()]
            
            if 'email' not in columns:
                self.cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
                logger.info("Added email column to users table")
            
            if 'password_hash' not in columns:
                self.cur.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
                logger.info("Added password_hash column to users table")
                
        except sqlite3.Error as e:
            logger.error(f"Migration error: {e}")
            # Continue anyway - table might already be correct
    
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.close()