from random import sample
from collections import defaultdict
from .utils.blackbox import get_loyalty, get_rentability, open_box_n_times, \
    convert_to_list, convert_to_dict, LOT_CATEGORIES

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=127)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name


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
            products = cls.get_mock_products(lot_cost)
        else:
            products = [Product.objects.get(pk=pk) for pk in convert_to_list(product_ids)]
            prices = [product.price for product in products]
            lot_cost = convert_to_dict(prices)

        lot_amount = data['lot_amount']
        price = data['price']
        name = data['name']
        loyalty = get_loyalty(lot_amount)
        rentability = get_rentability(lot_amount, lot_cost, price)

        if instance is None:
            instance = BlackBox.objects.create(name=name, price=price,
                                               loyalty=loyalty, rentability=rentability)
        else:
            instance = cls.set_properties(instance, name=name, price=price,
                                          loyalty=loyalty, rentability=rentability)
            instance.items.all().delete()

        cls.set_products_and_amounts(instance, products, convert_to_list(lot_amount))
        return instance

    @staticmethod
    def get_mock_products(lot_cost):
        products = [Product.objects.create(name='mock', price=cost)
                    for cost in convert_to_list(lot_cost)]
        for product in products:
            product.save()
        return products

    @classmethod
    def set_properties(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def set_products_and_amounts(cls, instance, products, amounts):
        for product, amount in zip(products, amounts):
            item = BlackBoxItem.objects.create(product=product, black_box=instance, amount=amount)
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


class Lottery(models.Model):
    name = models.CharField(max_length=127)
    write_off = models.DecimalField(decimal_places=2, max_digits=7)
    referral_coeff = models.PositiveIntegerField(blank=True, null=True)
    ticket_price = models.DecimalField(decimal_places=2, max_digits=7)
    min_profit = models.DecimalField(decimal_places=2, max_digits=7)
    min_rentability = models.DecimalField(decimal_places=2, max_digits=3)
    max_rentability = models.DecimalField(decimal_places=2, max_digits=3)
    total_cost = models.DecimalField(decimal_places=2, max_digits=7)
    discount = models.DecimalField(decimal_places=2, max_digits=3)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

    def products(self):
        return [lottery_item.product for lottery_item in self.lottery_items.all()]

    def ticket_amount(self):
        return self.lottery_items.all().count()

    @staticmethod
    def lucky_numbers(data):
        amounts = [lot['amount'] for lot in data.get('lots')]
        numbers = sample(range(data['ticket_amount']), sum(amounts))
        return numbers

    @classmethod
    def from_json(cls, data, instance=None):
        name = data['name']
        write_off = data['write_off']
        referral_coeff = data.get('referral_coeff')
        discount = data.get('discount')
        ticket_price = data['ticket_price']
        max_rentability = data['max_rentability']
        min_rentability = data['min_rentability']
        min_profit = data['min_profit']
        total_cost = data['total_cost']

        lots = data.get('lots')
        products = cls.get_mock_products(lots)
        numbers = cls.lucky_numbers(data)

        if instance is None:
            instance = Lottery.objects.create(name=name, write_off=write_off,referral_coeff=referral_coeff,
                                              ticket_price=ticket_price, min_profit=min_profit,
                                              min_rentability=min_rentability, max_rentability=max_rentability,
                                              total_cost=total_cost, discount=discount)
        else:
            instance = cls.set_properties(instance, name=name, write_off=write_off, referral_coeff=referral_coeff,
                                          ticket_price=ticket_price, min_profit=min_profit,
                                          min_rentability=min_rentability, max_rentability=max_rentability,
                                          total_cost=total_cost, discount=discount)
            instance.lottery_items.all().delete()

        cls.set_tickets(instance, data, products, numbers)
        return instance

    @staticmethod
    def get_mock_products(lots):
        products = [Product.objects.create(name='mock', price=lot['price'])
                    for lot in lots]
        for product in products:
            product.save()
        return products

    @classmethod
    def set_tickets(cls, instance, data, products, numbers):
        tickets = [Ticket.objects.create(product=None, lottery=instance, number=i)
                   for i in range(data['ticket_amount'])]
        lots = data['lots']
        products_for_amount = []
        for product, lot in zip(products, lots):
            products_for_amount.extend([product] * lot['amount'])
        for product, number in zip(products_for_amount, numbers):
            tickets[number].product = product
        for ticket in tickets:
            ticket.save()
        return tickets

    @classmethod
    def set_properties(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def lots(self):
        counter = defaultdict(int)
        for ticket in self.lottery_items.all():
            if ticket.product:
                product = ticket.product
                counter[(product.id, product.price)] += 1
        products = []
        for id_price, amount in counter.items():
            id_, price = id_price
            products.append({'amount': amount, 'price': price})
        return sorted(products, key=lambda x: x['price'], reverse=True)


class Ticket(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE,
                                related_name='lottery_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='lottery_items', blank=True, null=True)
    number = models.PositiveIntegerField()
