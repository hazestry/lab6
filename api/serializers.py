from rest_framework import serializers
from .models import Client, Car, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone', 'address']

class CarSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'owner', 'make', 'model', 'year']

class OrderSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'car', 'description', 'date_created', 'price', 'status']
