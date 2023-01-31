from django.contrib import admin

# Register your models here.

from .models import Item, OrderItem, Order, Category, ShippingAddress, Payment


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
