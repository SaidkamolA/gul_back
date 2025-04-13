from django.urls import path
from .views import ProductViewSet

urlpatterns = [
    path('', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='product-detail'),
    path('statistics/', ProductViewSet.as_view({'get': 'statistics'}), name='product-statistics'),
] 