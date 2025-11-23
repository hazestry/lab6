from rest_framework import serializers
from .models import Client, Car, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cars_count = serializers.IntegerField(source='cars.count', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone', 'address', 'cars_count']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CarSerializer(serializers.ModelSerializer):
    owner = ClientSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), 
        source='owner', 
        write_only=True
    )
    orders_count = serializers.IntegerField(source='orders.count', read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'owner', 'owner_id', 'make', 'model', 'year', 'orders_count']
        read_only_fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), 
        source='car', 
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'car', 'car_id', 'description', 'date_created', 'price', 'status']
        read_only_fields = ['id', 'date_created']