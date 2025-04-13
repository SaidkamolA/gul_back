from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, UserProfileView

urlpatterns = [
    # Authentication
    path('login/', TokenObtainPairView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user_register'),

    # User management
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_list'),
    path('users/<int:pk>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='user_detail'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('users/statistics/', UserViewSet.as_view({'get': 'statistics'}), name='user-statistics'),
    path('users/change-password/', UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
]