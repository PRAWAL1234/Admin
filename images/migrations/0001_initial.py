# Generated by Django 4.1.7 on 2024-02-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider Images')),
                ('Create_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
