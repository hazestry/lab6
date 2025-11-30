from rest_framework import serializers
from .models import Client, Car, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


# сериализаторы для чтения 
class ClientDetailSerializer(serializers.ModelSerializer):
    # о клиенте
    user = UserSerializer()
    cars_count = serializers.IntegerField(source='cars.count', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone', 'address', 'cars_count']
        read_only_fields = ['id']


class CarDetailSerializer(serializers.ModelSerializer):
    # о машине
    owner = ClientDetailSerializer(read_only=True)
    orders_count = serializers.IntegerField(source='orders.count', read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'owner', 'make', 'model', 'year', 'orders_count']
        read_only_fields = ['id']


class OrderDetailSerializer(serializers.ModelSerializer):
    # о заказе
    car = CarDetailSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'car', 'description', 'date_created', 'price', 'status']
        read_only_fields = ['id', 'date_created']


# сериализаторы для записи
class ClientSerializer(serializers.ModelSerializer):
    # запись / изменение клиента
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user', 'phone', 'address']
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

    def to_representation(self, instance):
        #сериализатор для отображения
        return ClientDetailSerializer(instance, context=self.context).data


class CarSerializer(serializers.ModelSerializer):
    # запись / изменение машины
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), 
        source='owner',
        help_text="ID владельца автомобиля"
    )

    class Meta:
        model = Car
        fields = ['id', 'owner_id', 'make', 'model', 'year']
        read_only_fields = ['id']

    def to_representation(self, instance):
        #сериализатор для отображения
        return CarDetailSerializer(instance, context=self.context).data


class OrderSerializer(serializers.ModelSerializer):
    # запись / изменение заказа
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), 
        source='car',
        help_text="ID автомобиля"
    )

    class Meta:
        model = Order
        fields = ['id', 'car_id', 'description', 'price', 'status']
        read_only_fields = ['id']

    def to_representation(self, instance):
        #сериализатор для отображения
        return OrderDetailSerializer(instance, context=self.context).data