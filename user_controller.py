from connection import Database
from user import User

class UserController:
    def __init__(self):
        self.db = Database() 
        
    def add_user(self, user):
        try:
            query = "INSERT INTO users (user_id, user_name) VALUES (%s, %s)"
            values = (user.get_user_id(), user.get_user_name())  # Use User object's ID
            self.db.cur.execute(query, values)
            self.db.conn.commit()
            print(f"User added successfully! ID: {user.get_user_id()}")
            return user.get_user_id()
        except Exception as e:
            print("Error adding user:", e)

    def get_user(self, user_id):
        try:
            query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
            self.db.cur.execute(query, (user_id,))
            result = self.db.cur.fetchone()
            if result:
                return User(result[0], result[1]) 
            else:
                return None
        except Exception as e:
            print("Error fetching user:", e)

    def get_all_users(self):
        try:
            query = "SELECT user_id, user_name FROM users"
            self.db.cur.execute(query)
            results = self.db.cur.fetchall()
            return [User(row[0], row[1]) for row in results]  
        except Exception as e:
            print("Error fetching all users:", e)
