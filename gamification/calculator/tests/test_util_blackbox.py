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
