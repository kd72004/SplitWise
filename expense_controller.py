from connection_sqlite import Database 
from expense import Expense
import logging
import sqlite3

logger = logging.getLogger(__name__)

class ExpenseController:
    def create_expense_original(self, name, paid_by, total_amount, split_type, user_shares, group_id):
        """
        Creates an expense and records the shares in a separate table.
        """
        try:
            expense = Expense(name, paid_by, total_amount, split_type, user_shares, group_id)
            
            with Database() as db:
                expense.save_to_db(db)
                
            return {
                "expense_id": expense.expense_id,
                "name": expense.name,
                "paid_by": expense.paid_by,
                "total_amount": expense.total_amount,
                "group_id": expense.group_id,
                "split_type": expense.split_type,
                "user_shares": expense.user_shares,
                "split_transactions": expense.split_transactions()
            }
        except ValueError as e:
            logger.error(f"Validation error creating expense: {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"Database error creating expense: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating expense: {e}")
            raise
    
    def create_expense(self, group_id, description, total_amount, paid_by, member_ids):
        """Create equal split expense"""
        try:
            # Calculate equal shares
            share_amount = total_amount / len(member_ids)
            user_shares = [{"borrower_id": member_id, "amount": share_amount} for member_id in member_ids]
            
            expense = Expense(description, paid_by, total_amount, 'equal', user_shares, group_id)
            
            with Database() as db:
                expense.save_to_db(db)
                
            return {'success': True, 'expense_id': expense.expense_id}
        except Exception as e:
            logger.error(f"Error creating expense: {e}")
            return {'success': False, 'message': str(e)}
    
    def create_custom_expense(self, group_id, description, total_amount, paid_by, member_amounts):
        """Create custom split expense"""
        try:
            # Validate amounts sum to total
            if abs(sum(member_amounts.values()) - total_amount) > 0.01:
                return {'success': False, 'message': 'Individual amounts must sum to total amount'}
            
            user_shares = [{"borrower_id": member_id, "amount": amount} for member_id, amount in member_amounts.items()]
            expense = Expense(description, paid_by, total_amount, 'unequal', user_shares, group_id)
            
            with Database() as db:
                expense.save_to_db(db)
                
            return {'success': True, 'expense_id': expense.expense_id}
        except Exception as e:
            logger.error(f"Error creating custom expense: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_group_expenses(self, group_id):
        """Get all expenses for a group"""
        with Database() as db:
            try:
                query = """
                SELECT e.expense_id, e.name, e.total_amount, e.paid_by, u.user_name, e.created_at
                FROM expense e
                JOIN users u ON e.paid_by = u.user_id
                WHERE e.group_id = ?
                ORDER BY e.created_at DESC
                """
                db.cur.execute(query, (group_id,))
                results = db.cur.fetchall()
                
                class ExpenseObj:
                    def __init__(self, expense_id, description, total_amount, paid_by, paid_by_name, created_at):
                        self.expense_id = expense_id
                        self.description = description
                        self.total_amount = total_amount
                        self.paid_by = paid_by
                        self.paid_by_name = paid_by_name
                        self.created_at = created_at
                
                return [ExpenseObj(row[0], row[1], row[2], row[3], row[4], row[5]) for row in results]
            except sqlite3.Error as e:
                logger.error(f"Error fetching expenses: {e}")
                return []