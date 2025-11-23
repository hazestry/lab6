from django.contrib import admin
from .models import Client, Car, Order

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'phone', 'address']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['user__date_joined']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Имя'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'make', 'model', 'year', 'owner']
    list_filter = ['make', 'year']
    search_fields = ['make', 'model', 'owner__user__username']
    autocomplete_fields = ['owner']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'status', 'price', 'date_created']
    list_filter = ['status', 'date_created']
    search_fields = ['description', 'car__make', 'car__model']
    date_hierarchy = 'date_created'
    readonly_fields = ['date_created']