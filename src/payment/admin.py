from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register the ShippingAddress model
admin.site.register(ShippingAddress)

# Inline admin interface for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Set to 0 to prevent Django from adding extra empty rows

# Custom admin interface for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total', 'created_at']
    inlines = [OrderItemInline]  # Include OrderItemInline to display OrderItems within the Order admin page

# Register the Order model with the custom OrderAdmin
admin.site.register(Order, OrderAdmin)
