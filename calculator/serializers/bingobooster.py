from rest_framework import serializers


class CalculateSerializer(serializers.Serializer):
    prices = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                  max_digits=12, decimal_places=2))
    booster_amount = serializers.IntegerField(min_value=0)
    fix_amount = serializers.IntegerField(min_value=0)
    budget = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    participants = serializers.IntegerField(min_value=0)
