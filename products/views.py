from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Sum, F
from django.utils import timezone
from datetime import timedelta

class ProductViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """
        Get product statistics. Only accessible by admin users.
        Returns:
        - Total number of products
        - Total number of products by category
        - Total number of products by status
        - Total number of products added in the last 30 days
        - Total sum of all products
        - Total sum by category
        - Total sum of recent products (last 30 days)
        """
        total_products = self.queryset.count()
        
        # Products by category
        products_by_category = self.queryset.values('category__name').annotate(
            count=Count('id'),
            total_sum=Sum('price')
        )
        
        # Products by status
        products_by_status = self.queryset.values('status').annotate(
            count=Count('id'),
            total_sum=Sum('price')
        )
        
        # Products added in last 30 days
        last_30_days = timezone.now() - timedelta(days=30)
        recent_products = self.queryset.filter(
            created_at__gte=last_30_days
        ).count()

        # Total sum calculations
        total_sum = self.queryset.aggregate(total_sum=Sum('price'))['total_sum'] or 0
        recent_products_sum = self.queryset.filter(
            created_at__gte=last_30_days
        ).aggregate(total_sum=Sum('price'))['total_sum'] or 0

        return Response({
            'total_products': total_products,
            'total_sum': total_sum,
            'products_by_category': products_by_category,
            'products_by_status': products_by_status,
            'recent_products': recent_products,
            'recent_products_sum': recent_products_sum
        }) 