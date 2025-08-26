#!/usr/bin/env python3
"""
Test script for custom expense feature with selective members and custom amounts
"""

from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
from logic import BalanceCalculator
from user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_custom_expense():
    print("Testing Custom Expense Feature...")
    
    # Initialize controllers
    user_controller = UserController()
    group_controller = GroupController()
    expense_controller = ExpenseController()
    calculator = BalanceCalculator()
    
    try:
        # Test 1: Create users
        print("\n1. Creating users...")
        alice = User(user_name="Alice_Custom")
        bob = User(user_name="Bob_Custom")
        charlie = User(user_name="Charlie_Custom")
        david = User(user_name="David_Custom")
        eve = User(user_name="Eve_Custom")
        
        user_controller.add_user(alice)
        user_controller.add_user(bob)
        user_controller.add_user(charlie)
        user_controller.add_user(david)
        user_controller.add_user(eve)
        print("5 users created successfully!")
        
        # Test 2: Create group with all 5 members
        print("\n2. Creating group with 5 members...")
        group_result = group_controller.create_group("Custom Expense Group")
        if "error" in group_result:
            print(f"Group creation failed: {group_result['error']}")
            return
        
        group_id = group_result["group_id"]
        print(f"Group created: {group_id}")
        
        # Add all 5 users to group
        group_controller.add_user_to_group(group_id, alice.get_user_id())
        group_controller.add_user_to_group(group_id, bob.get_user_id())
        group_controller.add_user_to_group(group_id, charlie.get_user_id())
        group_controller.add_user_to_group(group_id, david.get_user_id())
        group_controller.add_user_to_group(group_id, eve.get_user_id())
        print("All 5 users added to group!")
        
        # Test 3: Create custom expense - Alice pays, only 3 people involved
        print("\n3. Creating custom expense (Alice pays for 3 people)...")
        
        user_shares_dinner = [
            {"borrower_id": alice.get_user_id(), "amount": 60.0},
            {"borrower_id": bob.get_user_id(), "amount": 50.0},
            {"borrower_id": charlie.get_user_id(), "amount": 40.0}
        ]
        
        expense1 = expense_controller.create_expense(
            name="Dinner (3 people only)",
            paid_by=alice.get_user_id(),
            total_amount=150.0,
            split_type="unequal",
            user_shares=user_shares_dinner,
            group_id=group_id
        )
        print(f"Expense 1: {expense1['name']} - ${expense1['total_amount']}")
        print("  Participants: Alice ($60), Bob ($50), Charlie ($40)")
        
        # Test 4: Create another custom expense - Bob pays for different people
        print("\n4. Creating another custom expense (Bob pays for 2 people)...")
        
        user_shares_movie = [
            {"borrower_id": bob.get_user_id(), "amount": 40.0},
            {"borrower_id": david.get_user_id(), "amount": 40.0}
        ]
        
        expense2 = expense_controller.create_expense(
            name="Movie Tickets (2 people only)",
            paid_by=bob.get_user_id(),
            total_amount=80.0,
            split_type="unequal",
            user_shares=user_shares_movie,
            group_id=group_id
        )
        print(f"Expense 2: {expense2['name']} - ${expense2['total_amount']}")
        print("  Participants: Bob ($40), David ($40)")
        
        # Test 5: Calculate net balances
        print("\n5. Calculating net balances...")
        
        transactions = calculator.fetch_unsettled_transactions(group_id)
        print(f"Found {len(transactions)} individual transactions")
        
        net_balances = calculator.calculate_net_balances(transactions)
        print("Net balances after custom expenses:")
        
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
        
        print("\nCustom expense feature test completed successfully!")
        
        # Summary
        print(f"\nSUMMARY:")
        print(f"- Group has 5 members, but expenses involved different subsets")
        print(f"- Expense 1: 3 people - $150")
        print(f"- Expense 2: 2 people - $80")
        print(f"- Eve was not involved in any expenses")
        print(f"- Optimized to {len(optimized_settlements)} settlements")
        
    except Exception as e:
        print(f"Test failed: {e}")
        logger.error(f"Test error: {e}")

if __name__ == "__main__":
    test_custom_expense()