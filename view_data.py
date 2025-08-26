#!/usr/bin/env python3
"""
Backend data viewer for SplitWise database
"""

from connection_sqlite import Database
import logging

logging.basicConfig(level=logging.INFO)

def view_all_data():
    print("=== SPLITWISE DATABASE VIEWER ===\n")
    
    with Database() as db:
        # View Users
        print("USERS:")
        print("-" * 50)
        db.cur.execute("SELECT user_id, user_name, created_at FROM users ORDER BY created_at")
        users = db.cur.fetchall()
        if users:
            print(f"{'ID':<35} {'Name':<20} {'Created'}")
            print("-" * 70)
            for user in users:
                user_id = user[0][:8] + "..." if len(user[0]) > 8 else user[0]
                print(f"{user_id:<35} {user[1]:<20} {user[2] or 'N/A'}")
        else:
            print("No users found")
        
        # View Groups
        print(f"\nGROUPS:")
        print("-" * 50)
        db.cur.execute("SELECT group_id, group_name, created_at FROM groups ORDER BY created_at")
        groups = db.cur.fetchall()
        if groups:
            print(f"{'ID':<35} {'Name':<20} {'Created'}")
            print("-" * 70)
            for group in groups:
                group_id = group[0][:8] + "..." if len(group[0]) > 8 else group[0]
                print(f"{group_id:<35} {group[1]:<20} {group[2] or 'N/A'}")
        else:
            print("No groups found")
        
        # View Group Members
        print(f"\nGROUP MEMBERS:")
        print("-" * 50)
        db.cur.execute("""
            SELECT g.group_name, u.user_name, gm.joined_at
            FROM group_members gm
            JOIN groups g ON gm.group_id = g.group_id
            JOIN users u ON gm.user_id = u.user_id
            ORDER BY g.group_name, u.user_name
        """)
        members = db.cur.fetchall()
        if members:
            current_group = None
            for member in members:
                if member[0] != current_group:
                    current_group = member[0]
                    print(f"\n  Group: {current_group}")
                print(f"    - {member[1]} (joined: {member[2] or 'N/A'})")
        else:
            print("No group members found")
        
        # View Expenses
        print(f"\nEXPENSES:")
        print("-" * 50)
        db.cur.execute("""
            SELECT e.name, u.user_name as paid_by, e.total_amount, 
                   e.split_type, g.group_name, e.created_at
            FROM expense e
            JOIN users u ON e.paid_by = u.user_id
            JOIN groups g ON e.group_id = g.group_id
            ORDER BY e.created_at DESC
        """)
        expenses = db.cur.fetchall()
        if expenses:
            for expense in expenses:
                print(f"  {expense[0]}")
                print(f"     Paid by: {expense[1]}")
                print(f"     Amount: ${expense[2]:.2f}")
                print(f"     Split: {expense[3]}")
                print(f"     Group: {expense[4]}")
                print(f"     Date: {expense[5] or 'N/A'}")
                print()
        else:
            print("No expenses found")
        
        # View Expense Shares
        print(f"\nEXPENSE SHARES:")
        print("-" * 50)
        db.cur.execute("""
            SELECT e.name, u1.user_name as borrower, u2.user_name as paid_by, 
                   es.amount, es.created_at
            FROM expense_share es
            JOIN expense e ON es.expense_id = e.expense_id
            JOIN users u1 ON es.borrower_id = u1.user_id
            JOIN users u2 ON es.paid_by_id = u2.user_id
            ORDER BY e.name, u1.user_name
        """)
        shares = db.cur.fetchall()
        if shares:
            current_expense = None
            for share in shares:
                if share[0] != current_expense:
                    current_expense = share[0]
                    print(f"\n  Expense: {current_expense}")
                print(f"    {share[1]} owes ${share[3]:.2f} to {share[2]}")
        else:
            print("No expense shares found")
        
        # View Settlements
        print(f"\nOPTIMIZED SETTLEMENTS:")
        print("-" * 50)
        db.cur.execute("""
            SELECT g.group_name, u1.user_name as borrower, u2.user_name as receiver, 
                   bs.amount, bs.created_at
            FROM balance_sheet bs
            JOIN groups g ON bs.group_id = g.group_id
            JOIN users u1 ON bs.borrower_id = u1.user_id
            JOIN users u2 ON bs.receiver_id = u2.user_id
            ORDER BY g.group_name, bs.amount DESC
        """)
        settlements = db.cur.fetchall()
        if settlements:
            current_group = None
            for settlement in settlements:
                if settlement[0] != current_group:
                    current_group = settlement[0]
                    print(f"\n  Group: {current_group}")
                print(f"    {settlement[1]} pays ${settlement[3]:.2f} to {settlement[2]}")
        else:
            print("No settlements found")
        
        # Database Statistics
        print(f"\nDATABASE STATISTICS:")
        print("-" * 50)
        db.cur.execute("SELECT COUNT(*) FROM users")
        user_count = db.cur.fetchone()[0]
        
        db.cur.execute("SELECT COUNT(*) FROM groups")
        group_count = db.cur.fetchone()[0]
        
        db.cur.execute("SELECT COUNT(*) FROM expense")
        expense_count = db.cur.fetchone()[0]
        
        db.cur.execute("SELECT SUM(total_amount) FROM expense")
        total_expenses = db.cur.fetchone()[0] or 0
        
        db.cur.execute("SELECT COUNT(*) FROM balance_sheet")
        settlement_count = db.cur.fetchone()[0]
        
        print(f"  Total Users: {user_count}")
        print(f"  Total Groups: {group_count}")
        print(f"  Total Expenses: {expense_count}")
        print(f"  Total Amount: ${total_expenses:.2f}")
        print(f"  Active Settlements: {settlement_count}")

if __name__ == "__main__":
    view_all_data()