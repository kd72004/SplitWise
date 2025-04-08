# expense_split_strategy.py
from abc import ABC, abstractmethod

class ExpenseSplitStrategy(ABC):
    @abstractmethod
    def validate_split_request(self, split_list, total_amount):
        pass
