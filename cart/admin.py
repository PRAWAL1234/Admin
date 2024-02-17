from django.contrib import admin
from .models import cart,CartItem

# Register your models here.
@admin.register(cart)

class cartAdmin(admin.ModelAdmin):
    list_display=('cart_id','created_date')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','user','id','quantity','is_active')