from django.contrib import admin
from .models import ShippingAddress, Order

admin.site.register(ShippingAddress)
admin.site.register(Order)
