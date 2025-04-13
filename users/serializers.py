from django.contrib.auth import authenticate
from requests import Response
from rest_framework.exceptions import ValidationError

from rest_framework import serializers
from django.utils import timezone
import random

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'password',
            'first_name', 
            'last_name',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superuser',
            'date_joined',
            'last_login'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True}
        }

    def create(self, validated_data):
        if 'password' not in validated_data:
            raise serializers.ValidationError({"password": "This field is required for registration."})
            
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False),
            is_admin=validated_data.get('is_admin', False),
            is_superuser=validated_data.get('is_superuser', False)
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def validate(self, data):
        if self.instance is None and 'password' not in data:
            raise serializers.ValidationError({"password": "This field is required for new users."})
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_admin']
        read_only_fields = ['is_admin', 'username']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']