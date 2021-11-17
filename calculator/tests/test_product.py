from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from calculator.models.product import Product


class ProductTest(APITestCase):
    def tearDown(self):
        Product.objects.all().delete()

    def test_post(self):
        data = {
            'name': 'bicycle',
            'price': 1000
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        p = Product.objects.all()[0]
        self.assertEqual(p.name, 'bicycle')
        self.assertEqual(p.price, 1000)
        Product.objects.all().delete()

    def test_delete(self):
        data = {
            'name': 'product1',
            'price': 999
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Product.objects.get(name='product1').pk
        response = self.client.delete(reverse('product-detail', args = [pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=pk)

    def test_get(self):
        data  = {
            'name': 'product2',
            'price': 902
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pk = Product.objects.get(name='product2').pk
        response = self.client.get(reverse('product-detail', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'product2')
        self.assertEqual(response.json()['price'], 902)

    def test_list(self):
        response = self.client.post(reverse('product-list'), data={
            'name': 'product2',
            'price': 902
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('product-list'), data={
            'name': 'mock',
            'price': 902
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
