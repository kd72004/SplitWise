import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="splitwise_db",  
                user="postgres",    
                password="admin", 
                host="localhost",         
                port="5432"              
            )
            self.cur = self.conn.cursor()
            print("Database connection successful!")
        except Exception as e:
            print("Database connection failed:", e)

