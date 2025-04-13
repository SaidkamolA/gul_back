from django.contrib import admin
from .models import ShopSettings, NotificationSettings

@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'delivery_radius', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('Работа магазина', {
            'fields': ('working_hours', 'delivery_radius')
        }),
        ('Логотип', {
            'fields': ('logo',)
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'sms_notifications', 'telegram_notifications', 'created_at')
    list_filter = ('email_notifications', 'sms_notifications', 'telegram_notifications', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Настройки уведомлений', {
            'fields': ('email_notifications', 'sms_notifications', 'telegram_notifications')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ) 