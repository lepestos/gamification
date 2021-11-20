from typing import List, Union
from decimal import Decimal
from math import sqrt
from operator import itemgetter


BOOSTER_VALUES = (2, 3, 1.5, 2.5, 1.25, 1.75, 2.25, 2.75,)


class BingoUtil:
    @staticmethod
    def round_preserving_sum(amounts: List[Union[Decimal, float]]) -> List[int]:
        spare_amount = 0
        res = []
        for amount in amounts:
            if int(amount) == amount:
                res.append(int(amount))
            elif int(amount) + 1 - amount <= Decimal(spare_amount) + Decimal(1e-2):
                spare_amount -= int(amount) + 1 - amount
                res.append(int(amount + 1))
            else:
                spare_amount += amount - int(amount)
                res.append(int(amount))
        return res


class MiniBingoUtil:
    """
    As if we only had a single lot
    """
    def __init__(self, price: Decimal, discounts: List[Decimal],
                 budget: Decimal, lucky_participants: int, calculate: bool=True):
        self.price = price
        self.discounts = discounts
        self.k = len(self.discounts)
        self.budget = budget
        self.lucky_participants = lucky_participants
        if not calculate:
            return
        self.amounts = self.get_amounts()

    def get_amounts(self):
        return self.round_wo_exceeding_budget(self.get_unadjusted_amounts())

    def get_unadjusted_amounts(self):
        if self.budget < self.get_min_budget():
            return self.solve_amounts_low_budget()
        elif self.budget > self.get_max_budget():
            return self.solve_amounts_high_budget()
        else:
            return self.solve_amounts_normal_budget()

    def get_max_budget(self):
        max_budget = self.price * self.lucky_participants * self.discounts[-1]
        return max_budget

    def get_min_budget(self):
        min_budget = self.price * self.lucky_participants * self.discounts[0]
        return min_budget

    def solve_amounts_low_budget(self):
        am = int(self.budget / (self.discounts[0] * self.price))
        return [am] + [0] * (self.k - 1)

    def solve_amounts_high_budget(self):
        am = self.lucky_participants
        return [0] * (self.k - 1) + [am]

    def solve_amounts_normal_budget(self):
        if self.budget >= self.get_threshold():
            return self.apply_formulae(self.discounts[::-1])[::-1]
        else:
            return self.apply_formulae(self.discounts)

    def apply_formulae(self, discounts):
        solution = self.apply_first_two_formulae(discounts)
        for i in range(2, self.k):
            solution.append(self.apply_ith_formula(discounts, solution, i))
        return solution

    def apply_first_two_formulae(self, discounts):
        res = []
        sum_sq_roots = sum(sqrt(discount) for discount in discounts[1:])
        sum_rev_sq_roots = sum(1 / sqrt(discount) for discount in discounts[1:])
        numerator = self.lucky_participants * sum_sq_roots - self.budget / self.price * sum_rev_sq_roots
        denominator = sum_sq_roots - discounts[0] * sum_rev_sq_roots
        res.append(numerator / denominator)
        numerator = self.budget / self.price - self.lucky_participants * discounts[0]
        denominator *= sqrt(discounts[1])
        res.append(numerator / denominator)
        return res

    @staticmethod
    def apply_ith_formula(discounts, solution, i):
        return solution[1] * sqrt(discounts[1] / discounts[i])

    def get_threshold(self):
        roots_sum = sum(sqrt(d) for d in self.discounts)
        reverse_roots_sum = sum(1 / sqrt(d) for d in self.discounts)
        return self.price * self.lucky_participants * roots_sum / reverse_roots_sum

    def round_wo_exceeding_budget(self, amounts: List[Decimal]) -> List[int]:
        assert (self.price * sum(d * a for d, a in zip(self.discounts, amounts)) - self.budget) <= 1e-2
        spare_budget = 0
        spare_amount = 0
        res = []
        for amount, discount in zip(amounts[::-1], self.discounts[::-1]):
            if int(amount) == amount:
                res.append(int(amount))
            elif ((int(amount) + 1 - amount) * discount * self.price <= spare_budget + 1e-2
                    and (int(amount) + 1 - amount) <= spare_amount + 1e-2):
                spare_budget, spare_amount = self.decrement(spare_budget, spare_amount,
                                                            amount, discount)
                res.append(int(amount + 1))
            else:
                spare_budget, spare_amount = self.increment(spare_budget, spare_amount,
                                                            amount, discount)
                res.append(int(amount))
            assert spare_budget >= -1e-2
        res = res[::-1]
        return res

    def decrement(self, spare_budget, spare_amount, amount, discount):
        spare_budget -= (int(amount) + 1 - amount) * discount * self.price
        spare_amount -= int(amount) + 1 - amount
        return spare_budget, spare_amount

    def increment(self, spare_budget, spare_amount, amount, discount):
        spare_budget += (amount - int(amount)) * discount * self.price
        spare_amount += amount - int(amount)
        return spare_budget, spare_amount


