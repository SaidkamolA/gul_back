from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Sum, F
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Добавляем информацию о пользователе
        if request.user.is_authenticated:
            data['user'] = request.user.id
            if not data.get('email'):
                data['email'] = request.user.email

        # Проверяем обязательные поля
        if not data.get('items'):
            return Response(
                {'error': 'Необходимо указать товары'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем заказ
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Добавляем товары в заказ
        total_amount = 0
        for item in data['items']:
            order_item = OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            total_amount += order_item.price * order_item.quantity

        # Обновляем общую сумму заказа
        order.total_amount = total_amount
        order.save()

        return Response(
            self.get_serializer(order).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """
        Get order statistics. Only accessible by admin users.
        Returns:
        - Total number of orders
        - Total sum of all orders
        - Orders by status
        - Recent orders (last 30 days)
        - Recent orders sum (last 30 days)
        """
        total_orders = self.queryset.count()
        
        # Total sum of all orders
        total_sum = self.queryset.aggregate(
            total_sum=Sum('total_amount')
        )['total_sum'] or 0
        
        # Orders by status
        orders_by_status = self.queryset.values('status').annotate(
            count=Count('id'),
            total_sum=Sum('total_amount')
        )
        
        # Recent orders (last 30 days)
        last_30_days = timezone.now() - timedelta(days=30)
        recent_orders = self.queryset.filter(
            created_at__gte=last_30_days
        ).count()
        
        recent_orders_sum = self.queryset.filter(
            created_at__gte=last_30_days
        ).aggregate(
            total_sum=Sum('total_amount')
        )['total_sum'] or 0

        return Response({
            'total_orders': total_orders,
            'total_sum': total_sum,
            'orders_by_status': orders_by_status,
            'recent_orders': recent_orders,
            'recent_orders_sum': recent_orders_sum
        }) 