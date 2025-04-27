import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gulqand.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "gulqand"
password = "1844784s"
email = "gulqand@example.com"

if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=True,
        is_staff=True,
        is_superuser=True
    )
    # Если есть поле is_admin, тоже выставим
    if hasattr(user, 'is_admin'):
        user.is_admin = True
        user.save()
    print("Admin user created!")
else:
    user = User.objects.get(username=username)
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    if hasattr(user, 'is_admin'):
        user.is_admin = True
    user.set_password(password)
    user.save()
    print("Admin user updated!")