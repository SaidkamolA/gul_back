# gul/models.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.models import User  # Импортируем кастомную модель пользователя

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255, verbose_name='Product Name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Product Image')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def is_available(self):
        return self.status == 'active'

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()
            return True
        return False

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='User')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Price')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    address = models.TextField(verbose_name='Delivery Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def calculate_total_price(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_price = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.calculate_total_price()
