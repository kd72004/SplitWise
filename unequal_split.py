class UnequalExpenseSplit:
    def process_split(self, paid_by, user_shares, total_amount):
        """
        Distributes an expense unequally.

        :param paid_by: UUID of the user who paid the expense
        :param user_shares: List of dictionaries [{"userid": id, "amount": amount}]
        :param total_amount: The total amount paid
        :return: List of tuples in format (borrower_id, paid_by_id, amount)
        """

        total_assigned_amount = sum(entry.get("amount", 0) for entry in user_shares)
        if total_assigned_amount != total_amount:
            raise ValueError("Sum of split amounts must match the total amount.")

        split_transactions = []

        for entry in user_shares:
            user = entry.get("borrower_id")
            amount = entry.get("amount")

            if user is None or amount is None:
                raise ValueError(f"Invalid entry format: {entry}")

            if user != paid_by:  
                split_transactions.append((user, paid_by, amount))

        return split_transactions
