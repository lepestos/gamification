from .mixins import CalculateViewSet

from calculator.utils.bingo import DiscountBingoUtil, BoosterBingoUtil
from calculator.models.bingodiscount import BingoDiscount
from calculator.serializers.bingodiscount import BingoSerializer, CalculateSerializer
from calculator.serializers.bingobooster import CalculateBoosterSerializer, BoosterSerializer
from calculator.models.bingobooster import BingoBooster


class BingoViewSet(CalculateViewSet):
    serializer_class = BingoSerializer
    queryset = BingoDiscount.objects.all()
    model_class = BingoDiscount
    util_class = DiscountBingoUtil

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        return super().get_serializer_class()


class BoosterViewSet(CalculateViewSet):
    serializer_class = BoosterSerializer
    queryset = BingoBooster.objects.all()
    model_class = BingoBooster
    util_class = BoosterBingoUtil

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateBoosterSerializer
        return super().get_serializer_class()

