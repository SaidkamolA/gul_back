from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Product, Order, OrderItem
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    OrderCreateSerializer
)
from users.models import User

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        if not request.user.is_admin:  # Используем is_admin вместо is_staff
            return Response(
                {"detail": "You do not have permission to view statistics."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get date range from query params or use defaults
        today = timezone.now()
        
        # Calculate statistics
        total_orders = Order.objects.count()
        # Не учитываем отмененные заказы в общей сумме выручки
        total_revenue = Order.objects.exclude(status='cancelled').aggregate(

            total=Sum('total_price')
        )['total'] or 0
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
        
        # Prepare the response
        response_data = {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'recent_orders': OrderSerializer(recent_orders, many=True).data,
            'order_status_counts': {
                status: Order.objects.filter(status=status).count()
                for status, _ in Order.STATUS_CHOICES
                if status != 'pending'  # Исключаем статус "В ожидании"
            }
        }

        return Response(response_data)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:  # Используем is_admin вместо is_staff
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)