class DiscountBingoUtil(BingoUtil):
    def __init__(self, prices: List[Decimal], discounts: List[Decimal],
                 budget: Decimal, lucky_participants: int,
                 usage_probability: Decimal, unlucky_participants: int,
                 budget_distribution: List[Decimal]):
        self.message = ''
        self.success = True
        self.prices = prices
        self.discounts = sorted(discounts)
        self.n = len(self.prices)
        self.k = len(self.discounts)
        self.budget = budget
        self.lucky_participants = lucky_participants
        self.usage_probability = usage_probability
        self.set_unlucky_participants(unlucky_participants)
        self.set_budget_distribution(budget_distribution)
        self.abs_budget_distribution = self.get_abs_budget_distribution()
        self.participants_per_lot = self.get_participants_per_lot()
        self.amounts = self.get_amounts()
        self.lucky_participants = self.get_lucky_participants()
        self.total_participants = self.get_total_participants()
        self.expected_budget = self.get_expected_budget()

    def to_json(self):
        data = {
            'amounts': self.amounts,
            'participants_per_lot': self.participants_per_lot,
            'unlucky_participants': self.unlucky_participants,
            'total_participants': self.total_participants,
            'budget_distribution': [round(a, 2) for a in self.budget_distribution],
            'expected_budget': self.expected_budget,
            'message': self.message,
            'success': self.success,
            'lucky_participants': self.lucky_participants,
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

    def get_participants_per_lot(self) -> List[int]:
        nums = [self.lucky_participants * abd for abd in self.abs_budget_distribution]
        helper_sum = sum(s / c for s, c in zip(self.abs_budget_distribution, self.prices))
        dens = [c * helper_sum for c in self.prices]
        not_rounded_aml = [num / den for num, den in zip(nums, dens)]
        return self.round_preserving_sum(not_rounded_aml)

    def get_amounts(self):
        solutions = [self.get_amounts_for_single_lot(budget, participant_amount, price)
                     for budget, participant_amount, price
                     in zip(self.abs_budget_distribution,
                            self.participants_per_lot, self.prices)]
        self.participants_per_lot = [sum(sol) for sol in solutions]
        return solutions

    def get_amounts_for_single_lot(self, budget, participant_amount, price):
        mini_bingo = MiniBingoUtil(price, self.discounts, budget, participant_amount)
        return mini_bingo.amounts

    def get_unlucky_participants(self):
        return 0

    def get_total_participants(self):
        return self.lucky_participants + self.unlucky_participants

    def get_budget_distribution(self):
        return [Decimal(1/self.n)] * self.n

    def get_abs_budget_distribution(self):
        return self.round_preserving_sum([self.budget * bd for bd in self.budget_distribution])

    def get_expected_budget(self):
        expected_value_matrix = [[a * c * d for a, d in zip(amounts_row, self.discounts)]
                                 for amounts_row, c in zip(self.amounts, self.prices)]
        return sum(sum(row) for row in expected_value_matrix) * self.usage_probability

    def get_lucky_participants(self):
        return sum(self.participants_per_lot)


class BoosterBingoUtil(BingoUtil):
    def __init__(self, prices: List[Decimal], booster_amount: int,
                 fix_amount: int, budget: Decimal, participants: int,
                 abs_budget_distribution: List[Decimal]):
        self.message = ''
        self.success = True
        self.prices = prices
        self.n = len(self.prices)
        self.booster_amount = booster_amount
        self.fix_amount = fix_amount
        self.budget = budget
        self.participants = participants
        self.set_abs_budget_distribution(abs_budget_distribution)
        self.participants_per_mission = self.get_participants_per_mission()
        self.values = self.get_values()
        self.percentages = self.get_percentages()
        self.enumerated_percentages = self.get_enumerated_percentages()
        self.discounts, self.orders = self.get_discounts()
        self.participants_per_lot = self.participants_per_mission
        self.amounts = self.get_amounts()
        self.transform_amounts()


    def to_json(self):
        data = {
            'abs_budget_distribution': self.abs_budget_distribution,
            'values': self.values,
            'amounts': self.amounts,
            'message': self.message,
            'success': self.success,
        }
        return data

    def set_abs_budget_distribution(self, abs_budget_distribution):
        if abs_budget_distribution is None:
            self.abs_budget_distribution = self.get_abs_budget_distribution()
        else:
            self.abs_budget_distribution = abs_budget_distribution

    def get_abs_budget_distribution(self):
        return self.round_preserving_sum([self.budget/self.n] * self.n)

    def get_participants_per_mission(self):
        return self.round_preserving_sum([self.participants/self.n] * self.n)

    def get_values(self):
        values = [self.get_values_for_mission(price) for price in self.prices]
        return values

    def get_values_for_mission(self, price):
        values = dict()
        values['booster'] = list(BOOSTER_VALUES[:self.booster_amount])
        step = round(price / self.fix_amount, -1)
        values['fix'] = [step * i for i in range(1, self.fix_amount)] + [price + step]
        return values

    def get_percentages(self):
        percentages = [self.get_percentages_for_mission(price, mission_values)
                       for price, mission_values in zip(self.prices, self.values)]
        return percentages

    def get_percentages_for_mission(self, price, values):
        percentages = []
        for value in values['booster']:
            percentages.append(self.booster_to_percents(value))
        for value in values['fix']:
            percentages.append(self.fix_to_percents(value, price))
        return percentages

    def get_enumerated_percentages(self):
        return list(list(enumerate(p)) for p in self.percentages)

    def get_discounts(self):
        sorted_en_p = [sorted(ep, key=itemgetter(1)) for ep in self.enumerated_percentages]
        discounts = [[el[1] for el in row] for row in sorted_en_p]
        orders = [[el[0] for el in row] for row in sorted_en_p]
        return discounts, orders

    def get_amounts(self):
        solutions = []
        for participant_amount, price, budget, discounts \
                in zip(self.participants_per_lot, self.prices,
                       self.abs_budget_distribution, self.discounts):
            mini_bingo = MiniBingoUtil(price, discounts, budget, participant_amount)
            solutions.append(mini_bingo.amounts)
        self.participants_per_lot = [sum(sol) for sol in solutions]
        return solutions

    def transform_amounts(self):
        enum_amounts = [sorted(list(zip(ord_row, am_row)), key=itemgetter(0))
                        for am_row, ord_row in zip(self.amounts, self.orders)]
        raw_amounts = [[a[1] for a in row] for row in enum_amounts]
        self.amounts = raw_amounts

    @staticmethod
    def booster_to_percents(value):
        return value - 1

    @staticmethod
    def fix_to_percents(value, price):
        return value / price


if __name__ == '__main__':
    input_data = {'prices': [570, 1218, 1721], 'discounts': [0.1, 0.17, 0.71, 0.51, 0.58, 0.28, 0.77, 0.91, 0.02, 0.48],
                  'budget': 46536, 'lucky_participants': 87, 'usage_probability': 1, 'unlucky_participants': None,
                  'budget_distribution': None}
    bingo = DiscountBingoUtil(**input_data)
    print(bingo.to_json())

    input_data = {
        'prices': [100, 200],
        'booster_amount': 3,
        'fix_amount': 3,
        'budget': 1500,
        'participants': 10,
        'abs_budget_distribution': None,
    }
    bingo = BoosterBingoUtil(**input_data)
    print(bingo.to_json())
    print(bingo.enumerated_percentages)
    print(bingo.discounts)
    print(bingo.orders)
