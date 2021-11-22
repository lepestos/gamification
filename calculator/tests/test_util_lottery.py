import unittest
from random import seed
from copy import deepcopy

from calculator.utils.lottery import LotteryUtil


seed(42)


class LotteryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
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

    def test_initial(self):
        exp_response = {
            'write_off': 1000,
            'ticket_amount': {'cur': 24, 'min': 18, 'max': 136},
            'total_cost': 2600,
            'ticket_price': {'cur': 150, 'min': 10, 'max': 530},
            'min_profit': 250,
            'min_rentability': 0.1,
            'max_rentability': 0.38,
            'success': True,
            'message': ''
        }
        lottery = LotteryUtil(**self.data)
        self.assertEqual(lottery.to_json(), exp_response)

    def test_recalculate(self):
        data = deepcopy(self.data)
        data['ticket_amount'] = 30
        data['ticket_price'] = 130
        exp_response = {
            'write_off': 1300,
            'ticket_amount': {'cur': 30, 'min': 20, 'max': 150},
            'total_cost': 2600,
            'ticket_price': {'cur': 130, 'min': 10, 'max': 470},
            'min_profit': 364,
            'min_rentability': 0.14,
            'max_rentability': 0.5,
            'success': True,
            'message': ''
        }
        lottery = LotteryUtil(**data)
        self.assertEqual(lottery.to_json(), exp_response)

    def test_recalculate_too_few_tickets(self):
        data = deepcopy(self.data)
        data['ticket_amount'] = 17
        data['ticket_price'] = 150
        exp_response = {
            'write_off': 1000,
            'ticket_amount': {'cur': 24, 'min': 18, 'max': 136},
            'total_cost': 2600,
            'ticket_price': {'cur': 150, 'min': 10, 'max': 530},
            'min_profit': 250,
            'min_rentability': 0.1,
            'max_rentability': 0.38,
            'success': True,
            'message': 'Для заданной цены количество билетов должно быть '
                       'не меньше 18, поэтому оно было перерасчитано.'
        }
        lottery = LotteryUtil(**data)
        self.assertEqual(lottery.to_json(), exp_response)

    def test_bad_lots(self):
        data = deepcopy(self.data)
        data['lots'][1]['price'] = -2
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_bad_write_off(self):
        data = deepcopy(self.data)
        data['write_off'] = -100
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_bad_referral_coeff(self):
        data = deepcopy(self.data)
        data['referral_coeff'] = 3.5
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_bad_discount(self):
        data = deepcopy(self.data)
        data['discount'] = 1.05
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_bad_ticket_price(self):
        data = deepcopy(self.data)
        data['ticket_price'] = -1
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_bad_ticket_amount(self):
        data = deepcopy(self.data)
        data['ticket_amount'] = -1
        lottery = LotteryUtil(**data)
        self.assertFalse(lottery.to_json()['success'])

    def test_ticket_price_is_multiple_of_10(self):
        data = deepcopy(self.data)
        for i in range(3):
            data['lots'][i]['amount'] = 1
        lottery = LotteryUtil(**data)
        ticket_price = lottery.to_json()['ticket_price']['cur']
        self.assertEqual(ticket_price, (ticket_price // 10) * 10)

    def test_recalculate_invalid_ticket_amount(self):
        data = deepcopy(self.data)
        data['ticket_amount'] = 5
        data['ticket_price'] = 130
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertTrue(r['success'])
        self.assertEqual(r['message'], 'Для заданной цены количество билетов должно быть '
                                       'не меньше 20, поэтому оно было перерасчитано.')

    def test_only_ticket_price_or_ticket_amount_provided(self):
        data = deepcopy(self.data)
        data['ticket_amount'] = 30
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertFalse(r['success'])
        self.assertEqual(r['message'], "Error: ticket_amount and ticket_price must be either "
                                       "both zero or both non-zero")
        data = deepcopy(self.data)
        data['ticket_amount'] = 0
        data['ticket_amount'] = 130
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertFalse(r['success'])
        self.assertEqual(r['message'], "Error: ticket_amount and ticket_price must be either "
                                       "both zero or both non-zero")

    def test_no_referral_programme(self):
        data = deepcopy(self.data)
        data['referral_coeff'] = 0
        data['discount'] = 0
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertTrue(r['success'])
        self.assertEqual(r['min_rentability'], r['max_rentability'])
        self.assertEqual(r['write_off'], r['min_profit'])

    def test_no_referral_programme_write_off_and_min_profit_are_equal(self):
        data = {
            'lots': [{'amount': 100, 'price': 1000}],
            'write_off': 150000,
            'referral_coeff': 0,
            'discount': 0,
            'ticket_amount': 0,
            'ticket_price': 0,
        }
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertEqual(r['write_off'], r['min_profit'])

    def test_send_message_on_too_large_numbers(self):
        data = {
            'lots': [{'amount': 1e5, 'price': 1e6}],
            'write_off': 150000,
            'referral_coeff': 0,
            'discount': 0,
            'ticket_amount': 0,
            'ticket_price': 0,
        }
        lottery = LotteryUtil(**data)
        r = lottery.to_json()
        self.assertFalse(r['success'])
        self.assertEqual(r['message'], 'Слишком большие значения, попробуйте уменьшить входные данные')
        