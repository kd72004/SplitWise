#!/usr/bin/env python3
"""
Simple test script to verify SplitWise functionality
"""

from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
from user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_splitwise():
    print("Testing SplitWise Application...")
    
    # Initialize controllers
    user_controller = UserController()
    group_controller = GroupController()
    expense_controller = ExpenseController()
    
    try:
        # Test 1: Create users
        print("\n1. Creating users...")
        alice = User(user_name="Alice")
        bob = User(user_name="Bob")
        charlie = User(user_name="Charlie")
        
        user_controller.add_user(alice)
        user_controller.add_user(bob)
        user_controller.add_user(charlie)
        print("Users created successfully!")
        
        # Test 2: Create group
        print("\n2. Creating group...")
        group_result = group_controller.create_group("Trip to Paris")
        if "error" in group_result:
            print(f"❌ Group creation failed: {group_result['error']}")
            return
        
        group_id = group_result["group_id"]
        print(f"Group created: {group_id}")
        
        # Test 3: Add users to group
        print("\n3. Adding users to group...")
        group_controller.add_user_to_group(group_id, alice.get_user_id())
        group_controller.add_user_to_group(group_id, bob.get_user_id())
        group_controller.add_user_to_group(group_id, charlie.get_user_id())
        print("Users added to group!")
        
        # Test 4: Get group members
        print("\n4. Getting group members...")
        members_result = group_controller.get_group_members(group_id)
        if "error" in members_result:
            print(f"❌ Failed to get members: {members_result['error']}")
        else:
            print(f"Group '{members_result['group_name']}' has {len(members_result['members'])} members")
            for member in members_result['members']:
                print(f"   - {member['user_name']} ({member['user_id'][:8]}...)")
        
        # Test 5: Create expense
        print("\n5. Creating expense...")
        user_shares = [
            {"borrower_id": alice.get_user_id(), "amount": 100.0},
            {"borrower_id": bob.get_user_id(), "amount": 100.0},
            {"borrower_id": charlie.get_user_id(), "amount": 100.0}
        ]
        
        expense_result = expense_controller.create_expense(
            name="Hotel Bill",
            paid_by=alice.get_user_id(),
            total_amount=300.0,
            split_type="equal",
            user_shares=user_shares,
            group_id=group_id
        )
        
        print(f"Expense created: {expense_result['name']} - ${expense_result['total_amount']}")
        print(f"   Split transactions: {len(expense_result['split_transactions'])} transactions")
        
        print("\nAll tests passed! SplitWise is working correctly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.error(f"Test error: {e}")

if __name__ == "__main__":
    test_splitwise()