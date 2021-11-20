from math import floor, ceil
from typing import List, Dict


class LotteryUtil:
    def __init__(self, lots: List[Dict[str, int]], write_off: float,
                 ticket_amount: int, ticket_price: float,
                 referral_coeff, discount):
        self.message = ''
        self.success = True
        self.validate(lots, write_off, referral_coeff, discount, ticket_amount, ticket_price)
        if not self.success:
            return
        self.lot_amounts = [lot['amount'] for lot in lots]
        self.lot_prices = [lot['price'] for lot in lots]
        self.write_off = write_off
        self.set_referral_coeff(referral_coeff)
        self.discount = discount
        self.total_cost = self.get_total_cost()
        self.set_ticket_amount(ticket_amount, ticket_price)
        self.set_ticket_price(ticket_price)
        self.min_profit = self.get_min_profit()
        self.write_off = self.get_write_off()
        self.min_rentability = self.get_min_rentability()
        self.max_rentability = self.get_max_rentability()

    def to_json(self):
        if not self.success:
            return {
                'success': False,
                'message': self.message
            }
        min_p = self.get_cur_min_ticket_price()
        max_p = self.get_cur_max_ticket_price()
        min_a = self.get_cur_min_ticket_amount()
        max_a = self.get_cur_max_ticket_amount()
        data = {
            'write_off': self.write_off,
            'ticket_amount': {'cur': self.ticket_amount, 'min': min_a, 'max': max_a},
            'total_cost': self.total_cost,
            'ticket_price': {'cur': self.ticket_price, 'min': min_p, 'max': max_p},
            'min_profit': round(self.min_profit),
            'min_rentability': round(self.min_rentability, 2),
            'max_rentability': round(self.max_rentability, 2),
            'success': self.success,
            'message': self.message,
        }
        return data

    def validate(self, lots, write_off, referral_coeff,
                 discount, ticket_amount, ticket_price):
        for lot in lots:
            if lot['amount'] < 0:
                self.message = 'Error: lot amount < 0'
                self.success = False
            if lot['price'] < 0:
                self.message = 'Error: lot price < 0'
                self.success = False
        if write_off < 0:
            self.message = 'Error: write_off < 0'
            self.success = False
            return
        if referral_coeff < 0:
            self.message = 'Error: referral_coeff < 0'
            self.success = False
            return
        if referral_coeff != float('inf') and (referral_coeff - int(referral_coeff)) != 0:
            self.message = 'Error: referral_coeff must be integer'
            self.success = False
            return
        if not (0 <= discount <= 1):
            self.message = 'Error: discount must be a number between 0 and 1'
            self.success = False
            return
        if ticket_amount < 0:
            self.message = 'Error: ticket_amount < 0'
            self.success = False
            return
        if ticket_price < 0:
            self.message = 'Error: ticket_price < 0'
            self.success = False
            return
        if (ticket_price == 0) is not (ticket_amount == 0):
            self.message = "Error: ticket_amount and ticket_price must be " \
                           "either both zero or both non-zero"
            self.success = False
            return

    def set_ticket_amount(self, ticket_amount, ticket_price):
        if ticket_amount == 0:
            self.ticket_amount = self.get_ticket_amount()
        else:
            min_amount = self.get_min_ticket_amount(ticket_price)
            if ticket_amount < min_amount:
                print('here')
                self.ticket_amount = max(self.get_ticket_amount(), min_amount)
                self.message = f'Для заданной цены количество билетов должно быть ' \
                               f'не меньше {min_amount}, поэтому оно было перерасчитано.'
            else:
                self.ticket_amount = ticket_amount

    def set_ticket_price(self, ticket_price):
        if ticket_price == 0:
            self.ticket_price = self.get_ticket_price()
        else:
            self.ticket_price = ticket_price
            self.write_off = self.get_write_off()

    def set_referral_coeff(self, referral_coeff):
        if referral_coeff == 0:
            self.referral_coeff = float('inf')
        else:
            self.referral_coeff = referral_coeff

    def get_ticket_amount(self):
        return 4 * sum(self.lot_amounts)

    def get_total_cost(self):
        return sum(a * c for a, c in zip(self.lot_amounts, self.lot_prices))

    def get_ticket_price(self):
        return self.round_up((self.write_off + self.total_cost) / self.ticket_amount)

    def get_min_profit(self):
        factor1 = self.ticket_amount - floor(self.ticket_amount / (self.referral_coeff + 1))
        factor2 = 1 - self.discount
        factor3 = self.ticket_price
        deduction = self.total_cost
        return factor1 * factor2 * factor3 - deduction

    def get_min_rentability(self):
        return self.min_profit / self.total_cost

    def get_max_rentability(self):
        return self.write_off / self.total_cost

    def get_write_off(self):
        return self.ticket_amount * self.ticket_price - self.total_cost

    def get_min_ticket_amount(self, price):
        return max(ceil(self.total_cost / price), sum(self.lot_amounts))

    def get_cur_min_ticket_amount(self):
        return max(ceil(self.total_cost / self.ticket_price), sum(self.lot_amounts))

    def get_cur_max_ticket_amount(self):
        min_ta = self.get_cur_min_ticket_amount()
        return 3 * self.ticket_amount - 2 * min_ta + 100

    def get_cur_min_ticket_price(self):
        # return self.round_up(self.total_cost / self.ticket_amount)
        return 10

    def get_cur_max_ticket_price(self):
        min_tp = self.get_cur_min_ticket_price()
        return 3 * self.ticket_price - 2 * min_tp + 100

    @staticmethod
    def round_up(price):
        return ceil(price / 10) * 10


if __name__ == '__main__':
    input_data = {
        'lots': [
            {'amount': 1, 'price': 1000},
            {'amount': 2, 'price': 500},
            {'amount': 3, 'price': 200},
        ],
        'write_off': 1000,
        'referral_coeff': 4,
        'discount': 0.05,
        'ticket_amount': 0,
        'ticket_price': 0
    }
    lottery = LotteryUtil(**input_data)
    print(lottery.to_json())

    input_data = {
        'lots': [
            {'amount': 1, 'price': 1000},
            {'amount': 2, 'price': 500},
            {'amount': 3, 'price': 200},
        ],
        'write_off': 1000,
        'referral_coeff': 4,
        'discount': 0.05,
        'ticket_amount': 30,
        'ticket_price': 130
    }
    lottery = LotteryUtil(**input_data)
    print(lottery.to_json())

    input_data = {
        'lots': [
            {'amount': 1, 'price': 1000},
            {'amount': 1, 'price': 500},
            {'amount': 1, 'price': 200},
        ],
        'write_off': 1000,
        'referral_coeff': 4,
        'discount': 0.05,
        'ticket_amount': 0,
        'ticket_price': 0
    }
    lottery = LotteryUtil(**input_data)
    print(lottery.to_json())
