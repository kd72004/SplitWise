from connection import Database 
from expense import Expense

class ExpenseController:
    def __init__(self):
        self.db = Database()  

    def create_expense(self, name, paid_by, total_amount, split_type, user_shares, group_id):
        """
        Creates an expense and records the shares in a separate table.

        :param name: Name of the expense
        :param paid_by: UUID of the user who paid
        :param total_amount: Total amount of the expense
        :param split_type: "equal", "unequal", or "percentage"
        :param user_shares: List of dictionaries defining shares
        :param group_id: UUID of the group
        :return: Dictionary containing expense details
        """
        expense = Expense(name, paid_by, total_amount, split_type, user_shares, group_id, self.db)
        return {
            "expense_id": expense.expense_id,
            "name": expense.name,
            "paid_by": expense.paid_by,
            "total_amount": expense.total_amount,
            "group_id": expense.group_id,
            "split_type": expense.split_type,
            "user_shares": expense.user_shares,
            "split_transactions":expense.split_transactions()
        }

    def close_connection(self):
        """Close the database connection."""
        self.db.close()
