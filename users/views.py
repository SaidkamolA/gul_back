import random

from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from users.models import User
from users.serializers import UserProfileSerializer, UserSerializer


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'is_active': True,
            'is_staff': False,
            'is_admin': False,
            'is_superuser': False
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        # Only admins can create users through admin panel
        if not request.user.is_authenticated or not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can create users."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            self.get_serializer(user).data,
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        # Only admins can list all users
        if not request.user.is_authenticated or not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can view all users."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        # Users can only retrieve their own data unless they're admin
        if request.user.id != user.id and not request.user.is_admin:
            return Response(
                {"detail": "You do not have permission to view this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Only admins can update other users
        if request.user.id != instance.id and not request.user.is_admin:
            return Response(
                {"detail": "You do not have permission to update this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Only admins can update admin-only fields
        if not request.user.is_admin:
            admin_fields = ['is_active', 'is_staff', 'is_admin', 'is_superuser']
            for field in admin_fields:
                request.data.pop(field, None)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        # Only admins can delete users
        if not request.user.is_admin:
            return Response(
                {"detail": "Only administrators can delete users."},
                status=status.HTTP_403_FORBIDDEN
            )
        user.delete()
        return Response(status=204)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """
        Get user statistics. Only accessible by admin users.
        Returns:
        - Total number of users
        - Number of users registered in the last 24 hours
        - Number of users registered in the last 7 days
        - Number of users registered in the last 30 days
        """
        total_users = User.objects.count()
        now = timezone.now()
        
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        
        users_24h = User.objects.filter(date_joined__gte=last_24h).count()
        users_7d = User.objects.filter(date_joined__gte=last_7d).count()
        users_30d = User.objects.filter(date_joined__gte=last_30d).count()

        return Response({
            'total_users': total_users,
            'users_last_24h': users_24h,
            'users_last_7d': users_7d,
            'users_last_30d': users_30d
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Change user password.
        """
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {'error': 'Current password and new password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'message': 'Password changed successfully'},
            status=status.HTTP_200_OK
        )