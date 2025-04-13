from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopSettingsViewSet, NotificationSettingsViewSet

router = DefaultRouter()
router.register(r'shop/settings', ShopSettingsViewSet, basename='shop-settings')
router.register(r'notifications/settings', NotificationSettingsViewSet, basename='notification-settings')

urlpatterns = [
    path('', include(router.urls)),
] 