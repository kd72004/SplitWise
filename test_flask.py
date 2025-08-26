#!/usr/bin/env python3

from user_controller import UserController
from group_controller import GroupController

# Test the controllers
user_controller = UserController()
group_controller = GroupController()

print("=== Testing User Registration ===")
result = user_controller.register("testuser", "test@example.com", "password123")
print(f"Registration result: {result}")

if result['success']:
    user_id = result['user_id']
    print(f"User ID: {user_id}")
    
    print("\n=== Testing User Login ===")
    login_result = user_controller.login("testuser", "password123")
    print(f"Login result: {login_result}")
    
    print("\n=== Testing Group Creation ===")
    group_result = group_controller.create_group("Test Group", user_id)
    print(f"Group creation result: {group_result}")
    
    print("\n=== Testing Get User Groups ===")
    groups = group_controller.get_user_groups(user_id)
    print(f"User groups: {[g.group_name for g in groups]}")
    
    print("\n=== Database Test Complete ===")
else:
    print("Registration failed, skipping other tests")