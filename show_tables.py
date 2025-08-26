#!/usr/bin/env python3
"""
Quick table overview for SplitWise database
"""

from connection_sqlite import Database

def show_tables():
    print("=== SPLITWISE DATABASE TABLES ===\n")
    
    with Database() as db:
        # Get all table names
        db.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in db.cur.fetchall()]
        
        print(f"Total Tables: {len(tables)}\n")
        
        for table in tables:
            print(f"TABLE: {table.upper()}")
            print("-" * 40)
            
            # Get table structure
            db.cur.execute(f"PRAGMA table_info({table})")
            columns = db.cur.fetchall()
            
            # Get row count
            db.cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = db.cur.fetchone()[0]
            
            print(f"Rows: {count}")
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Show purpose
            purpose = {
                'users': 'Stores user accounts (ID, name)',
                'groups': 'Stores expense groups',
                'group_members': 'Links users to groups (many-to-many)',
                'expense': 'Main expense records',
                'expense_share': 'Individual shares of each expense',
                'balance_sheet': 'Optimized settlements (who pays whom)'
            }
            
            if table in purpose:
                print(f"Purpose: {purpose[table]}")
            
            print()

if __name__ == "__main__":
    show_tables()