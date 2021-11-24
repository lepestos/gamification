from django.db import models


class BingoDiscount(models.Model):
    name = models.CharField(max_length=127)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    expected_budget = models.DecimalField(max_digits=12, decimal_places=2)
    total_participants = models.PositiveIntegerField()
    unlucky_participants = models.IntegerField()
    lucky_participants = models.IntegerField()
    usage_probability = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    @classmethod
    def from_json(cls, data, instance=None):
        prices = data.pop('prices')
        discounts = data.pop('discounts')
        budget_distribution = data.pop('budget_distribution')
        participants_per_lot = data.pop('participants_per_lot')
        amounts = data.pop('amounts')
        if instance is None:
            instance = BingoDiscount.objects.create(**data)
        else:
            instance = cls.set_properties(instance, **data)
            instance.lottery_items.all().delete()

        cls.set_discount_products(prices, budget_distribution, participants_per_lot,
                                  amounts, discounts, instance)

        return instance

    @staticmethod
    def get_discounts(discounts):
        discounts = [Discount.objects.create(value=discount) for discount in discounts]
        for discount in discounts:
            discount.save()
        return discounts

    @staticmethod
    def get_lots(prices, budget_distribution, participants_per_lot):
        lots = [Lot.objects.create(price=price, budget_in_percents=budget_in_percents,
                                   participants=participants)
                for price, budget_in_percents, participants
                in zip(prices, budget_distribution, participants_per_lot)]
        for lot in lots:
            lot.save()
        return lots

    @classmethod
    def set_discount_products(cls, prices, budget_distribution, participants_per_lot, amounts, discounts, instance):
        lots = cls.get_lots(prices, budget_distribution, participants_per_lot)
        discounts = cls.get_discounts(discounts)
        for row, lot in zip(amounts, lots):
            for amount, discount in zip(row, discounts):
                discount_product = DiscountProduct.objects.create(discount=discount,
                                                                  lot=lot, amount=amount,
                                                                  bingo=instance)
                discount_product.save()

    @classmethod
    def set_properties(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def budget_distribution(self):
        return [bingo.lot.budget_in_percents for bingo in self.bingo_items.all()]

    def participants_per_lot(self):
        return [bingo.lot.participants for bingo in self.bingo_items.all()]

    def prices(self):
        return [bingo.lot.price for bingo in self.bingo_items.all()]

    def discounts(self):
        return [bingo.discount.value for bingo in self.bingo_items.all()]

    def amounts(self):
        prices = self.prices()
        amounts = []
        amount = []
        for bingo in self.bingo_items.all():
            for price in prices:
                amount = []
                if bingo.lot.price == price:
                    amount.append(bingo.amount)
            amounts.append(amount)


class Discount(models.Model):
    value = models.DecimalField(max_digits=3, decimal_places=2)


class DiscountProduct(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE,
                                 related_name='bingo_items')
    lot = models.ForeignKey("Lot", on_delete=models.CASCADE,
                            related_name='bingo_items')
    bingo = models.ForeignKey(BingoDiscount, on_delete=models.CASCADE,
                              related_name='bingo_items')
    amount = models.IntegerField()


class Lot(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=12)
    budget_in_percents = models.DecimalField(decimal_places=2, max_digits=3)
    participants = models.IntegerField()
