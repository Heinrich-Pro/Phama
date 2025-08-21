from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
     model = OrderItem
     extra = 0
     readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'total_price', 'created_at')
     list_filter = ('created_at', 'user')
     search_fields = ('id', 'user__username')
     inlines = [OrderItemInline]
     readonly_fields = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
     list_display = ('order', 'product', 'quantity', 'price')
     list_filter = ('order',)
     search_fields = ('product__name',)