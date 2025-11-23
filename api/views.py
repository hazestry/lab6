from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Client, Car, Order
from .serializers import ClientSerializer, CarSerializer, OrderSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с клиентами.
    
    list: Получить список всех клиентов
    create: Создать нового клиента
    retrieve: Получить информацию о конкретном клиенте
    update: Обновить информацию о клиенте
    partial_update: Частично обновить информацию о клиенте
    destroy: Удалить клиента
    """
    queryset = Client.objects.all().select_related('user')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email', 'phone', 'address']
    ordering_fields = ['id', 'user__username']
    
    @action(detail=True, methods=['get'])
    def cars(self, request, pk=None):
        """Получить все автомобили клиента"""
        client = self.get_object()
        cars = client.cars.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с автомобилями.
    
    list: Получить список всех автомобилей
    create: Добавить новый автомобиль
    retrieve: Получить информацию о конкретном автомобиле
    update: Обновить информацию об автомобиле
    partial_update: Частично обновить информацию об автомобиле
    destroy: Удалить автомобиль
    """
    queryset = Car.objects.all().select_related('owner', 'owner__user')
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['make', 'year', 'owner']
    search_fields = ['make', 'model']
    ordering_fields = ['id', 'make', 'model', 'year']
    
    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        """Получить все заказы для автомобиля"""
        car = self.get_object()
        orders = car.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint для работы с заказами.
    
    list: Получить список всех заказов
    create: Создать новый заказ
    retrieve: Получить информацию о конкретном заказе
    update: Обновить информацию о заказе
    partial_update: Частично обновить информацию о заказе
    destroy: Удалить заказ
    """
    queryset = Order.objects.all().select_related('car', 'car__owner', 'car__owner__user')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'car', 'car__owner']
    search_fields = ['description']
    ordering_fields = ['id', 'date_created', 'price', 'status']
    ordering = ['-date_created']