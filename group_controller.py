from connection import Database
from group import Group
import uuid

class GroupController:
    def __init__(self):
        self.db = Database()

    def create_group(self, group_name):
        try:
            group_id = str(uuid.uuid4())  
            query = "INSERT INTO groups (group_id, group_name) VALUES (%s, %s)"
            self.db.cur.execute(query, (group_id, group_name))
            self.db.conn.commit()
            return {"message": "Group created successfully!", "group_id": group_id}
        except Exception as e:
            return {"error": str(e)}

    def delete_group(self, group_id):
        try:
            query = "DELETE FROM groups WHERE group_id = %s"
            self.db.cur.execute(query, (group_id,))
            self.db.conn.commit()
            return {"message": "Group deleted successfully!"}
        except Exception as e:
            return {"error": str(e)}

    def add_user_to_group(self, group_id, user_id):
        try:
            query = "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)"
            self.db.cur.execute(query, (group_id, user_id))
            self.db.conn.commit()
            return {"message": "User added to group!"}
        except Exception as e:
            return {"error": str(e)}

    def get_user_groups(self, user_id):
        try:
            query = "SELECT g.group_id, g.group_name FROM groups g JOIN group_members gm ON g.group_id = gm.group_id WHERE gm.user_id = %s"
            self.db.cur.execute(query, (user_id,))
            results = self.db.cur.fetchall()
            return [{"group_id": row[0], "group_name": row[1]} for row in results]
        except Exception as e:  
            return {"error": str(e)}

    def get_group_members(self, group_id):
        try:
            query = """
            SELECT g.group_name, u.user_id, u.user_name 
            FROM groups g
            JOIN group_members gm ON g.group_id = gm.group_id
            JOIN users u ON gm.user_id = u.user_id
            WHERE g.group_id = %s
            """
            self.db.cur.execute(query, (group_id,))
            results = self.db.cur.fetchall()

            if not results:
                return {"error": "No members found or invalid group ID"}

            group_name = results[0][0]  
            members = [{"user_id": row[1], "user_name": row[2]} for row in results]

            return {"group_id": group_id, "group_name": group_name, "members": members}

        except Exception as e:
            return {"error": str(e)}
        
    def remove_user_from_group(self, group_id: str, user_id: str) -> dict:
        group = self.get_group(group_id)
        if not group:
            return {"error": f"Group with ID {group_id} does not exist."}
        user = self.user_controller.get_user(user_id)
        if not user:
            return {"error": f"User with ID {user_id} does not exist."}
        members = self.get_group_members(group_id)
        if user_id not in [member["user_id"] for member in members["members"]]:
            return {"error": f"User {user_id} is not in group {group_id}."}
        query = "DELETE FROM group_members WHERE group_id = %s AND user_id = %s"
        self.db.execute(query, (group_id, user_id))
        
        return {"message": f"User {user_id} removed from group {group_id}."}

