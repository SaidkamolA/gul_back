from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShopSettings, NotificationSettings
from .serializers import ShopSettingsSerializer, NotificationSettingsSerializer

class ShopSettingsViewSet(viewsets.ModelViewSet):
    queryset = ShopSettings.objects.all()
    serializer_class = ShopSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        # Возвращаем первый объект настроек или создаем новый
        obj, created = ShopSettings.objects.get_or_create(pk=1)
        return obj

    def perform_update(self, serializer):
        serializer.save()

class NotificationSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificationSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        settings, created = NotificationSettings.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(settings)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data) 