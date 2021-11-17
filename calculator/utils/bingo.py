from typing import List
from decimal import Decimal


class DiscountBingoUtil:
    def __init__(self, prices: List[int], discounts: List[Decimal],
                 budget: Decimal, lucky_participants: int,
                 usage_probability: Decimal, unlucky_participants: int,
                 budget_distribution: List[Decimal]):
        self.prices = prices
        self.discounts = discounts
        self.budget = budget
        self.lucky_participants = lucky_participants
        self.usage_probability = usage_probability
        self.set_unlucky_participants(unlucky_participants)
        self.set_budget_distribution(budget_distribution)
        self.amounts = self.get_amounts()
        self.amount_per_lot = self.get_amount_per_lot()
        self.total_participants = self.get_total_participants()
        self.expected_budget = self.get_expected_budget()


    def to_json(self):
        data = {
            'amounts': self.amounts,
            'amount_per_lot': self.amount_per_lot,
            'unlucky_participants': self.unlucky_participants,
            'total_participants': self.total_participants,
            'budget_distribution': self.budget_distribution,
            'expected_budget': self.expected_budget,
        }
        return data

    def set_unlucky_participants(self, unlucky_participants):
        if unlucky_participants is None:
            self.unlucky_participants = self.get_unlucky_participants()
        else:
            self.unlucky_participants = unlucky_participants

    def set_budget_distribution(self, budget_distribution):
        if budget_distribution is None:
            self.budget_distribution = self.get_budget_distribution()
        else:
            self.budget_distribution = budget_distribution

    def get_amounts(self):
        pass

    def get_amount_per_lot(self):
        pass

    def get_unlucky_participants(self):
        pass

    def get_total_participants(self):
        pass

    def get_budget_distribution(self):
        pass

    def get_expected_budget(self):
        pass


class BoosterBingoUtil:
    pass
