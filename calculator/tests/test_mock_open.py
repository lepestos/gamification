from collections import Counter
from decimal import Decimal
from random import seed

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models.blackbox import BlackBox, BlackBoxItem
from calculator.models.product import Product
from calculator.utils.blackbox import LOT_CATEGORIES


seed(42)


class MockOpenTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.products = [Product.objects.create(name=f'Product #{i}',
                                               price=1000) for i in range(3)]
        for product in cls.products:
            product.save()

        cls.bb_1 = cls.create_bb('Box 1', 2000, cls.products, [1, 1, 1])
        cls.bb_2 = cls.create_bb('Box 2', 2000, cls.products, [10, 20, 30])

    @staticmethod
    def create_bb(name, price, products, amounts):
        bb = BlackBox.objects.create(name=name, price=price, loyalty=0.6, rentability=0.3)
        items = [BlackBoxItem.objects.create(
            black_box=bb, product=product, amount=amount
        ) for product, amount in zip(products, amounts)]
        for item in items:
            item.save()
        bb.save()
        return bb

    def test_mock_open_small(self):
        res = self.bb_1.mock_open(3)
        self.assertEqual(set(res), set(LOT_CATEGORIES))
        res = self.bb_1.mock_open(0)
        self.assertEqual(res, [])

    def test_mock_open_large(self):
        res = self.bb_2.mock_open(60)
        self.assertEqual(Counter(res), Counter(
            {'costly': 10, 'middle': 20, 'cheap': 30}
        ))
        res = self.bb_2.mock_open(1000)
        self.assertEqual(Counter(res), Counter(
            {'costly': 10, 'middle': 20, 'cheap': 30}
        ))

    def test_api(self):
        pk = self.bb_1.pk
        response = self.client.post(reverse('blackbox-detail', args=[pk]) + 'mock_open/', data={'n': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(set(data['product_categories']), set(LOT_CATEGORIES))

    def test_rentability_is_never_negative(self):
        products = [Product.objects.create(name=f'Product {i}', price=i*100) for i in range(1, 4)]
        bb = self.create_bb('Box 3', 170, products, [1, 2, 3])
        cat_map = bb.lot_cost()
        for _ in range(10):
            res = bb.mock_open(6)
            total_giveaway = 0
            for i, category in enumerate(res):
                total_giveaway += cat_map[category]
                self.assertLessEqual(total_giveaway, Decimal((i + 1) * 170), msg=f'{i}th iteration')

    def test_mock_open_unsaved_api(self):
        data = {
            'name': 'Box 3',
            'price': 170,
            'lot_cost': {'costly': 300, 'middle': 200, 'cheap': 100},
            'lot_amount': {'costly': 1, 'middle': 2, 'cheap': 3},
            'n': 6
        }
        response = self.client.post(reverse('blackbox-list') + 'mock_open_unsaved/',
                                    data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res = response.json()['product_categories']
        self.assertEqual(Counter(res), Counter(data['lot_amount']))
