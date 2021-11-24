from .mixins import CalculateViewSet

from calculator.utils.bingo import DiscountBingoUtil
from calculator.models.bingodiscount import BingoDiscount
from calculator.serializers.bingodiscount import BingoSerializer, CalculateSerializer
from calculator.serializers.bingodiscount import CalculateSerializer


class BingoViewSet(CalculateViewSet):
    serializer_class = BingoSerializer
    queryset = BingoDiscount.objects.all()
    model_class = BingoDiscount
    util_class = DiscountBingoUtil

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        return super().get_serializer_class()

