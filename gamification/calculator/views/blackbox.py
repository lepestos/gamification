from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from calculator.utils.blackbox import BlackBoxUtil
from calculator.models import BlackBox
from calculator.serializers.blackbox import BlackBoxSerializer,\
    CalculateSerializer, MockOpenSerializer, MockOpenUnsavedSerializer


class BlackBoxViewSet(viewsets.ModelViewSet):
    serializer_class = BlackBoxSerializer
    queryset = BlackBox.objects.all()

    def get_serializer_class(self):
        if self.action == 'calculate':
            return CalculateSerializer
        if self.action == 'mock_open':
            return MockOpenSerializer
        if self.action == 'mock_open_unsaved':
            return MockOpenUnsavedSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        box = BlackBox.from_json(serializer.data)
        box.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        data = serializer.validated_data
        box = BlackBox.from_json(data, instance=instance)
        box.save()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            box = BlackBoxUtil(**serializer.data)
            data = box.to_json()
            if data['success']:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

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
