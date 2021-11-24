from rest_framework import serializers

from calculator.models.bingodiscount import BingoDiscount


class Matrix(serializers.ListField):
    child = serializers.IntegerField(min_value=0)


class BingoSerializer(serializers.ModelSerializer):
    prices = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                  max_digits=12, decimal_places=2))
    discounts = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                     max_digits=3, decimal_places=2))
    budget_distribution = serializers.ListSerializer(child=serializers.DecimalField(max_digits=12,
                                                                                    decimal_places=2))
    participants_per_lot = serializers.ListSerializer(child=serializers.DecimalField(max_digits=12,
                                                                                     decimal_places=2))
    amounts = serializers.ListSerializer(child=Matrix())

    class Meta:
        model = BingoDiscount
        fields = ('name', 'prices', 'discounts', 'budget', 'budget_distribution',
                  'expected_budget', 'participants_per_lot',
                  'total_participants', 'unlucky_participants',
                  'lucky_participants', 'usage_probability',
                  'amounts', 'id', )
        read_only_fields = ('id',)


class CalculateSerializer(serializers.Serializer):
    prices = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                  max_digits=12, decimal_places=2))
    discounts = serializers.ListField(child=serializers.DecimalField(min_value=0,
                                                                     max_digits=3, decimal_places=2))
    budget = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    lucky_participants = serializers.IntegerField(min_value=0)
    usage_probability = serializers.DecimalField(max_digits=3, decimal_places=2)
    unlucky_participants = serializers.DecimalField(allow_null=True, max_digits=3, decimal_places=2)
    budget_distribution = serializers.ListSerializer(child=serializers.DecimalField(max_digits=12,
                                                                                    decimal_places=2),
                                                     allow_null=True)
