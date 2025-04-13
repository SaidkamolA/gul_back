from django.db import models
from django.conf import settings

class ShopSettings(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название магазина')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    working_hours = models.CharField(max_length=255, verbose_name='Часы работы')
    delivery_radius = models.IntegerField(verbose_name='Радиус доставки (км)')
    logo = models.ImageField(upload_to='shop_logos/', null=True, blank=True, verbose_name='Логотип')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Настройки магазина'
        verbose_name_plural = 'Настройки магазина'

    def __str__(self):
        return self.name

class NotificationSettings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_settings')
    email_notifications = models.BooleanField(default=True, verbose_name='Email уведомления')
    sms_notifications = models.BooleanField(default=False, verbose_name='SMS уведомления')
    telegram_notifications = models.BooleanField(default=False, verbose_name='Telegram уведомления')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Настройки уведомлений'
        verbose_name_plural = 'Настройки уведомлений'

    def __str__(self):
        return f'Настройки уведомлений для {self.user.username}' 