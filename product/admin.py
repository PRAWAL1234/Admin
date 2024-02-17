from django.contrib import admin
from .models import Product,Variation
# Register your models here.
@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display=('id','product_name','stock','price','category')
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Variation)

class variationAdmin(admin.ModelAdmin):
    list_display=('id','product')
