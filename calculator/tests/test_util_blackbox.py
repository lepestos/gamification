from copy import deepcopy
import unittest

from calculator.utils.blackbox import BlackBoxUtil


class BlackBoxTest(unittest.TestCase):
    def test_0_probability_costly(self):
        data = {
            "lot_cost": {'costly': 400, 'middle': 200, 'cheap': 100},
            "costly_amount": 10,
            "black_box_cost": 160,
            "rentability": 0,
            "loyalty": 0.6
        }
        box = BlackBoxUtil(**data)
        res = box.to_json()
        self.assertEqual(res['message'], f'С новыми значениями констант цена '
                                         f'должна лежать в интервале от 170 до '
                                         f'280, поэтому она была перерасчитана.')

    def test_send_message_on_too_large_numbers(self):
        data = {
            "lot_cost": {'costly': 4e11, 'middle': 2e11, 'cheap': 1e11},
            "costly_amount": 10,
            "black_box_cost": 3e11,
            "rentability": 0,
            "loyalty": 0.6
        }
        box = BlackBoxUtil(**data)
        res = box.to_json()
        self.assertFalse(res['success'])
        self.assertEqual(res['message'], 'Слишком большие значения, попробуйте уменьшить входные данные')


    def model_does_not_change_after_instant_recalculate(self):
        data = {
            'lot_cost': {'costly': 8000, 'middle': 2000, 'cheap': 1000},
            'costly_amount': 10,
            'black_box_cost': 0,
            'rentability': 0.15,
            'loyalty': 0.6,
        }
        box = BlackBoxUtil(**data)
        res1 = box.to_json()
        inp = deepcopy(res1)
        inp.pop('message')
        inp.pop('success')
        inp.pop('amounts')
        inp.pop('probabilities')
        inp['black_box_cost'] = res1['black_box_cost']['cur']
        inp['lot_cost'] = data['lot_cost']
        inp['costly_amount'] = data['costly_amount']
        box = BlackBoxUtil(**inp)
        res2 = box.to_json()
        self.assertEqual(res1['probabilities'], res2['probabilities'])
        self.assertEqual(res1, res2)
