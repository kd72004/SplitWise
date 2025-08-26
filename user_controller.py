from connection_sqlite import Database
from user import User
import logging
import sqlite3
import hashlib

logger = logging.getLogger(__name__)

class UserController:
    def add_user(self, user):
        if not user.get_user_name().strip():
            raise ValueError("Username cannot be empty")
            
        with Database() as db:
            try:
                query = "INSERT INTO users (user_id, user_name) VALUES (?, ?)"
                values = (user.get_user_id(), user.get_user_name())
                db.cur.execute(query, values)
                logger.info(f"User added successfully! ID: {user.get_user_id()}")
                return user.get_user_id()
            except sqlite3.IntegrityError as e:
                logger.error(f"User already exists: {e}")
                raise ValueError("User already exists")
            except sqlite3.Error as e:
                logger.error(f"Database error adding user: {e}")
                raise

    def get_user(self, user_id):
        if not user_id or not user_id.strip():
            return None
            
        with Database() as db:
            try:
                query = "SELECT user_id, user_name FROM users WHERE user_id = ?"
                db.cur.execute(query, (user_id,))
                result = db.cur.fetchone()
                return User(result[0], result[1]) if result else None
            except sqlite3.Error as e:
                logger.error(f"Database error fetching user: {e}")
                return None

    def get_all_users(self):
        with Database() as db:
            try:
                query = "SELECT user_id, user_name FROM users"
                db.cur.execute(query)
                results = db.cur.fetchall()
                return [User(row[0], row[1]) for row in results]
            except sqlite3.Error as e:
                logger.error(f"Database error fetching users: {e}")
                return []
    
    def register(self, username, email, password):
        """Register a new user with email and password"""
        if not username.strip() or not email.strip() or not password.strip():
            return {'success': False, 'message': 'All fields are required'}
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with Database() as db:
            try:
                # Check if username exists
                db.cur.execute("SELECT user_id FROM users WHERE user_name = ?", (username,))
                if db.cur.fetchone():
                    return {'success': False, 'message': 'Username already exists'}
                
                # Check if email exists
                db.cur.execute("SELECT user_id FROM users WHERE email = ?", (email,))
                if db.cur.fetchone():
                    return {'success': False, 'message': 'Email already exists'}
                
                # Insert new user
                db.cur.execute(
                    "INSERT INTO users (user_name, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                
                user_id = db.cur.lastrowid
                logger.info(f"User registered successfully: {username}")
                return {'success': True, 'user_id': user_id, 'message': 'Registration successful'}
                
            except sqlite3.Error as e:
                logger.error(f"Database error during registration: {e}")
                return {'success': False, 'message': 'Registration failed'}
    
    def login(self, username, password):
        """Login user with username and password"""
        if not username.strip() or not password.strip():
            return {'success': False, 'message': 'Username and password are required'}
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        with Database() as db:
            try:
                db.cur.execute(
                    "SELECT user_id, user_name FROM users WHERE user_name = ? AND password_hash = ?",
                    (username, password_hash)
                )
                result = db.cur.fetchone()
                
                if result:
                    logger.info(f"User logged in successfully: {username}")
                    return {'success': True, 'user_id': result[0], 'username': result[1]}
                else:
                    return {'success': False, 'message': 'Invalid username or password'}
                    
            except sqlite3.Error as e:
                logger.error(f"Database error during login: {e}")
                return {'success': False, 'message': 'Login failed'}