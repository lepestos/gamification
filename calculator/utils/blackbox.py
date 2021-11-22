from math import sqrt, ceil, floor
from typing import Dict, Iterable, List, Optional
from random import choices
from decimal import Decimal


PROFIT = 0.15
LOYALTY = 0.6

LOT_CATEGORIES = ('costly', 'middle', 'cheap')


class BlackBoxUtil:
    def __init__(self, lot_cost: Dict[str, float],  costly_amount: int,
                 black_box_cost: float, rentability: float = PROFIT,
                 loyalty: float = LOYALTY):
        self.prices = [float(lot_cost[category]) for category in LOT_CATEGORIES]
        self.max_count_costly = costly_amount
        self.profit = float(rentability)
        self.loyalty = float(loyalty)
        self.min_price = self.get_min_price()
        self.max_price = self.get_max_price()
        self.set_price(black_box_cost)
        self.probabilities = self.get_probabilities()
        self.amounts = self.get_amounts()
        self.update_probabilities()

    def to_json(self):
        max_p = self.get_rounded_max_price()
        min_p = self.get_rounded_min_price()
        if max_p < min_p:
            data = {
                'message': 'Цены дорогого и среднего лотов '
                           'отличаются на слишком маленькую величину.',
                'success': True
            }
        elif not self.validate_output_size():
            data = {
                'message': 'Слишком большие значения, попробуйте уменьшить входные данные',
                'success': False
            }
        else:
            lot_amount = convert_to_dict(self.amounts)
            lot_cost = convert_to_dict(self.prices)
            loyalty = get_loyalty(lot_amount)
            rentability = get_rentability(lot_amount, lot_cost, self.ticket_price)
            if rentability > 1:
                rentability = 1
            data = {
                'probabilities': convert_to_dict(self.probabilities),
                'amounts': lot_amount,
                'black_box_cost': {
                    'cur': self.ticket_price,
                    'max': max_p,
                    'min': min_p
                },
                'loyalty': loyalty,
                'rentability': rentability,
                'message': self.message,
                'success': True
            }
        return data

    def validate_output_size(self):
        if self.ticket_price >= 1e10:
            return False
        for amount in self.amounts:
            if amount >= 1e10:
                return False
        return True

    def set_price(self, black_box_cost):
        if black_box_cost == 0:
            self.ticket_price = self.get_optimal_price()
            self.message = ''
        elif not self.min_price <= black_box_cost <= self.max_price:
            self.ticket_price = self.get_optimal_price()
            self.message = f'С новыми значениями констант цена должна ' \
                           f'лежать в интервале от {self.get_rounded_min_price()} ' \
                           f'до {self.get_rounded_max_price()}, поэтому она была перерасчитана.'
        else:
            self.ticket_price = float(black_box_cost)
            self.message = ''

    def get_probabilities(self):
        p3 = 1 - self.loyalty
        p1 = (self.ticket_price / (self.profit + 1)
              - self.loyalty * (self.prices[1] - self.prices[2])
              - self.prices[2])\
             / (self.prices[0] - self.prices[1])
        p2 = self.loyalty - p1
        return p1, p2, p3

    def get_max_price(self):
        return round((self.profit + 1)
                     * (self.loyalty * self.prices[0]
                        - self.loyalty * self.prices[2] + self.prices[2]),
                     2)

    def get_min_price(self):
        res = round((self.profit + 1)
                     * (self.loyalty * self.prices[1]
                        - self.loyalty * self.prices[2] + self.prices[2]),
                     2)
        if self.profit == 0:
            res += 10
        return res

    def get_amounts(self):
        a1 = self.max_count_costly
        p1, p2, p3 = self.probabilities
        if abs(p1) < 1e-4:
            if p2 >= p3:
                return 0, a1, ceil(a1 * p3 / p2)
            return 0, floor(a1 * p2 / p3), a1
        return a1, ceil(a1 * p2 / p1), ceil(a1 * p3 / p1)

    def update_probabilities(self):
        total_amount = sum(self.amounts)
        self.probabilities = [round(amount/total_amount, 3) for amount in self.amounts]

    def get_optimal_price(self):
        return self.round_up(
            self.geometric_mean(self.min_price, self.max_price)
        )

    def get_rounded_max_price(self):
        return self.round_down(self.max_price)

    def get_rounded_min_price(self):
        return self.round_up(self.min_price)

    @staticmethod
    def geometric_mean(a:float, b:float) -> float:
        return sqrt(a * b)

    @staticmethod
    def round_up(price):
        return ceil(price / 10) * 10

    @staticmethod
    def round_down(price):
        return floor(price / 10) * 10


def convert_to_dict(it: Iterable) -> Dict:
    return {key: round(value, 3) for key, value in zip(LOT_CATEGORIES, it)}


def convert_to_list(dct: Dict) -> List:
    return [dct[cat] for cat in LOT_CATEGORIES]


def get_loyalty(lot_amount: Dict[str, float]):
    numerator = lot_amount['costly'] + lot_amount['middle']
    denominator = sum(lot_amount.values())
    return round(numerator / denominator, 2)


def get_rentability(lot_amount, lot_cost, price):
    total_amount = sum(lot_amount.values())
    expected_value = sum(lot_amount[key] * lot_cost[key] for key in lot_amount) / total_amount
    return round(price / expected_value - 1, 2)


def open_box_n_times(n: int, amounts: List[int],
                     costs: List[Decimal], box_price: Decimal) -> List[str]:
    res = []
    total_giveaway = Decimal(0)
    gained = Decimal(0)
    for _ in range(n):
        gained += box_price
        item_number = get_item(amounts, costs, total_giveaway, gained)
        if item_number is None:
            break
        amounts[item_number] -= 1
        total_giveaway += costs[item_number]
        res.append(LOT_CATEGORIES[item_number])
    return res


def get_item(amounts: List[int], costs: List[Decimal],
             total_giveaway: Decimal, gained: Decimal) -> Optional[int]:
    valid_options = [i for i in range(3) if amounts[i] > 0 and total_giveaway + costs[i] <= gained]
    weights = [amounts[i] for i in valid_options]
    if len(valid_options) == 0:
        return
    i = choices(valid_options, weights=weights)[0]
    return i


if __name__ == '__main__':
    data = {
        "lot_cost": {'costly': 40, 'middle': 30, 'cheap': 10},
        "costly_amount": 10,
        "black_box_cost": 160,
        "rentability": 0.15,
        "loyalty": 0.6
    }
    box = BlackBoxUtil(**data)
    print(box.to_json())
