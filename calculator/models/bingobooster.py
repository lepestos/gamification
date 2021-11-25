from django.db import models


class BingoBooster(models.Model):
    name = models.CharField(max_length=127)


class BoosterFix(models.Model):
    amount = models.IntegerField()
    value = models.DecimalField(max_digits=7, decimal_places=2)


class Mission(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=7)
    bingo = models.ForeignKey(BingoBooster, on_delete=models.CASCADE,
                              related_name='booster_items')
