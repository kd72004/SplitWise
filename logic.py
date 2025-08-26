import heapq
from connection_sqlite import Database
import logging
import sqlite3

logger = logging.getLogger(__name__)

class MaxHeap:
    def __init__(self):
        self.data = []
    
    def push(self, item):
        self.data.append(item)
        self.data.sort(key=lambda x: x[0], reverse=True)
    
    def pop(self):
        return self.data.pop(0) if self.data else None
    
    def is_empty(self):
        return len(self.data) == 0

class BalanceCalculator:
    def extract_id(self, val):
        """Extract clean ID from various formats"""
        if not val:
            return val
        if isinstance(val, dict) and '_id' in val:
            return str(val['_id'])
        return str(val)
    
    def calculate_net_balances(self, transactions):
        """Compute net balances for each user."""
        if not transactions:
            return {}
            
        net = {}
        for payer, borrower, amount in transactions:
            payer_id = self.extract_id(payer)
            borrower_id = self.extract_id(borrower)
            
            if not all([payer_id, borrower_id, amount]):
                continue
                
            # Payer gets positive balance (they are owed money)
            net[payer_id] = net.get(payer_id, 0) + float(amount)
            # Borrower gets negative balance (they owe money)
            net[borrower_id] = net.get(borrower_id, 0) - float(amount)
        
        # Remove users with zero balance
        return {user: amt for user, amt in net.items() if abs(amt) >= 0.01}

    def settle_transactions(self, net_balances, group_id):
        """Use MaxHeap to minimize the number of transactions (like JavaScript version)"""
        if not net_balances or not group_id:
            return []
        
        logger.info(f"Net balances: {net_balances}")
        
        # Prepare MaxHeaps for creditors and debtors
        creditors = MaxHeap()  # [amount, userId] - people who are owed money
        debtors = MaxHeap()    # [amount, userId] - people who owe money (stored as positive)
        
        for user, amount in net_balances.items():
            if amount > 0.01:  # Creditor (owed money)
                creditors.push([amount, user])
            elif amount < -0.01:  # Debtor (owes money)
                debtors.push([-amount, user])  # Store as positive for max heap
        
        # Settle debts
        settlements = []
        while not creditors.is_empty() and not debtors.is_empty():
            credit_amt, credit_user = creditors.pop()
            debt_amt, debt_user = debtors.pop()
            
            settle_amt = min(credit_amt, debt_amt)
            
            # Avoid self-transactions
            if credit_user != debt_user and settle_amt > 0:
                settlements.append((group_id, debt_user, credit_user, round(settle_amt, 2)))
            
            # Put back remaining amounts
            if credit_amt > settle_amt:
                creditors.push([credit_amt - settle_amt, credit_user])
            if debt_amt > settle_amt:
                debtors.push([debt_amt - settle_amt, debt_user])
        
        logger.info(f"Generated {len(settlements)} optimized settlements")
        return settlements
    
    def fetch_unsettled_transactions(self, group_id):
        """Fetch all unsettled expense transactions for a group"""
        with Database() as db:
            try:
                # Get all expense shares for the group
                db.cur.execute("""
                    SELECT es.paid_by_id, es.borrower_id, es.amount
                    FROM expense_share es
                    JOIN expense e ON es.expense_id = e.expense_id
                    WHERE e.group_id = ?
                """, (group_id,))
                
                transactions = []
                for row in db.cur.fetchall():
                    paid_by, borrower, amount = row
                    if paid_by != borrower:  # Skip self-payments
                        transactions.append([paid_by, borrower, float(amount)])
                
                return transactions
            except sqlite3.Error as e:
                logger.error(f"Error fetching transactions: {e}")
                return []
    
    def process_group_settlements(self, group_id):
        """Main function to process and optimize group settlements"""
        try:
            # Fetch all transactions
            transactions = self.fetch_unsettled_transactions(group_id)
            
            if not transactions:
                logger.info("No transactions found for group")
                return []
            
            # Calculate net balances
            net_balances = self.calculate_net_balances(transactions)
            
            # Generate optimized settlements
            settlements = self.settle_transactions(net_balances, group_id)
            
            # Clear old settlements and store new ones
            if settlements:
                self.store_settlements(settlements)
            
            return settlements
            
        except Exception as e:
            logger.error(f"Error processing settlements: {e}")
            return []

    def store_settlements(self, transactions):
        """Store settlement transactions in database."""
        if not transactions:
            logger.info("No transactions to store")
            return
            
        with Database() as db:
            try:
                group_id = transactions[0][0]
                db.cur.execute("DELETE FROM balance_sheet WHERE group_id = ?", (group_id,))
                
                db.cur.executemany("""
                    INSERT INTO balance_sheet (group_id, borrower_id, receiver_id, amount) 
                    VALUES (?, ?, ?, ?)
                """, transactions)
                
                logger.info(f"Stored {len(transactions)} settlement transactions")
            except sqlite3.Error as e:
                logger.error(f"Error storing settlements: {e}")
                raise

    def get_group_settlements(self, group_id):
        """Retrieve settlement transactions for a group."""
        with Database() as db:
            try:
                db.cur.execute("""
                    SELECT bs.borrower_id, u1.user_name, bs.receiver_id, u2.user_name, bs.amount
                    FROM balance_sheet bs
                    JOIN users u1 ON bs.borrower_id = u1.user_id
                    JOIN users u2 ON bs.receiver_id = u2.user_id
                    WHERE bs.group_id = ?
                    ORDER BY bs.amount DESC
                """, (group_id,))
                
                results = db.cur.fetchall()
                return [{
                    "borrower_id": row[0],
                    "borrower_name": row[1],
                    "receiver_id": row[2],
                    "receiver_name": row[3],
                    "amount": float(row[4])
                } for row in results]
            except sqlite3.Error as e:
                logger.error(f"Error fetching settlements: {e}")
                return []