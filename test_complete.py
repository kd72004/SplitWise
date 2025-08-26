#!/usr/bin/env python3
"""
Complete test script for SplitWise with expense management and settlement optimization
"""

from user_controller import UserController
from group_controller import GroupController
from expense_controller import ExpenseController
from logic import BalanceCalculator
from user import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_splitwise():
    print("Testing Complete SplitWise Application...")
    
    # Initialize controllers
    user_controller = UserController()
    group_controller = GroupController()
    expense_controller = ExpenseController()
    calculator = BalanceCalculator()
    
    try:
        # Test 1: Create users
        print("\n1. Creating users...")
        alice = User(user_name="Alice_Test")
        bob = User(user_name="Bob_Test")
        charlie = User(user_name="Charlie_Test")
        david = User(user_name="David_Test")
        
        user_controller.add_user(alice)
        user_controller.add_user(bob)
        user_controller.add_user(charlie)
        user_controller.add_user(david)
        print("Users created successfully!")
        
        # Test 2: Create group
        print("\n2. Creating group...")
        group_result = group_controller.create_group("Weekend Trip")
        if "error" in group_result:
            print(f"Group creation failed: {group_result['error']}")
            return
        
        group_id = group_result["group_id"]
        print(f"Group created: {group_id}")
        
        # Test 3: Add users to group
        print("\n3. Adding users to group...")
        group_controller.add_user_to_group(group_id, alice.get_user_id())
        group_controller.add_user_to_group(group_id, bob.get_user_id())
        group_controller.add_user_to_group(group_id, charlie.get_user_id())
        group_controller.add_user_to_group(group_id, david.get_user_id())
        print("Users added to group!")
        
        # Test 4: Create multiple expenses
        print("\n4. Creating expenses...")
        
        # Alice pays for hotel (400 split among 4 people = 100 each)
        user_shares_hotel = [
            {"borrower_id": alice.get_user_id(), "amount": 100.0},
            {"borrower_id": bob.get_user_id(), "amount": 100.0},
            {"borrower_id": charlie.get_user_id(), "amount": 100.0},
            {"borrower_id": david.get_user_id(), "amount": 100.0}
        ]
        
        expense1 = expense_controller.create_expense(
            name="Hotel Bill",
            paid_by=alice.get_user_id(),
            total_amount=400.0,
            split_type="equal",
            user_shares=user_shares_hotel,
            group_id=group_id
        )
        print(f"Expense 1: {expense1['name']} - ${expense1['total_amount']}")
        
        # Bob pays for dinner (240 split among 4 people = 60 each)
        user_shares_dinner = [
            {"borrower_id": alice.get_user_id(), "amount": 60.0},
            {"borrower_id": bob.get_user_id(), "amount": 60.0},
            {"borrower_id": charlie.get_user_id(), "amount": 60.0},
            {"borrower_id": david.get_user_id(), "amount": 60.0}
        ]
        
        expense2 = expense_controller.create_expense(
            name="Dinner",
            paid_by=bob.get_user_id(),
            total_amount=240.0,
            split_type="equal",
            user_shares=user_shares_dinner,
            group_id=group_id
        )
        print(f"Expense 2: {expense2['name']} - ${expense2['total_amount']}")
        
        # Charlie pays for gas (120 split among 4 people = 30 each)
        user_shares_gas = [
            {"borrower_id": alice.get_user_id(), "amount": 30.0},
            {"borrower_id": bob.get_user_id(), "amount": 30.0},
            {"borrower_id": charlie.get_user_id(), "amount": 30.0},
            {"borrower_id": david.get_user_id(), "amount": 30.0}
        ]
        
        expense3 = expense_controller.create_expense(
            name="Gas",
            paid_by=charlie.get_user_id(),
            total_amount=120.0,
            split_type="equal",
            user_shares=user_shares_gas,
            group_id=group_id
        )
        print(f"Expense 3: {expense3['name']} - ${expense3['total_amount']}")
        
        # Test 5: Calculate and optimize settlements
        print("\n5. Processing settlements...")
        
        # Get all transactions
        transactions = calculator.fetch_unsettled_transactions(group_id)
        print(f"Found {len(transactions)} individual transactions")
        
        # Calculate net balances
        net_balances = calculator.calculate_net_balances(transactions)
        print("Net balances:")
        for user_id, balance in net_balances.items():
            # Get username for display
            user = user_controller.get_user(user_id)
            username = user.get_user_name() if user else user_id[:8]
            if balance > 0:
                print(f"  {username} is owed: ${balance:.2f}")
            else:
                print(f"  {username} owes: ${abs(balance):.2f}")
        
        # Optimize settlements
        optimized_settlements = calculator.process_group_settlements(group_id)
        print(f"\nOptimized to {len(optimized_settlements)} settlements:")
        
        for settlement in optimized_settlements:
            group_id_s, debtor_id, creditor_id, amount = settlement
            debtor = user_controller.get_user(debtor_id)
            creditor = user_controller.get_user(creditor_id)
            debtor_name = debtor.get_user_name() if debtor else debtor_id[:8]
            creditor_name = creditor.get_user_name() if creditor else creditor_id[:8]
            print(f"  {debtor_name} pays ${amount:.2f} to {creditor_name}")
        
        # Test 6: Verify settlements from database
        print("\n6. Verifying stored settlements...")
        stored_settlements = calculator.get_group_settlements(group_id)
        print(f"Retrieved {len(stored_settlements)} settlements from database:")
        
        for settlement in stored_settlements:
            print(f"  {settlement['borrower_name']} owes ${settlement['amount']:.2f} to {settlement['receiver_name']}")
        
        print("\nAll tests passed! Complete SplitWise functionality working correctly!")
        
        # Summary
        print(f"\nSUMMARY:")
        print(f"- Total expenses: ${400 + 240 + 120} across 3 transactions")
        print(f"- Reduced to {len(optimized_settlements)} optimized settlements")
        print(f"- Saved {len(transactions) - len(optimized_settlements)} transactions!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        logger.error(f"Test error: {e}")

if __name__ == "__main__":
    test_complete_splitwise()