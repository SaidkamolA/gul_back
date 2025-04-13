from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path('', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('<int:pk>/', OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='order-detail'),
    path('statistics/', OrderViewSet.as_view({'get': 'statistics'}), name='order-statistics'),
] 