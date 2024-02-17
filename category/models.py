from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(unique=True,max_length=50)
    slug=models.SlugField(unique=True,max_length=50)
    images=models.ImageField(upload_to='category')
    def __str__(self):
        return self.category_name