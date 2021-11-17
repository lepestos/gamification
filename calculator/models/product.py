from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def get_mock_products(cls, costs):
        products = [cls.objects.create(name='mock', price=price)
                    for price in costs]
        for product in products:
            product.save()
        return products

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name
