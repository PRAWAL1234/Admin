from django.db import models

# Create your models here.
class img(models.Model):
    image=models.ImageField(upload_to='footer')
    Create_date=models.DateField(auto_now_add=True)