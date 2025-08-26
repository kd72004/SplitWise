import uuid

class Group:
    def __init__(self, group_id=None, group_name=""):
        self.group_id = group_id if group_id else uuid.uuid4().hex
        self.group_name = group_name.strip() if group_name else ""

    def get_group_id(self):
        return self.group_id

    def get_group_name(self):
        return self.group_name
    
    def __str__(self):
        return f"Group(id={self.group_id}, name={self.group_name})"
    
    def __repr__(self):
        return self.__str__()
