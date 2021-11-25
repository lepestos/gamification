from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class CalculateViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        instance = self.model_class.from_json(serializer.data)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        data = serializer.validated_data
        instance = self.model_class.from_json(data, instance=instance)
        instance.save()

    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            util_instance = self.util_class(**serializer.data)
            data = util_instance.to_json()
            if data['success']:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
