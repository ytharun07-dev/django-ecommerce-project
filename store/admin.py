from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)