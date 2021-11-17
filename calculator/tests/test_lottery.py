from copy import deepcopy
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models.product import Product
from calculator.models.lottery import Lottery, Ticket


class LotteryTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        Product.objects.all()
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'name': 'Lottery',
            'lots': [
                {'amount': 1, 'price': 1000.0},
                {'amount': 2, 'price': 500.0},
                {'amount': 3, 'price': 200.0}
            ],
            'write_off': 1000.0,
            'referral_coeff': 4,
            'ticket_amount': 24,
            'total_cost': 2600.0,
            'ticket_price': 150.0,
            'min_profit': 250.0,
            'min_rentability': 0.1,
            'max_rentability': 0.38,
            'discount': 0.05
            }
        cls.other_data = {
            'name': 'Lottery',
            'lots': [
                {'amount': 1, 'price': 1000.0},
                {'amount': 2, 'price': 500.0},
                {'amount': 3, 'price': 200.0}
            ],
            'write_off': 1300.0,
            "referral_coeff": 4,
            'ticket_amount': 30,
            'total_cost': 2600.0,
            'ticket_price': 130.0,
            'min_profit': 364.0,
            'min_rentability': 0.14,
            'max_rentability': 0.5,
            'discount': 0.05
            }
        cls.products = [Product.objects.create(name=name, price=price)
                        for name, price in zip(['p1', 'p2', 'p3'], [1000, 500, 200])]
        for product in cls.products:
            product.save()

    def tearDown(self):
        Lottery.objects.all().delete()
        Ticket.objects.all().delete()

    def test_post(self):
        response = self.client.post(reverse('lottery-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lottery = Lottery.objects.get()
        self.assertEqual(lottery.lots(), [
                {"amount": 1, "price": 1000.0},
                {"amount": 2, "price": 500.0},
                {"amount": 3, "price": 200.0}
            ],)
        self.assertEqual(lottery.write_off, Decimal('1000.0'))
        self.assertEqual(lottery.referral_coeff, 4)
        self.assertEqual(lottery.ticket_amount(), 24)
        self.assertEqual(lottery.total_cost, Decimal('2600.0'))
        self.assertEqual(lottery.ticket_price, Decimal('150.0'))
        self.assertEqual(lottery.min_profit, Decimal('250.0'))
        self.assertEqual(lottery.min_rentability, Decimal('0.1'))
        self.assertEqual(lottery.max_rentability, Decimal('0.38'))
        self.assertEqual(lottery.discount, Decimal('0.05'))

    def test_delete(self):
        response = self.client.post(reverse('lottery-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Lottery.objects.get(name='Lottery').pk
        response = self.client.delete(reverse('lottery-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Lottery.DoesNotExist):
            Lottery.objects.get(name='Lottery')

    def test_get(self):
        response = self.client.post(reverse('lottery-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Lottery.objects.get(name='Lottery').pk
        response = self.client.get(reverse('lottery-detail', args=[pk]))
        data = response.json()
        self.assertEqual(data['name'], 'Lottery')
        self.assertEqual(data['lots'], [
            {"amount": 1, "price": 1000.0},
            {"amount": 2, "price": 500.0},
            {"amount": 3, "price": 200.0}
        ], )
        self.assertEqual(data['write_off'], Decimal('1000.0'))
        self.assertEqual(data['referral_coeff'], 4)
        self.assertEqual(data['ticket_amount'], 24)
        self.assertEqual(data['total_cost'], Decimal('2600.0'))
        self.assertEqual(data['ticket_price'], Decimal('150.0'))
        self.assertEqual(data['min_profit'], Decimal('250.0'))
        self.assertEqual(data['min_rentability'], 0.1)
        self.assertEqual(data['max_rentability'], 0.38)
        self.assertEqual(data['discount'], 0.05)

    def test_put(self):
        self.client.post(reverse('lottery-list'), data=self.data, format='json')
        pk = Lottery.objects.get(name='Lottery').pk
        response = self.client.put(reverse('lottery-detail', args=[pk]),
                                   data=self.other_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lottery = Lottery.objects.get()
        self.assertEqual(lottery.lots(), [
            {"amount": 1, "price": 1000.0},
            {"amount": 2, "price": 500.0},
            {"amount": 3, "price": 200.0}
        ])
        self.assertEqual(lottery.write_off, Decimal('1300.0'))
        self.assertEqual(lottery.referral_coeff, 4)
        self.assertEqual(lottery.ticket_amount(), 30)
        self.assertEqual(lottery.total_cost, Decimal('2600.0'))
        self.assertEqual(lottery.ticket_price, Decimal('130.0'))
        self.assertEqual(lottery.min_profit, Decimal('364.0'))
        self.assertEqual(lottery.min_rentability, Decimal('0.14'))
        self.assertEqual(lottery.max_rentability, Decimal('0.5'))
        self.assertEqual(lottery.discount, Decimal('0.05'))
        self.assertEqual(Ticket.objects.all().count(), 30)

    def test_truncated_name(self):
        data = deepcopy(self.data)
        data1 = deepcopy(self.data)
        data['name'] = '123456789012345'
        lottery = Lottery.from_json(data)
        lottery.save()
        self.assertEqual(lottery.truncated_name(), '123456789012345')
        data1['name'] = '1234567890123456'
        lottery = Lottery.from_json(data1)
        lottery.save()
        self.assertEqual(lottery.truncated_name(), '123456789012...')
