from past_main import get_result  
import heapq
from connection import Database  # Import Database class

db = Database()  # Establish database connection

def greedy(transactions):
    """Compute net balances for each user."""
    balance_map = {}
    for sender, receiver, amount in transactions:
        balance_map[sender] = balance_map.get(sender, 0) - amount  
        balance_map[receiver] = balance_map.get(receiver, 0) + amount  
    return balance_map

def settle_transactions(net_balances, group_id):
    """Use heaps to minimize the number of transactions required to settle balances."""
    giver_heap = []  
    taker_heap = []  
    final_result = []  

    # Split balances into heaps
    for person, balance in net_balances.items():
        if balance < 0:
            heapq.heappush(giver_heap, (balance, person))  
        elif balance > 0:
            heapq.heappush(taker_heap, (-balance, person))  

    # Process settlements
    while giver_heap and taker_heap:
        neg_balance, debtor = heapq.heappop(giver_heap)  
        pos_balance, creditor = heapq.heappop(taker_heap)  

        settle_amount = min(-neg_balance, -pos_balance)  
        final_result.append((group_id, debtor, creditor, settle_amount))  

        # Update remaining balances
        remaining_debt = neg_balance + settle_amount  
        remaining_credit = pos_balance + settle_amount  

        if remaining_debt < 0:
            heapq.heappush(giver_heap, (remaining_debt, debtor))  
        if remaining_credit < 0:
            heapq.heappush(taker_heap, (remaining_credit, creditor))  

    return final_result

def setup_database():
    """Create the balance_sheet table if it doesn't exist."""
    db.cur.execute("""
        CREATE TABLE IF NOT EXISTS balance_sheet (
            id SERIAL PRIMARY KEY,
            group_id TEXT,
            borrower_id TEXT,
            receiver_id TEXT,
            amount REAL
        )
    """)
    db.conn.commit()

def store_in_database(transactions):
    """Insert transaction records into the database."""
    db.cur.executemany("""
        INSERT INTO balance_sheet (group_id, borrower_id, receiver_id, amount) 
        VALUES (%s, %s, %s, %s)
    """, transactions)
    
    db.conn.commit()
    print("\n✅ Data successfully stored in database.")

def display_stored_data():
    """Retrieve and display all stored transactions."""
    db.cur.execute("SELECT * FROM balance_sheet")
    rows = db.cur.fetchall()

    print("\n📌 Stored Transactions in Database:")
    for row in rows:
        print(row)

# Main Execution Flow
if __name__ == "__main__":
    setup_database()  # Ensure database table exists

    # Fetch data dynamically
    data = get_result()  
    result, group_id = data  

    # Compute net balances
    net_balances = greedy(result)

    # Compute transactions
    transactions = settle_transactions(net_balances, group_id)

    # Store results in the database
    store_in_database(transactions)

    # Display stored transactions
    display_stored_data()
