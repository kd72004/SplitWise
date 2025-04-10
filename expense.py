import uuid
from equal_split import EqualExpenseSplit  
from unequal_split import UnequalExpenseSplit  
from percentage_split import PercentageExpenseSplit  
class Expense:
    def __init__(self, name, paid_by, total_amount, split_type, user_shares, group_id, db):
        self.expense_id = str(uuid.uuid4())  
        self.name = name
        self.paid_by = paid_by
        self.total_amount = total_amount
        self.split_type = split_type
        self.user_shares = user_shares
        self.group_id = group_id
        self.db = db 

        self.save_expense_to_db()  
        self.save_shares_to_db()  


    def split_transactions(self):
        if self.split_type == "equal":
            split_strategy = EqualExpenseSplit()
        elif self.split_type == "unequal":
            split_strategy = UnequalExpenseSplit()
        elif self.split_type == "percentage":
            split_strategy = PercentageExpenseSplit()
        else:
            raise ValueError("Invalid split type.")
        
        transactions = split_strategy.process_split(self.paid_by, self.user_shares, self.total_amount)


        split_transactions_dict = {borrower_id: {"paid_by": paid_by, "amount": amount} for borrower_id, paid_by, amount in transactions}
        
        return split_transactions_dict
 

    def save_expense_to_db(self):
        """Save the main expense details to the `expense` table."""  
        try:
            query = '''
                INSERT INTO expense (expense_id, name, paid_by, total_amount, split_type, group_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            self.db.cur.execute(query, (
                self.expense_id,
                self.name,
                self.paid_by,
                self.total_amount,
                self.split_type,
                self.group_id
            ))

            self.db.conn.commit()  
            print("Expense saved successfully!")

        except Exception as e:
            print(f" Error saving expense: {e}")

    def save_shares_to_db(self):
        """Save individual shares into the `expense_share` table."""  
        try:
            
            query = '''
                INSERT INTO expense_share (expense_id, borrower_id, paid_by_id, amount)
                VALUES (%s, %s, %s, %s)
            '''

            for share in self.user_shares:  
                borrower_id = share["borrower_id"]  
                amount = float(share["amount"]) 
                self.db.cur.execute(query, (self.expense_id, borrower_id, self.paid_by, amount))

            
            self.db.conn.commit()
                
            print("Expense shares saved successfully!")

        except Exception as e:
            print(f"Error saving expense shares: {e}")
