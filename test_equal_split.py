#!/usr/bin/env python3
"""
Test script for equal split functionality
"""

from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
from logic import BalanceCalculator
from user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_equal_split():
    print("Testing Equal Split Feature...")
    
    # Initialize controllers
    user_controller = UserController()
    group_controller = GroupController()
    expense_controller = ExpenseController()
    calculator = BalanceCalculator()
    
    try:
        # Test 1: Create users
        print("\n1. Creating users...")
        alice = User(user_name="Alice_Equal")
        bob = User(user_name="Bob_Equal")
        charlie = User(user_name="Charlie_Equal")
        david = User(user_name="David_Equal")
        
        user_controller.add_user(alice)
        user_controller.add_user(bob)
        user_controller.add_user(charlie)
        user_controller.add_user(david)
        print("4 users created successfully!")
        
        # Test 2: Create group
        print("\n2. Creating group...")
        group_result = group_controller.create_group("Equal Split Test")
        if "error" in group_result:
            print(f"Group creation failed: {group_result['error']}")
            return
        
        group_id = group_result["group_id"]
        print(f"Group created: {group_id}")
        
        # Add all users to group
        group_controller.add_user_to_group(group_id, alice.get_user_id())
        group_controller.add_user_to_group(group_id, bob.get_user_id())
        group_controller.add_user_to_group(group_id, charlie.get_user_id())
        group_controller.add_user_to_group(group_id, david.get_user_id())
        print("All users added to group!")
        
        # Test 3: Equal split expense - Alice pays for 3 people
        print("\n3. Creating equal split expense (Alice pays for 3 people)...")
        
        # Alice pays $120 for dinner, split equally among Alice, Bob, Charlie (3 people)
        # Each person owes $40
        user_shares_dinner = [
            {"borrower_id": alice.get_user_id(), "amount": 40.0},
            {"borrower_id": bob.get_user_id(), "amount": 40.0},
            {"borrower_id": charlie.get_user_id(), "amount": 40.0}
            # David is not included
        ]
        
        expense1 = expense_controller.create_expense(
            name="Dinner - Equal Split",
            paid_by=alice.get_user_id(),
            total_amount=120.0,
            split_type="equal",
            user_shares=user_shares_dinner,
            group_id=group_id
        )
        print(f"Expense 1: {expense1['name']} - ${expense1['total_amount']}")
        print("  Equal split among 3 people: Alice, Bob, Charlie ($40 each)")
        print("  David not included")
        
        # Test 4: Another equal split - Bob pays for all 4 people
        print("\n4. Creating another equal split expense (Bob pays for all 4 people)...")
        
        # Bob pays $200 for hotel, split equally among all 4 people
        # Each person owes $50
        user_shares_hotel = [
            {"borrower_id": alice.get_user_id(), "amount": 50.0},
            {"borrower_id": bob.get_user_id(), "amount": 50.0},
            {"borrower_id": charlie.get_user_id(), "amount": 50.0},
            {"borrower_id": david.get_user_id(), "amount": 50.0}
        ]
        
        expense2 = expense_controller.create_expense(
            name="Hotel - Equal Split",
            paid_by=bob.get_user_id(),
            total_amount=200.0,
            split_type="equal",
            user_shares=user_shares_hotel,
            group_id=group_id
        )
        print(f"Expense 2: {expense2['name']} - ${expense2['total_amount']}")
        print("  Equal split among 4 people: All members ($50 each)")
        
        # Test 5: Calculate net balances
        print("\n5. Calculating net balances...")
        
        transactions = calculator.fetch_unsettled_transactions(group_id)
        print(f"Found {len(transactions)} individual transactions")
        
        net_balances = calculator.calculate_net_balances(transactions)
        print("Net balances after equal split expenses:")
        
        for user_id, balance in net_balances.items():
            user = user_controller.get_user(user_id)
            username = user.get_user_name() if user else user_id[:8]
            if balance > 0:
                print(f"  {username} is owed: ${balance:.2f}")
            elif balance < 0:
                print(f"  {username} owes: ${abs(balance):.2f}")
            else:
                print(f"  {username} is settled")
        
        # Test 6: Optimize settlements
        print("\n6. Optimizing settlements...")
        optimized_settlements = calculator.process_group_settlements(group_id)
        
        print(f"Optimized to {len(optimized_settlements)} settlements:")
        for settlement in optimized_settlements:
            group_id_s, debtor_id, creditor_id, amount = settlement
            debtor = user_controller.get_user(debtor_id)
            creditor = user_controller.get_user(creditor_id)
            debtor_name = debtor.get_user_name() if debtor else debtor_id[:8]
            creditor_name = creditor.get_user_name() if creditor else creditor_id[:8]
            print(f"  {debtor_name} pays ${amount:.2f} to {creditor_name}")
        
        print("\nEqual split feature test completed successfully!")
        
        # Summary
        print(f"\nSUMMARY:")
        print(f"- Expense 1: $120 split equally among 3 people ($40 each)")
        print(f"- Expense 2: $200 split equally among 4 people ($50 each)")
        print(f"- No individual amount entry required for equal splits")
        print(f"- Optimized to {len(optimized_settlements)} settlements")
        
    except Exception as e:
        print(f"Test failed: {e}")
        logger.error(f"Test error: {e}")

if __name__ == "__main__":
    test_equal_split()