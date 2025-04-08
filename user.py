import uuid

class User:
    def __init__(self, user_id=None, user_name=""):
        self.user_id = user_id if user_id else str(uuid.uuid4())  # Generate UUID if not provided
        self.user_name = user_name

    def get_user_id(self):
        return self.user_id

    def get_user_name(self):
        return self.user_name
