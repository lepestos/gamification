from django.db import models

from calculator.models.product import Product
from calculator.utils.blackbox import convert_to_list, convert_to_dict,\
    get_loyalty, get_rentability, LOT_CATEGORIES, open_box_n_times


class BlackBox(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    loyalty = models.DecimalField(max_digits=3, decimal_places=2)
    rentability = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        ordering = ('price',)

    @classmethod
    def from_json(cls, data, instance=None):
        lot_cost = data.get('lot_cost')
        product_ids = data.get('product_ids')
        assert (lot_cost is None) != (product_ids is None)

        if lot_cost is not None:
            products = Product.get_mock_products(convert_to_list(lot_cost))
        else:
            products = [Product.objects.get(pk=pk)
                        for pk in convert_to_list(product_ids)]
            prices = [product.price for product in products]
            lot_cost = convert_to_dict(prices)

        lot_amount = data['lot_amount']
        price = data['price']
        name = data['name']
        loyalty = get_loyalty(lot_amount)
        rentability = get_rentability(lot_amount, lot_cost, price)

        if instance is None:
            instance = BlackBox.objects.create(
                name=name, price=price,
                loyalty=loyalty, rentability=rentability
            )
        else:
            instance = cls.set_properties(
                instance, name=name, price=price,
                loyalty=loyalty, rentability=rentability
            )
            instance.items.all().delete()

        cls.set_products_and_amounts(instance, products,
                                     convert_to_list(lot_amount))
        return instance

    @classmethod
    def set_properties(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def set_products_and_amounts(cls, instance, products, amounts):
        for product, amount in zip(products, amounts):
            item = BlackBoxItem.objects.create(product=product,
                                               black_box=instance, amount=amount)
            item.save()

    def __str__(self):
        return f'Box({self.name}, {self.price}, {self.loyalty}, {self.rentability})'

    def truncated_name(self):
        if len(self.name) <= 15:
            return self.name
        return self.name[:12] + '...'

    def products(self):
        return [item.product for item in self.sorted_items()]

    def probabilities(self):
        return [item.probability for item in self.sorted_items()]

    def sorted_items(self):
        return sorted(list(self.items.all()),
                      key=lambda item: item.product.price, reverse=True)

    def get_category_mapping(self):
        return {key:value for key, value in zip(self.products(), LOT_CATEGORIES)}

    def amounts(self):
        return [item.amount for item in self.sorted_items()]

    def costs(self):
        return [item.product.price for item in self.sorted_items()]

    def lot_amount(self):
        amounts = [item.amount for item in self.sorted_items()]
        return {key:value for key, value in zip(LOT_CATEGORIES, amounts)}

    def lot_cost(self):
        costs = [item.product.price for item in self.sorted_items()]
        return {key:value for key, value in zip(LOT_CATEGORIES, costs)}

    def max_count_costly(self):
        return self.sorted_items()[0].amount

    def mock_open(self, n):
        """get an item from the box n times"""
        return open_box_n_times(n, self.amounts(), self.costs(), self.price)


class BlackBoxItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='items')
    black_box = models.ForeignKey(BlackBox, on_delete=models.CASCADE,
                                  related_name='items')
    amount = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} in {self.black_box.name}'
