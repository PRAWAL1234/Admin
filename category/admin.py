from django.contrib import admin
from .models import Category
# Register your models here.
@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display=('category_name','slug','id')
    prepopulated_fields={'slug':('category_name',)}