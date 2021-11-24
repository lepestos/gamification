from collections import defaultdict
from random import sample

from django.db import models

from calculator.models.product import Product


class Lottery(models.Model):
    name = models.CharField(max_length=127)
    write_off = models.DecimalField(decimal_places=2, max_digits=12)
    referral_coeff = models.PositiveIntegerField(blank=True, null=True)
    ticket_price = models.DecimalField(decimal_places=2, max_digits=12)
    min_profit = models.DecimalField(decimal_places=2, max_digits=12)
    min_rentability = models.DecimalField(decimal_places=2, max_digits=3)
    max_rentability = models.DecimalField(decimal_places=2, max_digits=3)
    total_cost = models.DecimalField(decimal_places=2, max_digits=12)
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
        numbers = cls.lucky_numbers(data)
        lots = data.pop('lots')
        ticket_amount = data.pop('ticket_amount')
        products = Product.get_mock_products([lot['price'] for lot in lots])
        if instance is None:
            instance = Lottery.objects.create(**data)
        else:
            instance = cls.set_properties(instance, **data)
            instance.lottery_items.all().delete()

        cls.set_tickets(instance, ticket_amount, lots, products, numbers)
        return instance

    @classmethod
    def set_tickets(cls, instance, ticket_amount, lots, products, numbers):
        tickets = [Ticket.objects.create(product=None, lottery=instance, number=i)
                   for i in range(ticket_amount)]
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

    def truncated_name(self):
        if len(self.name) <= 15:
            return self.name
        return self.name[:12] + '...'


class Ticket(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE,
                                related_name='lottery_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='lottery_items',
                                blank=True, null=True)
    number = models.PositiveIntegerField()
