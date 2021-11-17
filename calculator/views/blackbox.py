from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from calculator.utils.blackbox import BlackBoxUtil
from calculator.models.blackbox import BlackBox
from calculator.serializers.blackbox import BlackBoxSerializer,\
    CalculateSerializer, MockOpenSerializer, MockOpenUnsavedSerializer
from .mixins import CalculateViewSet


class BlackBoxViewSet(CalculateViewSet):
    serializer_class = BlackBoxSerializer
    queryset = BlackBox.objects.all()
    model_class = BlackBox
    util_class = BlackBoxUtil

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        if self.action == 'mock_open':
            return MockOpenSerializer
        if self.action == 'mock_open_unsaved':
            return MockOpenUnsavedSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def mock_open(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bb = BlackBox.objects.get(pk=pk)
            product_categories = bb.mock_open(serializer.data.get('n'))
            data = {'product_categories': product_categories}
            return Response(data)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def mock_open_unsaved(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bb = BlackBox.from_json(serializer.data)
            bb.save()
            product_categories = bb.mock_open(serializer.data.get('n'))
            data = {'product_categories': product_categories}
            bb.delete()
            return Response(data)
