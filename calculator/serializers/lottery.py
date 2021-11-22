from rest_framework import serializers

from calculator.models.lottery import Lottery


class LotSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class LotterySerializer(serializers.ModelSerializer):
    lots = LotSerializer(many=True)
    ticket_amount = serializers.IntegerField(min_value=0)

    class Meta:
        model = Lottery
        fields = ('name', 'lots', 'write_off', 'referral_coeff', 'ticket_amount',
                  'total_cost', 'ticket_price', 'min_profit',
                  'min_rentability', 'max_rentability', 'discount', 'truncated_name', 'id',)
        read_only_fields = ('truncated_name',)


class CalculateSerializer(serializers.Serializer):
    lots = LotSerializer(many=True)
    write_off = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    referral_coeff = serializers.IntegerField(required=False)
    ticket_amount = serializers.IntegerField(min_value=0)
    ticket_price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    discount = serializers.DecimalField(max_digits=3, decimal_places=2,
                                        min_value=0, max_value=1, required=False)
