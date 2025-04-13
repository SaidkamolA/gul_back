from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    is_admin = models.BooleanField(default=False, verbose_name='Admin Access')
    is_staff = models.BooleanField(default=False, verbose_name='Staff status')
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser status')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username