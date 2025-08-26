import uuid

class User:
    def __init__(self, user_id=None, user_name=""):
        self.user_id = user_id if user_id else uuid.uuid4().hex
        self.user_name = user_name.strip() if user_name else ""

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        return self.user_name
    
    def __str__(self):
        return f"User(id={self.user_id}, name={self.user_name})"
    
    def __repr__(self):
        return self.__str__()
