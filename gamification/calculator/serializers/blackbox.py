from rest_framework import serializers

from calculator.models import BlackBox, Product


class LotAmountSerializer(serializers.Serializer):
    costly = serializers.IntegerField(min_value=1)
    middle = serializers.IntegerField(min_value=1)
    cheap = serializers.IntegerField(min_value=1)


class LotCostSerializer(serializers.Serializer):
    costly = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    middle = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    cheap = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)

    def validate(self, attrs):
        if not attrs['costly'] >= attrs['middle'] >= attrs['cheap']:
            raise serializers.ValidationError(
                'Не выполняется условие costly > middle > cheap'
            )
        return attrs


class ProductIdsSerializer(serializers.Serializer):
    costly = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    middle = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    cheap = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def validate(self, attrs):
        prices = {cat:product.price for cat, product in attrs.items()}
        if not prices['costly'] > prices['middle'] > prices['cheap']:
            raise serializers.ValidationError(
                'Не выполняется условие costly > middle > cheap'
            )
        return attrs


class BlackBoxSerializer(serializers.ModelSerializer):
    lot_amount = LotAmountSerializer(help_text='{costly: int, middle: int, cheap: int}')
    lot_cost = LotCostSerializer(required=False, help_text='{costly: decimal, middle: decimal, cheap: decimal}')
    product_ids = ProductIdsSerializer(required=False, help_text='{costly: int, middle: int, cheap: int}')

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'lot_cost', 'lot_amount', 'truncated_name',
                  'loyalty', 'rentability', 'max_count_costly', 'id',
                  'product_ids',)
        read_only_fields = ('loyalty', 'rentability',
                            'max_count_costly', 'id', 'truncated_name',)
        write_only_fields = ('product_ids',)

    def validate(self, attrs):
        if ('lot_cost' in attrs) == ('product_ids' in attrs):
            raise serializers.ValidationError(
                'Должно присутствовать ровно одно из двух полей: либо product_ids, либо lot_cost'
            )
        return attrs


class CalculateSerializer(serializers.Serializer):
    lot_cost = LotCostSerializer(help_text='{costly: float, middle: float, cheap: float}')
    costly_amount = serializers.IntegerField(min_value=1)
    rentability = serializers.DecimalField(required=False, min_value=0, max_value=1,
                                           max_digits=3, decimal_places=2,
                                           help_text="Десятичная дробь, не проценты!")
    loyalty = serializers.DecimalField(required=False, min_value=0, max_value=1,
                                       max_digits=3, decimal_places=2,
                                       help_text="Десятичная дробь, не проценты!")
    black_box_cost = serializers.DecimalField(min_value=0, max_digits=7, decimal_places=2)


class MockOpenSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1, help_text='Количество открытий')


class MockOpenUnsavedSerializer(serializers.ModelSerializer):
    lot_cost = LotCostSerializer(help_text='{costly: decimal, middle: decimal, cheap: decimal}')
    lot_amount = LotAmountSerializer(help_text='{costly: int, middle: int, cheap: int}')
    n = serializers.IntegerField(min_value=1, help_text='Количество открытий')

    class Meta:
        model = BlackBox
        fields = ('name', 'price', 'lot_cost', 'lot_amount', 'n')
