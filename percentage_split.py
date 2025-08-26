class PercentageExpenseSplit:
    def process_split(self, paid_by, user_shares, total_amount):
        """
        Distributes an expense based on percentage shares.

        :param paid_by: UUID of the user who paid the expense
        :param user_shares: List of dictionaries [{"userid": id, "percentage": percentage}]
        :param total_amount: The total amount paid
        :return: List of tuples in format (borrower_id, paid_by_id, amount)
        """
    
        total_percentage = sum(entry.get("percentage", 0) for entry in user_shares)
        if total_percentage != 100:
            raise ValueError("Sum of percentage shares must be exactly 100%.")

        split_transactions = []

        for entry in user_shares:
            user = entry.get("borrower_id")
            percentage = entry.get("percentage")

            if user is None or percentage is None:
                raise ValueError(f"Invalid entry format: {entry}")

            split_amount = (percentage / 100) * total_amount  

            if user != paid_by:  
                split_transactions.append((user, paid_by, split_amount))

        return split_transactions
