from rest_framework import serializers
from app.models import User, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = Product
        # List of fields to pass to the serializer
        fields = ['id', 'name', 'price', 'description', 'image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = User
        # List of fields to pass to the serializer
        fields = ['id', 'username', 'is_active', 'is_admin']