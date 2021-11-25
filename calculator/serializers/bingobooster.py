from rest_framework import serializers
from calculator.models.bingobooster import BingoBooster

class BoosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BingoBooster
        fields = ('name',)


class CalculateBoosterSerializer(serializers.Serializer):
    prices = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                  max_digits=12, decimal_places=2))
    booster_amount = serializers.IntegerField(min_value=0)
    fix_amount = serializers.IntegerField(min_value=0)
    budget = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    participants = serializers.IntegerField(min_value=0)
    abs_budget_distribution = serializers.ListSerializer(
        child=serializers.DecimalField(decimal_places=2, max_digits=7),
        allow_null=True)
