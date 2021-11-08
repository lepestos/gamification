from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from calculator.utils.lottery import LotteryUtil
from calculator.models import Lottery
from calculator.serializers.lottery import LotterySerializer, CalculateSerializer


class LotteryViewSet(viewsets.ModelViewSet):
    serializer_class = LotterySerializer
    queryset = Lottery.objects.all()

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        lottery = Lottery.from_json(serializer.data)
        lottery.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        data = serializer.validated_data
        lottery = Lottery.from_json(data, instance=instance)
        lottery.save()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lottery = LotteryUtil(**serializer.data)
            data = lottery.to_json()
            if data['success']:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
