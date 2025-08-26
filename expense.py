import uuid
import logging
from equal_split import EqualExpenseSplit  
from unequal_split import UnequalExpenseSplit  
from percentage_split import PercentageExpenseSplit

logger = logging.getLogger(__name__)

class Expense:
    SPLIT_STRATEGIES = {
        "equal": EqualExpenseSplit,
        "unequal": UnequalExpenseSplit,
        "percentage": PercentageExpenseSplit
    }
    
    def __init__(self, name, paid_by, total_amount, split_type, user_shares, group_id):
        if not all([name, paid_by, total_amount, split_type, user_shares, group_id]):
            raise ValueError("All expense parameters are required")
        if total_amount <= 0:
            raise ValueError("Total amount must be positive")
        if split_type not in self.SPLIT_STRATEGIES:
            raise ValueError(f"Invalid split type. Must be one of: {list(self.SPLIT_STRATEGIES.keys())}")
            
        self.expense_id = uuid.uuid4().hex
        self.name = name.strip()
        self.paid_by = paid_by
        self.total_amount = float(total_amount)
        self.split_type = split_type
        self.user_shares = user_shares
        self.group_id = group_id

    def split_transactions(self):
        strategy_class = self.SPLIT_STRATEGIES[self.split_type]
        split_strategy = strategy_class()
        transactions = split_strategy.process_split(self.paid_by, self.user_shares, self.total_amount)
        return {borrower_id: {"paid_by": paid_by, "amount": amount} for borrower_id, paid_by, amount in transactions}
 
    def save_to_db(self, db):
        """Save expense and shares to database"""
        try:
            # Save main expense
            expense_query = '''
                INSERT INTO expense (expense_id, name, paid_by, total_amount, split_type, group_id)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            db.cur.execute(expense_query, (
                self.expense_id, self.name, self.paid_by, 
                self.total_amount, self.split_type, self.group_id
            ))

            # Save shares
            share_query = '''
                INSERT INTO expense_share (expense_id, borrower_id, paid_by_id, amount)
                VALUES (?, ?, ?, ?)
            '''
            for share in self.user_shares:
                borrower_id = share["borrower_id"]
                amount = float(share.get("amount", 0))
                db.cur.execute(share_query, (self.expense_id, borrower_id, self.paid_by, amount))

            logger.info(f"Expense {self.expense_id} saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving expense: {e}")
            raise
