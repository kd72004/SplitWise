from connection_sqlite import Database
from group import Group
import uuid
import logging
import sqlite3

logger = logging.getLogger(__name__)

class GroupController:
    def create_group(self, group_name, user_id):
        if not group_name or not group_name.strip():
            return {"success": False, "message": "Group name cannot be empty"}
            
        with Database() as db:
            try:
                group_id = uuid.uuid4().hex
                query = "INSERT INTO groups (group_id, group_name) VALUES (?, ?)"
                db.cur.execute(query, (group_id, group_name.strip()))
                
                # Add creator as member
                db.cur.execute("INSERT INTO group_members (group_id, user_id) VALUES (?, ?)", (group_id, user_id))
                
                logger.info(f"Group created: {group_name}")
                return {"success": True, "message": "Group created successfully!", "group_id": group_id}
            except sqlite3.IntegrityError as e:
                logger.error(f"Group creation failed - duplicate: {e}")
                return {"success": False, "message": "Group name already exists"}
            except sqlite3.Error as e:
                logger.error(f"Database error creating group: {e}")
                return {"success": False, "message": "Failed to create group"}

    def delete_group(self, group_id):
        if not group_id or not group_id.strip():
            return {"error": "Group ID cannot be empty"}
            
        with Database() as db:
            try:
                query = "DELETE FROM groups WHERE group_id = ?"
                db.cur.execute(query, (group_id,))
                if db.cur.rowcount == 0:
                    return {"error": "Group not found"}
                logger.info(f"Group deleted: {group_id}")
                return {"message": "Group deleted successfully!"}
            except sqlite3.Error as e:
                logger.error(f"Database error deleting group: {e}")
                return {"error": "Failed to delete group"}

    def add_user_to_group(self, group_id, user_id):
        if not all([group_id, user_id]):
            return {"error": "Group ID and User ID are required"}
            
        with Database() as db:
            try:
                query = "INSERT INTO group_members (group_id, user_id) VALUES (?, ?)"
                db.cur.execute(query, (group_id, user_id))
                logger.info(f"User {user_id} added to group {group_id}")
                return {"message": "User added to group!"}
            except sqlite3.IntegrityError as e:
                logger.error(f"User already in group: {e}")
                return {"error": "User already in group or invalid IDs"}
            except sqlite3.Error as e:
                logger.error(f"Database error adding user to group: {e}")
                return {"error": "Failed to add user to group"}

    def get_user_groups(self, user_id):
        if not user_id:
            return []
            
        with Database() as db:
            try:
                query = "SELECT g.group_id, g.group_name FROM groups g JOIN group_members gm ON g.group_id = gm.group_id WHERE gm.user_id = ?"
                db.cur.execute(query, (user_id,))
                results = db.cur.fetchall()
                
                # Return list of objects for template compatibility
                class GroupObj:
                    def __init__(self, group_id, group_name):
                        self.group_id = group_id
                        self.group_name = group_name
                
                return [GroupObj(row[0], row[1]) for row in results]
            except sqlite3.Error as e:
                logger.error(f"Database error fetching user groups: {e}")
                return []

    def get_group_members(self, group_id):
        if not group_id or not group_id.strip():
            return {"error": "Group ID cannot be empty"}
            
        with Database() as db:
            try:
                query = """
                SELECT g.group_name, u.user_id, u.user_name 
                FROM groups g
                JOIN group_members gm ON g.group_id = gm.group_id
                JOIN users u ON gm.user_id = u.user_id
                WHERE g.group_id = ?
                """
                db.cur.execute(query, (group_id,))
                results = db.cur.fetchall()

                if not results:
                    return {"error": "No members found or invalid group ID"}

                group_name = results[0][0]
                members = [{"user_id": row[1], "user_name": row[2]} for row in results]
                return {"group_id": group_id, "group_name": group_name, "members": members}
            except sqlite3.Error as e:
                logger.error(f"Database error fetching group members: {e}")
                return {"error": "Failed to fetch group members"}
        
    def remove_user_from_group(self, group_id, user_id):
        if not all([group_id, user_id]):
            return {"error": "Group ID and User ID are required"}
            
        with Database() as db:
            try:
                check_query = "SELECT 1 FROM group_members WHERE group_id = ? AND user_id = ?"
                db.cur.execute(check_query, (group_id, user_id))
                if not db.cur.fetchone():
                    return {"error": "User is not in this group"}
                
                query = "DELETE FROM group_members WHERE group_id = ? AND user_id = ?"
                db.cur.execute(query, (group_id, user_id))
                logger.info(f"User {user_id} removed from group {group_id}")
                return {"message": f"User removed from group successfully"}
            except sqlite3.Error as e:
                logger.error(f"Database error removing user from group: {e}")
                return {"error": "Failed to remove user from group"}
    
    def get_group_info(self, group_id):
        """Get group information"""
        with Database() as db:
            try:
                db.cur.execute("SELECT group_id, group_name FROM groups WHERE group_id = ?", (group_id,))
                result = db.cur.fetchone()
                if result:
                    class GroupInfo:
                        def __init__(self, group_id, group_name):
                            self.group_id = group_id
                            self.group_name = group_name
                    return GroupInfo(result[0], result[1])
                return None
            except sqlite3.Error as e:
                logger.error(f"Error fetching group info: {e}")
                return None
    
    def get_group_members(self, group_id):
        """Get group members list"""
        with Database() as db:
            try:
                query = """
                SELECT u.user_id, u.user_name, u.email 
                FROM users u
                JOIN group_members gm ON u.user_id = gm.user_id
                WHERE gm.group_id = ?
                """
                db.cur.execute(query, (group_id,))
                results = db.cur.fetchall()
                
                class MemberObj:
                    def __init__(self, user_id, user_name, email):
                        self.user_id = user_id
                        self.user_name = user_name
                        self.email = email or 'N/A'
                
                return [MemberObj(row[0], row[1], row[2]) for row in results]
            except sqlite3.Error as e:
                logger.error(f"Error fetching group members: {e}")
                return []
    
    def add_member_by_username(self, group_id, username):
        """Add member to group by username"""
        with Database() as db:
            try:
                # Find user by username
                db.cur.execute("SELECT user_id FROM users WHERE user_name = ?", (username,))
                user_result = db.cur.fetchone()
                
                if not user_result:
                    return {'success': False, 'message': 'User not found'}
                
                user_id = user_result[0]
                
                # Check if already member
                db.cur.execute("SELECT 1 FROM group_members WHERE group_id = ? AND user_id = ?", (group_id, user_id))
                if db.cur.fetchone():
                    return {'success': False, 'message': 'User already in group'}
                
                # Add to group
                db.cur.execute("INSERT INTO group_members (group_id, user_id) VALUES (?, ?)", (group_id, user_id))
                return {'success': True, 'message': 'Member added successfully'}
                
            except sqlite3.Error as e:
                logger.error(f"Error adding member: {e}")
                return {'success': False, 'message': 'Failed to add member'}