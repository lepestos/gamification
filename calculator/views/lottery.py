from .mixins import CalculateViewSet

from calculator.utils.lottery import LotteryUtil
from calculator.models.lottery import Lottery
from calculator.serializers.lottery import LotterySerializer, CalculateSerializer


class LotteryViewSet(CalculateViewSet):
    serializer_class = LotterySerializer
    queryset = Lottery.objects.all()
    model_class = Lottery
    util_class = LotteryUtil

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        return super().get_serializer_class()
