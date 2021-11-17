from copy import deepcopy
from decimal import Decimal

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models.blackbox import BlackBox, BlackBoxItem
from calculator.models.product import Product
from calculator.utils.blackbox import convert_to_list, convert_to_dict


class BlackBoxTest(APITestCase):
    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        super().tearDownClass()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            'name': 'Box',
            'price': 200,
            'lot_cost': {'costly': 1000, 'middle': 100, 'cheap': 10},
            'lot_amount': {'costly': 1, 'middle': 3, 'cheap': 6},
        }
        cls.other_data = {
            'name': 'Box',
            'price': 40,
            'lot_cost': {'costly': 100, 'middle': 10, 'cheap': 1},
            'lot_amount': {'costly': 2, 'middle': 3, 'cheap': 5},
        }
        cls.products = [Product.objects.create(name=name, price=price)
                        for name, price in zip(['pr1', 'pr2', 'pr3'], [1000, 100, 10])]
        for product in cls.products:
            product.save()

    def tearDown(self):
        BlackBox.objects.all().delete()
        BlackBoxItem.objects.all().delete()

    def test_post(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bb = BlackBox.objects.get(name='Box')
        self.assertEqual(convert_to_list(bb.lot_cost()), [1000, 100, 10])
        self.assertEqual(convert_to_list(bb.lot_amount()), [1, 3, 6])
        self.assertEqual(bb.price, 200)
        self.assertEqual(bb.loyalty, Decimal('0.4'))
        self.assertEqual(bb.rentability, Decimal('0.47'))

    def test_delete(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.delete(reverse('blackbox-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(BlackBox.DoesNotExist):
            BlackBox.objects.get(name='Box')

    def test_get(self):
        response = self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.get(reverse('blackbox-detail', args=[pk]))
        data = response.json()
        self.assertEqual(data['name'], 'Box')
        self.assertEqual(data['price'], 200)
        self.assertEqual(data['lot_cost'], {'costly': 1000, 'middle': 100, 'cheap': 10})
        self.assertEqual(data['lot_amount'], {'costly': 1, 'middle': 3, 'cheap': 6})
        self.assertEqual(data['loyalty'], 0.4)
        self.assertEqual(data['rentability'], 0.47)
        self.assertEqual(data['max_count_costly'], 1)
        self.assertEqual(data['truncated_name'], 'Box')

    def test_put(self):
        self.client.post(reverse('blackbox-list'), data=self.data, format='json')
        pk = BlackBox.objects.get(name='Box').pk
        response = self.client.put(reverse('blackbox-detail', args=[pk]),
                                   data=self.other_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bb = BlackBox.objects.get(pk=pk)
        self.assertEqual(convert_to_list(bb.lot_cost()), [100, 10, 1])
        self.assertEqual(convert_to_list(bb.lot_amount()), [2, 3, 5])
        self.assertEqual(bb.price, 40)
        self.assertEqual(bb.loyalty, Decimal('0.5'))
        self.assertEqual(bb.rentability, Decimal('0.70'))
        self.assertEqual(BlackBoxItem.objects.all().count(), 3)

    def test_post_validation(self):
        data = deepcopy(self.data)
        data['lot_cost']['costly'] = 50
        response = self.client.post(reverse('blackbox-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_message = response.json()['lot_cost']['non_field_errors'][0]
        self.assertEqual(resp_message, 'Не выполняется условие costly > middle > cheap')

    def test_post_with_product_ids(self):
        product_ids = convert_to_dict([product.id for product in self.products])
        data = deepcopy(self.data)
        del data['lot_cost']
        data['product_ids'] = product_ids
        response = self.client.post(reverse('blackbox-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        bb = BlackBox.objects.get(name='Box')
        self.assertEqual(convert_to_list(bb.lot_cost()), [1000, 100, 10])
        self.assertEqual(convert_to_list(bb.lot_amount()), [1, 3, 6])
        self.assertEqual(bb.price, 200)
        self.assertEqual(bb.loyalty, Decimal('0.4'))
        self.assertEqual(bb.rentability, Decimal('0.47'))

    def test_post_validation_with_product_ids(self):
        product_ids = convert_to_dict([product.id for product in self.products[::-1]])
        data = deepcopy(self.data)
        del data['lot_cost']
        data['product_ids'] = product_ids
        response = self.client.post(reverse('blackbox-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_message = response.json()['product_ids']['non_field_errors'][0]
        self.assertEqual(resp_message, 'Не выполняется условие costly > middle > cheap')

    def test_post_either_product_ids_or_lot_cost(self):
        err_message = 'Должно присутствовать ровно одно из двух полей: либо product_ids, либо lot_cost'
        product_ids = convert_to_dict([product.id for product in self.products])
        data = deepcopy(self.data)
        data['product_ids'] = product_ids
        response = self.client.post(reverse('blackbox-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp_message= response.json()['non_field_errors'][0]
        self.assertEqual(resp_message, err_message)

    def test_truncated_name(self):
        data = deepcopy(self.data)
        data['name'] = '123456789012345'
        bb = BlackBox.from_json(data)
        bb.save()
        self.assertEqual(bb.truncated_name(), '123456789012345')
        data['name'] = '1234567890123456'
        bb = BlackBox.from_json(data)
        bb.save()
        self.assertEqual(bb.truncated_name(), '123456789012...')
