# Generated by Django 5.1.3 on 2024-12-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_order_address_order_books_order_customer_order_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageOfWebSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('photo', models.ImageField(upload_to='website_photos/')),
            ],
        ),
    ]
