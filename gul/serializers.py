from rest_framework import serializers
from .models import Order, Product, OrderItem
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']
        read_only_fields = ['is_admin']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_status(self, value):
        if value not in dict(Product.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status value")
        return value

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if image:
            product.image = image
            product.save()
        return product

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if image:
            instance.image = image
        instance.save()
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
        read_only_fields = ['price']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['items', 'status', 'phone', 'address']
        read_only_fields = ['status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total price first
        total_price = 0
        for item_data in items_data:
            product = item_data['product']
            total_price += product.price * item_data['quantity']
        
        # Create order with total_price
        order = Order.objects.create(
            total_price=total_price,
            user=self.context['request'].user,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
        
        return order

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'total_price']