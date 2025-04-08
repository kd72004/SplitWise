class EqualExpenseSplit:
    def process_split(self, paid_by, user_shares, total_amount):
        """
        Distributes the total_amount equally among users.

        :param paid_by: UUID of the user who paid the expense
        :param user_shares: List of dictionaries [{"userid": id}]
        :param total_amount: The total expense amount
        :return: List of tuples in format (borrower_id, paid_by_id, amount)
        """

        num_users = len(user_shares)
        if num_users == 0:
            raise ValueError("There must be at least one user to split the expense.")

        split_amount = total_amount / num_users
        split_transactions = []

        
        for entry in user_shares:
            user = entry.get("borrower_id")  # Use .get() to avoid KeyError
            if user is None:
                raise ValueError(f"Invalid entry format: {entry}")
            
            if user != paid_by:
                split_transactions.append((user, paid_by, split_amount))


        return split_transactions
